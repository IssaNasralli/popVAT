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

<img src="detection_four.png" width="75%"> 

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
visualization
```

---

