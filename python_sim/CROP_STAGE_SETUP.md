# Crop Stage Detection (CNN) Setup

This module adds crop stage detection using a **crop-conditioned CNN (ResNet18 backbone)**.

## 1) Install Python dependencies

```bash
pip install torch torchvision pillow
```

## 2) Prepare dataset

Create this structure:

```text
python_sim/dataset/
  tomato/
    germination/*.jpg
    vegetative/*.jpg
    flowering/*.jpg
    maturity/*.jpg
  rice/
    germination/*.jpg
    vegetative/*.jpg
    flowering/*.jpg
    maturity/*.jpg
  wheat/
    germination/*.jpg
    vegetative/*.jpg
    flowering/*.jpg
    maturity/*.jpg
```

Stage labels used by the model are:
- `germination`
- `vegetative`
- `flowering`
- `maturity`

Crop folder names should match profile crop names in lowercase (e.g., `tomato`, `rice`).

## 3) Train the CNN model

```bash
python python_sim/train_crop_stage_cnn.py --dataset-root python_sim/dataset --epochs 15
```

Model output:
- `python_sim/models/crop_stage_model.pt`
- `python_sim/models/crop_stage_model.json`

## 4) Run web app prediction

Start app:

```bash
npm run dev
```

In the app sidebar, open **Crop Stage AI**, upload image, and run prediction.

## Optional environment variable

If your model path differs:

```bash
set CROP_STAGE_MODEL_PATH=python_sim/models/crop_stage_model.pt
```

## Notes

- If the model checkpoint is missing, backend returns a heuristic fallback result.
- For production-quality results, train with diverse field images per crop/stage.
