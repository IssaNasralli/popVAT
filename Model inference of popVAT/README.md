# Model Inference of popVAT

This folder contains the scripts required to generate a **pixel-level population map** using a trained popVAT model.

The inference stage reconstructs a full population raster by applying the trained model to every valid pixel of the ancillary dataset.

---

# 1. Files in this folder

- **`test_popVAE_full_Gate.py`**  
  Main execution script for both training and inference.

- **`popVAE_full_Gate_Atrous_Gate.py`**  
  Definition of the popVAT architecture and prediction utilities.

These files contain the full implementation details of the inference pipeline.

---

# 2. High-Level Inference Workflow

The population map construction follows these steps:

1. Load the multi-band raster containing ancillary variables.
2. Load the trained model weights.
3. Iterate through all pixels of the raster.
4. Extract:
   - a **local contextual patch**
   - a **larger global patch**
   - the **central pixel features**
5. Run the trained model to predict the population value.
6. Write the prediction to the output raster.
7. Continue until the entire raster is processed.

Batch prediction is used to accelerate computation and reduce memory usage.

A checkpoint file is automatically created during inference so that processing can resume from the last processed pixel if the execution stops.

---

# 3. Running the Population Prediction

Population map generation can be launched with the following command:

```bash
python3 test_popVAE_full_Gate.py \
--model_option GAG \
--batch_size 1025 \
--latent_dim 20 \
--patch_size_global 21 \
--training 0 \
--choice tunisia10 \
--country Tunisia \
--nb_masks 24 \
--weights

###Important:

training 0 switches the program to inference mode.

In this mode, the model is not trained.

A trained weights file must already exist.

If the --weights parameter is not explicitly provided, the script automatically constructs the expected file name using the provided parameters:

'''
best_weights_popVAE_full_{country}_{model_option}_{batch_size}_{latent_dim}_{patch_size_global}.h5
'''
This file must already exist in the working directory.



