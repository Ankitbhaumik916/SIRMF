import base64
import io
import json
import os
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


DEFAULT_STAGE_NAMES = ["germination", "vegetative", "flowering", "maturity"]


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
        combined = torch.cat([image_features, crop_features], dim=1)
        return self.classifier(combined)


def _build_transform(image_size: int = 224):
    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )


def _load_image_from_base64(image_base64: str) -> Image.Image:
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return image


def _heuristic_fallback(image: Image.Image):
    image = image.resize((128, 128))
    pixels = list(image.getdata())

    green_score = sum(p[1] - 0.5 * (p[0] + p[2]) for p in pixels) / len(pixels)

    if green_score < 8:
        stage = "germination"
        confidence = 0.45
    elif green_score < 18:
        stage = "vegetative"
        confidence = 0.52
    elif green_score < 28:
        stage = "flowering"
        confidence = 0.50
    else:
        stage = "maturity"
        confidence = 0.48

    return {
        "stage": stage,
        "confidence": confidence,
        "topPredictions": [
            {"stage": stage, "confidence": confidence},
        ],
        "model": "heuristic-fallback",
    }


def _default_checkpoint_path() -> Path:
    return Path(__file__).parent / "models" / "crop_stage_model.pt"


def predict_crop_stage(image_base64: str, crop_type: str, model_path: str = ""):
    checkpoint_path = Path(model_path) if model_path else _default_checkpoint_path()

    image = _load_image_from_base64(image_base64)

    if not checkpoint_path.exists():
        fallback = _heuristic_fallback(image)
        return {
            "cropType": crop_type,
            **fallback,
            "note": "CNN model checkpoint not found. Train model to enable full CNN inference.",
        }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(checkpoint_path, map_location=device)

    stage_names = checkpoint.get("stage_names", DEFAULT_STAGE_NAMES)
    crop_to_idx = checkpoint.get("crop_to_idx", {})
    crop_key = (crop_type or "").strip().lower()

    if crop_key not in crop_to_idx:
        return {
            "cropType": crop_type,
            "stage": "unknown",
            "confidence": 0.0,
            "topPredictions": [],
            "model": "cnn-resnet18-crop-conditioned",
            "error": f"Crop '{crop_type}' not present in trained crop list.",
        }

    num_stages = len(stage_names)
    num_crops = len(crop_to_idx)

    model = CropStageNet(num_stages=num_stages, num_crops=num_crops)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    transform = _build_transform(checkpoint.get("image_size", 224))
    tensor = transform(image).unsqueeze(0).to(device)
    crop_id = torch.tensor([crop_to_idx[crop_key]], dtype=torch.long, device=device)

    with torch.no_grad():
        logits = model(tensor, crop_id)
        probs = torch.softmax(logits, dim=1).squeeze(0)

    top_values, top_indices = torch.topk(probs, k=min(3, num_stages))
    top_predictions = [
        {
            "stage": stage_names[idx.item()],
            "confidence": float(val.item()),
        }
        for val, idx in zip(top_values, top_indices)
    ]

    best = top_predictions[0]

    return {
        "cropType": crop_type,
        "stage": best["stage"],
        "confidence": best["confidence"],
        "topPredictions": top_predictions,
        "model": "cnn-resnet18-crop-conditioned",
    }


def main():
    try:
        payload = json.loads(os.sys.stdin.read())
        crop_type = payload.get("cropType", "")
        image_base64 = payload.get("imageBase64", "")
        model_path = payload.get("modelPath", "")

        if not image_base64:
            raise ValueError("imageBase64 is required")

        result = predict_crop_stage(image_base64=image_base64, crop_type=crop_type, model_path=model_path)
        print(json.dumps(result))
    except Exception as exc:
        error_payload = {
            "error": str(exc),
            "model": "cnn-resnet18-crop-conditioned",
        }
        print(json.dumps(error_payload))
        os.sys.exit(1)


if __name__ == "__main__":
    main()
