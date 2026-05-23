# popVAT_Building-Test

> **ℹ️ Note:** This repository provides a **quick test harness** for the pretrained **popVAT_Building** model.  
> It is intended for **fast experimentation on small sample GeoTIFFs**.
>
> **To reproduce the full workflow from raw data, follow the pipeline below:**
>
> ```text
> ArcGIS (generate mosaic shapefile)
>        ↓
> Google Earth Engine (compute DEM & Slope)
>        ↓
> ArcGIS (project, resample, and add DEM/Slope bands to RGB tiles)
>        ↓
>    Training
>        ↓
>  Run Prediction
>        ↓
> Apply Threshold
>        ↓
> Apply Colorization
>        ↓
> Overlay Masks on Original Images
>        ↓
> Convert TIFF → PNG (Visualization)
>        ↓
> Qualitative Comparison
> ```
>
> **However, if you only want to test the model or perform building segmentation, you can skip all preprocessing and training steps and directly use the provided pretrained model for inference.**

This repository provides a **lightweight test harness** for the pretrained **popVAT_Building** model to segment **buildings** on updated test images that combine **RGB + DEM + Slope** layers (5 bands).

---

# 📦 Requirements

- Python 3.8+
- TensorFlow
- numpy
- rasterio

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 📂 Repository Structure

```text
popVAT_Building-Test/
│── README.md
│── popVAE_Gate_Atrous_Gate_Building.py
│── predict.py
│── threshold.py
│── color.py
│── overlay.py
│── conversion_png.py   # NEW: TIFF → PNG conversion for visualization
│── wheight.h5
│
├── test_updated/
├── test_original/
├── test_ground_truth/
│
├── output/
├── output_threshold_0.9/
├── output_colorized/
├── output_annotation_popVAT/
│
├── vis_original/        # PNG visualization
├── vis_ground_truth/    # PNG visualization
├── vis_pred/            # PNG visualization
```

---

# 🚀 Quick Start

## 1) Run Prediction

```bash
python predict.py
```

---

## 2) Apply Threshold

```bash
python threshold.py --threshold 0.9
```

---

## 3) Apply Colorization

```bash
python color.py --path output_threshold_0.9
```

---

## 4) Overlay Masks

```bash
python overlay.py
```

---

## 5) Convert TIFF → PNG (Visualization Step)

⚠️ Required for README visualization (GitHub cannot render TIFF)

Run:

```bash
python conversion_png.py
```

This creates:

```text
vis_original/
vis_ground_truth/
vis_pred/
```
---

# ⏱️ Inference Time

Average inference time per image (Prediction):

```text
10–15 minutes per image
```
---

# 📊 Qualitative Comparison: Ground Truth vs Input vs popVAT

We provide a **side-by-side evaluation**:

- Ground Truth (`test_ground_truth/`)
- Original Image (`test_original/`)
- popVAT Prediction (`output_annotation_popVAT/`)

---

# 📊 Qualitative Comparison: Ground Truth vs Input vs popVAT

| Ground Truth | Original Image | popVAT Prediction |
|--------------|----------------|-------------------|
| <img src="vis_ground_truth/22828930_15.png" width="100%"> | <img src="vis_original/22828930_15.png" width="100%"> | <img src="vis_pred/22828930_15.png" width="100%"> |
| <img src="vis_ground_truth/22828990_15.png" width="100%"> | <img src="vis_original/22828990_15.png" width="100%"> | <img src="vis_pred/22828990_15.png" width="100%"> |
| <img src="vis_ground_truth/228290100_15.png" width="100%"> | <img src="vis_original/228290100_15.png" width="100%"> | <img src="vis_pred/228290100_15.png" width="100%"> |
| <img src="vis_ground_truth/23429020_15.png" width="100%"> | <img src="vis_original/23429020_15.png" width="100%"> | <img src="vis_pred/23429020_15.png" width="100%"> |
| <img src="vis_ground_truth/23429080_15.png" width="100%"> | <img src="vis_original/23429080_15.png" width="100%"> | <img src="vis_pred/23429080_15.png" width="100%"> |
| <img src="vis_ground_truth/23578960_15.png" width="100%"> | <img src="vis_original/23578960_15.png" width="100%"> | <img src="vis_pred/23578960_15.png" width="100%"> |
| <img src="vis_ground_truth/23579005_15.png" width="100%"> | <img src="vis_original/23579005_15.png" width="100%"> | <img src="vis_pred/23579005_15.png" width="100%"> |
| <img src="vis_ground_truth/23729035_15.png" width="100%"> | <img src="vis_original/23729035_15.png" width="100%"> | <img src="vis_pred/23729035_15.png" width="100%"> |
| <img src="vis_ground_truth/23879080_15.png" width="100%"> | <img src="vis_original/23879080_15.png" width="100%"> | <img src="vis_pred/23879080_15.png" width="100%"> |
| <img src="vis_ground_truth/24179065_15.png" width="100%"> | <img src="vis_original/24179065_15.png" width="100%"> | <img src="vis_pred/24179065_15.png" width="100%"> |


# ⚡ Full Pipeline

```text
predict.py
    ↓
threshold.py
    ↓
color.py
    ↓
overlay.py
    ↓
conversion_png.py
    ↓
visualization
```

---

