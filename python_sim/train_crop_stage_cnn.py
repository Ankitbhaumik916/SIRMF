import argparse
import json
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms


STAGE_NAMES = ["germination", "vegetative", "flowering", "maturity"]


class CropStageNet(nn.Module):
    def __init__(self, num_stages: int, num_crops: int, crop_embed_dim: int = 16):
        super().__init__()
        backbone = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        in_features = backbone.fc.in_features
        backbone.fc = nn.Identity()

        self.backbone = backbone
        self.crop_embedding = nn.Embedding(num_crops, crop_embed_dim)
        self.classifier = nn.Sequential(
            nn.Linear(in_features + crop_embed_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(256, num_stages),
        )

    def forward(self, images, crop_ids):
        image_features = self.backbone(images)
        crop_features = self.crop_embedding(crop_ids)
        return self.classifier(torch.cat([image_features, crop_features], dim=1))


class CropStageDataset(Dataset):
    def __init__(self, samples, crop_to_idx, stage_to_idx, transform=None):
        self.samples = samples
        self.crop_to_idx = crop_to_idx
        self.stage_to_idx = stage_to_idx
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image_path, crop_name, stage_name = self.samples[idx]
        image = Image.open(image_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        crop_id = self.crop_to_idx[crop_name]
        stage_id = self.stage_to_idx[stage_name]

        return image, torch.tensor(crop_id, dtype=torch.long), torch.tensor(stage_id, dtype=torch.long)


def discover_dataset(dataset_root: Path):
    samples = []

    for crop_dir in dataset_root.iterdir():
        if not crop_dir.is_dir():
            continue

        crop_name = crop_dir.name.strip().lower()

        for stage_name in STAGE_NAMES:
            stage_dir = crop_dir / stage_name
            if not stage_dir.exists() or not stage_dir.is_dir():
                continue

            for image_path in stage_dir.glob("*"):
                if image_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
                    samples.append((image_path, crop_name, stage_name))

    if not samples:
        raise ValueError(
            "No samples found. Expected dataset structure: dataset/<crop>/<stage>/*.jpg"
        )

    return samples


def stratified_split(samples, val_ratio=0.2):
    grouped = defaultdict(list)
    for sample in samples:
        _, crop_name, stage_name = sample
        grouped[(crop_name, stage_name)].append(sample)

    train_samples, val_samples = [], []

    for _, group_samples in grouped.items():
        group_samples = sorted(group_samples, key=lambda item: str(item[0]))
        cutoff = max(1, int(len(group_samples) * (1 - val_ratio)))
        train_samples.extend(group_samples[:cutoff])
        val_samples.extend(group_samples[cutoff:])

    return train_samples, val_samples


def train(args):
    dataset_root = Path(args.dataset_root)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    samples = discover_dataset(dataset_root)
    train_samples, val_samples = stratified_split(samples, val_ratio=args.val_ratio)

    crop_names = sorted({sample[1] for sample in samples})
    crop_to_idx = {crop: idx for idx, crop in enumerate(crop_names)}
    stage_to_idx = {stage: idx for idx, stage in enumerate(STAGE_NAMES)}

    train_transform = transforms.Compose(
        [
            transforms.Resize((args.image_size, args.image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=12),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    eval_transform = transforms.Compose(
        [
            transforms.Resize((args.image_size, args.image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    train_dataset = CropStageDataset(train_samples, crop_to_idx, stage_to_idx, train_transform)
    val_dataset = CropStageDataset(val_samples, crop_to_idx, stage_to_idx, eval_transform)

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CropStageNet(num_stages=len(STAGE_NAMES), num_crops=len(crop_to_idx))
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)

    best_acc = 0.0

    for epoch in range(args.epochs):
        model.train()
        running_loss = 0.0

        for images, crop_ids, labels in train_loader:
            images, crop_ids, labels = images.to(device), crop_ids.to(device), labels.to(device)
            optimizer.zero_grad()
            logits = model(images, crop_ids)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for images, crop_ids, labels in val_loader:
                images, crop_ids, labels = images.to(device), crop_ids.to(device), labels.to(device)
                logits = model(images, crop_ids)
                preds = torch.argmax(logits, dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

        val_acc = correct / total if total > 0 else 0
        avg_loss = running_loss / max(1, len(train_loader))
        print(f"Epoch {epoch + 1}/{args.epochs} | loss={avg_loss:.4f} | val_acc={val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            checkpoint = {
                "model_state_dict": model.state_dict(),
                "crop_to_idx": crop_to_idx,
                "stage_names": STAGE_NAMES,
                "image_size": args.image_size,
                "best_val_acc": best_acc,
            }
            torch.save(checkpoint, output_path)

    metadata_path = output_path.with_suffix(".json")
    metadata = {
        "dataset_root": str(dataset_root),
        "output": str(output_path),
        "num_samples": len(samples),
        "train_samples": len(train_samples),
        "val_samples": len(val_samples),
        "crop_to_idx": crop_to_idx,
        "stage_names": STAGE_NAMES,
        "best_val_acc": best_acc,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.lr,
        "image_size": args.image_size,
    }

    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print("\nTraining complete")
    print(f"Best validation accuracy: {best_acc:.4f}")
    print(f"Checkpoint saved to: {output_path}")
    print(f"Metadata saved to: {metadata_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Train crop stage CNN model")
    parser.add_argument(
        "--dataset-root",
        type=str,
        default=str(Path(__file__).parent / "dataset"),
        help="Dataset root path with structure: dataset/<crop>/<stage>/*.jpg",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(Path(__file__).parent / "models" / "crop_stage_model.pt"),
        help="Output checkpoint path",
    )
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--image-size", type=int, default=224)
    return parser.parse_args()


if __name__ == "__main__":
    train(parse_args())
