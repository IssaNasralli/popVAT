# popVAT_Population –France Example of Population Mapping from GeoTIFF

> **ℹ️ Note:** This repository provides a reproducible implementation of the **popVAT_Population** framework, tested for Tunisia, for France population mapping using multisource geospatial data and deep learning.
>
> The workflow supports:
>
> - Training from scratch
> - Fine-tuning from pretrained weights
> - Population prediction (inference)
> - Quantitative evaluation against census data
>
> The experiments reported in our paper can be reproduced on the **France (Île-de-France)** dataset using the commands provided below.

---

# Workflow Overview

The recommended workflow is:

```
Prepare GeoTIFF inputs
          ↓
Train or Fine-tune Model
          ↓
Generate Population Predictions
          ↓
Evaluate Results (R², MAE, RMSE, etc.)
```

### Prepare GeoTIFF Inputs

Users can either:

1. Prepare their own input raster data and corresponding population target raster following the same format expected by the framework, or

2. Directly use the ready-to-use files provided in this repository:

```text
france10.tif
POP_France.tif
```

These files contain the GeoTIFF inputs and reference population raster used for the France experiment presented in the paper.

---

# Requirements

Install the required Python packages before running the code:

```bash
pip install -r requirements.txt
```

---

# Repository Contents

```text
generalization_france/
│
├── France_Regions/
│   ├── France_Region_0.tif
│   ├── France_Region_1.tif
│   └── ...
│
├── POP_France.tif
├── README.md
├── best_weights_popVAE_full_France_GAG_1025_20_21.h5
├── data_atrous.py
├── evaluate.py
├── france10.part1.rar
├── france10.part2.rar
├── france10_popVAE_full_GAG_1025_20__best_weights_...
├── insee_population.csv
├── popVAE_full_Gate_Atrous_Gate.py
├── requirements.txt
└── test_popVAE_full_Gate.py
```

### Content Description

| File / Folder | Description |
|--------------|-------------|
| `France_Regions/` | Contains regional GeoTIFF files named `France_Region_X.tif` (X = 0, 1, ...). These files are used for the cross-country generalization experiments. |
| `POP_France.tif` | Reference population raster used during training and evaluation. |
| `france10.part1.rar` / `france10.part2.rar` | Compressed archive containing the France multisource GeoTIFF dataset (`france10.tif`). Extract both parts before use. |
| `best_weights_popVAE_full_France_GAG_1025_20_21.h5` | Pretrained model weights provided for reproduction and inference. |
| `test_popVAE_full_Gate.py` | Main script for training and inference. |
| `evaluate.py` | Evaluation utilities. |
| `data_atrous.py` | Data loading and preprocessing utilities. |
| `popVAE_full_Gate_Atrous_Gate.py` | Neural network architecture implementation. |
| `insee_population.csv` | Official census population data used for quantitative evaluation. |
| `requirements.txt` | Python package dependencies. |

---

# Dataset

The France experiment uses:

- Multisource GeoTIFF imagery
- Auxiliary geographic layers
- Census population data (`insee_population.csv`)

Place all required files in the appropriate data directories before running the scripts.

---

# Model Training

The main training script is:

```bash
test_popVAE_full_Gate.py
```

The implementation supports two training modes:

1. Training from scratch
2. Fine-tuning from pretrained weights

---

## 1. Training Using a Pretrained Model

To continue training (fine-tuning) from an existing checkpoint:

```bash
python test_popVAE_full_Gate.py \
    --model_option GAG \
    --batch_size 1025 \
    --latent_dim 20 \
    --patch_size_global 21 \
    --training 1 \
    --choice france10 \
    --country France \
    --weights best_weights_popVAE_full_France_GAG_1025_20_21.h5 \
    --nb_masks 8
```

The model will load the specified weight file and continue training from that checkpoint.

---

## 2. Training From Scratch

To start a new training session:

```bash
python test_popVAE_full_Gate.py \
    --model_option GAG \
    --batch_size 1025 \
    --latent_dim 20 \
    --patch_size_global 21 \
    --training 1 \
    --choice france10 \
    --country France \
    --nb_masks 8
```

### Important Note

The training script automatically constructs the expected checkpoint filename using the provided command-line parameters and attempts to load it if it exists.

During startup, the script will display one of the following messages:

```text
Best weight found
```

or

```text
No Best weights. Training from scratch.
```

If you want to guarantee a completely fresh training run:

- Rename the existing checkpoint file, or
- Delete the checkpoint file

When the message

```text
No Best weights. Training from scratch.
```

appears, the model is starting from randomly initialized weights.

---

# Population Prediction (Inference)

Inference mode generates the predicted population raster using a trained model.

---

## Inference Using Automatic Weight Detection

```bash
python test_popVAE_full_Gate.py \
    --model_option GAG \
    --batch_size 1025 \
    --latent_dim 20 \
    --patch_size_global 21 \
    --training 0 \
    --choice france10 \
    --country France \
    --nb_masks 8
```

The script automatically searches for the checkpoint whose filename matches the supplied parameters.

---

## Inference Using a Specific Weight File

```bash
python test_popVAE_full_Gate.py \
    --model_option GAG \
    --batch_size 1025 \
    --latent_dim 20 \
    --patch_size_global 21 \
    --training 0 \
    --choice france10 \
    --country France \
    --weights best_weights_popVAE_full_France_GAG_1025_20_21.h5 \
    --nb_masks 8
```

### Important Note

If the `--weights` argument is provided, the specified file is used.

Otherwise, the script automatically constructs the expected checkpoint filename from the command parameters and attempts to locate the corresponding model weights.

---

# Model Evaluation

After generating the predicted population raster, evaluate the results against census data using:

```bash
python3 r_squared.py \
    --raster france10_popVAE_full_GAG_1025_20__best_weights_popVAE_full_France_GAG_1025_20_21.h5__21_predicted.tif \
    --csv insee_population.csv \
    --region France \
    --nb_masks 8
```

The evaluation script computes statistical metrics comparing predicted and reference populations, including:

- R² (Coefficient of Determination)
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

These metrics are used throughout the paper to assess model performance.

---

# Example Configuration Used in the Paper

The France experiments reported in the paper were conducted using:

| Parameter | Value |
|------------|---------|
| Model | GAG |
| Batch Size | 1025 |
| Latent Dimension | 20 |
| Patch Size | 21 |
| Number of Masks | 8 |
| Region | France |
| Dataset | france10 |

---

# Output Files

Typical outputs include:

### Trained Weights

```text
best_weights_popVAE_full_France_GAG_1025_20_21.h5
```

### Predicted Population Raster

```text
france10_popVAE_full_GAG_1025_20__best_weights_popVAE_full_France_GAG_1025_20_21.h5__21_predicted.tif
```

### Evaluation Results

Performance statistics printed by:

```bash
r_squared.py

---

# Contact

For questions, bug reports, or collaboration inquiries, please open an issue in this repository.
