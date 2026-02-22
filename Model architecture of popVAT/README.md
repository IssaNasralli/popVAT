# Model Architecture of popVAT

This folder contains the implementation of the **popVAT** model, a deep learning framework for population estimation using a combination of **Variational Autoencoder (VAE)**, **atrous convolution**, and **gating mechanisms**.

The main file in this folder is:

- `popVAE_full_Gate_Atrous_Gate.py` — contains the full model implementation, data generators, VAE encoders/decoders, and prediction pipelines.

---

## High-Level Architecture

The **popVAT** model follows a **multi-branch, hierarchical design** to capture spatial patterns at different scales:

### 1. Medium-range Encoder–Decoder Branch
- Learns **contextual latent representations** `z` from medium-sized patches.
- Uses a **VAE** with residual blocks and dense layers.
- Includes a **learnable gating mechanism (G_m)** to modulate the latent vector before merging with other branches.

### 2. Pixel-level Branch
- Preserves **fine spatial details** for each pixel.
- Feeds the central pixel of the patch directly into the final prediction layers.

### 3. Global Atrous Convolution Branch
- Captures **large-scale spatial dependencies** from global patches using multiple **dilated convolutions** (atrous rates: 1, 3, 11, 17).
- Applies **global average pooling** to extract summary features.
- Modulated by a learnable **global gating mechanism (G_g)** before integration.

### 4. Integration & Prediction
- Outputs of all branches (`z`, pixel-level features, global features) are **concatenated**.
- Followed by a few convolutional layers and **global average pooling** to reduce the features to a scalar.
- The final output is the **predicted population density** for each pixel.

### 5. Training Loss
- Combines **VAE reconstruction loss**, **KL divergence**, and **population prediction loss**.
- Implemented in a custom `VAELossLayer`.

---

## Data Handling

Two `tf.keras.utils.Sequence` generators are provided:

1. `DataGenerator` – for medium-range + pixel-level patches.  
2. `DataGeneratorAtrous` – for medium-range, pixel-level, and global patches with atrous convolution.

They handle batching, patch extraction, and shuffling for efficient training.

---

## Prediction Pipeline

- The functions `predict_and_reconstruct_GAG_GA` and `predict_and_reconstruct_G` reconstruct population maps from input geospatial raster data.
- Supports **checkpointing** to resume predictions on large rasters.
- Ensures **population values remain within realistic bounds** and applies `np.expm1` to reverse log-transformation.

---

## Note

- Detailed implementation, hyperparameters, and usage examples are available by exploring `popVAE_full_Gate_Atrous_Gate.py`.

---

