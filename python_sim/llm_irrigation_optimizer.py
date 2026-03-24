import argparse
import base64
import json
from pathlib import Path

from crop_stage_inference import predict_crop_stage


DEFAULT_CHECKPOINT_PATH = Path(__file__).resolve().parent.parent / "best.pt"


def _image_file_to_base64(image_path: Path) -> str:
    return base64.b64encode(image_path.read_bytes()).decode("utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Rice crop stage detection using local best.pt")
    parser.add_argument("--image-path", required=True, help="Path to input rice image")
    parser.add_argument("--crop-type", default="rice", help="Crop type (default: rice)")
    parser.add_argument("--checkpoint-path", default=str(DEFAULT_CHECKPOINT_PATH), help="Path to checkpoint (.pt)")
    return parser.parse_args()


def main():
    args = parse_args()
    image_path = Path(args.image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image_base64 = _image_file_to_base64(image_path)
    result = predict_crop_stage(
        image_base64=image_base64,
        crop_type=args.crop_type,
        model_path=args.checkpoint_path,
    )
    print(json.dumps(result))


if __name__ == "__main__":
    main()
