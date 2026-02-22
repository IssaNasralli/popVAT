# Model training of popVAT

This folder contains scripts and resources required to train the **popVAT** model for population mapping using a Variational Autoencoder with hierarchical gating and atrous convolutions.

---

## 1. Files included

- **`test_popVAE_full_Gate.py`** – Main training and inference script. Handles model creation, data loading, training, and evaluation. Supports multiple model options for ablation studies
- **`data_atrous.py`** – Data processing utilities including:

  - Loading and preprocessing raster datasets  
  - Generating composite raster bands: mergin the educational POI layers into one comprehensive layer


---

## 2. Dependencies

Make sure the following Python packages are installed:

```bash
tensorflow 2.15.1
numpy
pandas
scikit-learn
rasterio
```
Other requirements:

Python ≥ 3.8

GPU recommended for training (NVIDIA Tesla K80 or higher)

Sufficient RAM for raster processing (≥32 GB recommended)

## 3. Preparing the Data
Before running the training script, ensure the following:

The final multi-band raster (tunisia10.tif) is available in the working directory.

All preprocessing steps should have been performed using data_atrous.py utilities if needed.

## 4. Training the Model

Use the main script test_popVAE_full_Gate.py to train the model.

Command:
```bash
python3 test_popVAE_full_Gate.py \
    --model_option GAG \
    --batch_size 1025 \
    --latent_dim 20 \
    --patch_size_global 21 \
    --training 1 \
    --choice tunisia10 \
    --country Tunisia \
     --weights	
```
Parameters:
```bash

--model_option	Model variant for ablation
--batch_size	Training batch size
--latent_dim	Dimension of latent representation
--patch_size_global	Size of the global patch for atrous convolution
--training	1 for training, 0 for inference
--choice	Base name of input raster file (e.g., tunisia10)
--country	Country name for district mask loading
--weights	Pre-trained weights file (optional; leave empty to train from scratch)

```
## 5. Output
After training, the script will produce:

Model weights: e.g., best_weights_popVAE_full_Tunisia_GAG_1025_20_21.h5

Model architecture JSON: e.g., model_architecture_popVAE_full_Tunisia_GAG_1025_20_21.json

## 6. Notes

- **Pretrained Weights:** A pretrained model corresponding to the best-performing configuration is already provided in this folder:  
  `best_weights_popVAE_full_Tunisia_GAG_1025_20_21.h5`. You can use it directly for inference or as a starting point for further fine-tuning by specifying it with the `--weights` argument in the training script.


Random Seeds: Seeds are set for reproducibility (tf, numpy, random).

Data Reduction Heuristic: Only a subset of the raster pixels is used to match the number of trainable parameters, ensuring stable learning and spatial generalization.

Logging: Training progress results are printed in the console.
