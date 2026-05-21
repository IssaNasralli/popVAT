# popVAT Population Estimation – France Example

This repository provides scripts for training, inference, and evaluation of the **popVAE** population estimation framework.

---

## Training

### 1. Fine-Tuning / Training Using a Pretrained Model

To continue training from an existing pretrained model:

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

The model will initialize from the specified weight file and continue training.

---

### 2. Training From Scratch

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

> **Important Note**
>
> The training script automatically attempts to locate an existing weight file using the standard naming convention employed by the framework.
>
> During startup, the script will display one of the following messages:
>
> - **"Best weight found"** → an existing checkpoint has been detected and training will resume from it.
> - **"No Best weights. Training from scratch."** → no compatible checkpoint was found and a completely new model will be trained.
>
> If you want to ensure a true training-from-scratch experiment, rename, move, or delete any previously generated weight files that match the current configuration.

---

## Inference

### Option 1 – Automatic Weight Discovery

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

The script will automatically search for the appropriate weight file based on the provided configuration parameters.

---

### Option 2 – Specify a Weight File Explicitly

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

> **Note**
>
> If the `--weights` argument is provided, the specified model checkpoint will be used directly.
>
> Otherwise, the script will attempt to locate the most appropriate checkpoint automatically using the command parameters.

---

## Evaluation

After inference, evaluate the generated population raster using the coefficient of determination (R²):

```bash
python3 r_squared.py \
    --raster france10_popVAE_full_GAG_1025_20__best_weights_popVAE_full_France_GAG_1025_20_21.h5__21_predicted.tif \
    --csv insee_population.csv \
    --region France \
    --nb_masks 8
```

### Inputs

- `--raster` : Predicted population raster generated during inference.
- `--csv` : Reference census/population data.
- `--region` : Region or country name.
- `--nb_masks` : Number of masks used during prediction.

### Output

The script computes and reports the **R² (coefficient of determination)** between the predicted population estimates and the reference census values.

---
