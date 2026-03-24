import base64
import io
import json
import os
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import SegformerConfig, SegformerForSemanticSegmentation


DEFAULT_STAGE_NAMES = ["Vegetative", "Booting/Heading", "Grain Filling", "Ripening"]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_RICE_STAGE_MODEL = None
_RICE_STAGE_META = {}


def _safe_ratio(num, den):
    return float(num) / float(den) if den > 0 else 0.0


def rice_features_from_mask(mask_np):
    green = int((mask_np == 1).sum())
    senescent = int((mask_np == 2).sum())
    panicle = int((mask_np == 3).sum())
    rice_total = green + senescent + panicle
    return {
        "rice_total": rice_total,
        "green_ratio": _safe_ratio(green, rice_total),
        "senescent_ratio": _safe_ratio(senescent, rice_total),
        "panicle_ratio": _safe_ratio(panicle, rice_total),
    }


def stage_from_rice_features(feat):
    p = feat["panicle_ratio"]
    s = feat["senescent_ratio"]

    if p < 0.03 and s < 0.20:
        return "Vegetative"
    if p < 0.12 and s < 0.30:
        return "Booting/Heading"
    if s < 0.45:
        return "Grain Filling"
    return "Ripening"


def _rule_confidence(feat):
    p = feat["panicle_ratio"]
    s = feat["senescent_ratio"]
    nearest_boundary = min(abs(p - 0.03), abs(p - 0.12), abs(s - 0.20), abs(s - 0.30), abs(s - 0.45))
    return min(1.0, nearest_boundary / 0.15)


def _infer_segformer_params(state_dict):
    hidden_sizes = [
        state_dict[f"segformer.encoder.patch_embeddings.{i}.proj.weight"].shape[0]
        for i in range(4)
    ]

    depths = []
    for stage_idx in range(4):
        prefix = f"segformer.encoder.block.{stage_idx}."
        block_indices = []
        for key in state_dict.keys():
            if key.startswith(prefix):
                block_indices.append(int(key.split(".")[4]))
        depths.append(max(block_indices) + 1 if block_indices else 0)

    decoder_hidden_size = state_dict["decode_head.linear_c.0.proj.weight"].shape[0]

    return {
        "hidden_sizes": hidden_sizes,
        "depths": depths,
        "decoder_hidden_size": decoder_hidden_size,
    }


def _load_image_from_base64(image_base64: str) -> Image.Image:
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return image


def _preprocess_pil_image(image: Image.Image, image_size: int):
    image_resized = image.resize((image_size, image_size), Image.BILINEAR)
    arr = np.asarray(image_resized, dtype=np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))
    tensor = torch.from_numpy(arr)

    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
    tensor = (tensor - mean) / std
    return tensor.unsqueeze(0)


def _default_checkpoint_path() -> Path:
    return Path(__file__).resolve().parent.parent / "best.pt"


def _load_rice_stage_model(checkpoint_path: Path):
    global _RICE_STAGE_MODEL, _RICE_STAGE_META

    if _RICE_STAGE_MODEL is not None and _RICE_STAGE_META.get("checkpoint") == str(checkpoint_path):
        return _RICE_STAGE_MODEL, _RICE_STAGE_META

    checkpoint = torch.load(checkpoint_path, map_location=DEVICE)
    state_dict = checkpoint["model"]
    num_classes = int(checkpoint.get("config", {}).get("num_classes", 6))
    img_size = int(checkpoint.get("config", {}).get("img_size", 512))

    params = _infer_segformer_params(state_dict)
    config = SegformerConfig(
        num_labels=num_classes,
        hidden_sizes=params["hidden_sizes"],
        depths=params["depths"],
        decoder_hidden_size=params["decoder_hidden_size"],
    )

    model = SegformerForSemanticSegmentation(config)
    model.load_state_dict(state_dict, strict=True)
    model.to(DEVICE)
    model.eval()

    _RICE_STAGE_MODEL = model
    _RICE_STAGE_META = {
        "checkpoint": str(checkpoint_path),
        "img_size": img_size,
        "num_classes": num_classes,
    }
    return _RICE_STAGE_MODEL, _RICE_STAGE_META


def predict_crop_stage(image_base64: str, crop_type: str, model_path: str = ""):
    checkpoint_path = Path(model_path) if model_path else _default_checkpoint_path()
    image = _load_image_from_base64(image_base64)

    if not checkpoint_path.exists():
        return {
            "cropType": crop_type,
            "stage": "unknown",
            "confidence": 0.0,
            "topPredictions": [],
            "model": "segformer-bestpt-rice-rules",
            "error": f"Checkpoint not found: {checkpoint_path}",
        }

    model, meta = _load_rice_stage_model(checkpoint_path)
    x = _preprocess_pil_image(image, image_size=meta["img_size"]).to(DEVICE)

    with torch.no_grad():
        logits = model(pixel_values=x).logits
        logits = F.interpolate(
            logits,
            size=(meta["img_size"], meta["img_size"]),
            mode="bilinear",
            align_corners=False,
        )
        probs = F.softmax(logits, dim=1)

    pred_mask = probs.argmax(1)[0].cpu().numpy()
    max_probs = probs.max(1).values[0].cpu().numpy()

    feat = rice_features_from_mask(pred_mask)
    best_stage = stage_from_rice_features(feat)

    rice_region = (pred_mask == 1) | (pred_mask == 2) | (pred_mask == 3)
    seg_conf = float(max_probs[rice_region].mean()) if rice_region.any() else float(max_probs.mean())
    rule_conf = _rule_confidence(feat)
    final_conf = float(0.7 * seg_conf + 0.3 * rule_conf)

    top_predictions = [{"stage": best_stage, "confidence": final_conf}]
    crop_key = (crop_type or "").strip().lower()
    note = None
    if crop_key and crop_key != "rice":
        note = "Current stage rules are tuned for rice masks; results for non-rice crops may be unreliable."

    result = {
        "cropType": crop_type,
        "stage": best_stage,
        "confidence": final_conf,
        "topPredictions": top_predictions,
        "model": "segformer-bestpt-rice-rules",
    }
    if note:
        result["note"] = note
    return result


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
