# Building Foot print

This folder contains the scripts used to **evaluate the predicted population maps** produced by popVAT.

The evaluation follows the standard approach used in population-mapping studies:  
pixel-level predictions are aggregated to administrative units and compared with official census data.

---

# 1. Files in this folder

- **`r_squared.py`**  
  Main script used to compute evaluation metrics between predicted population rasters and official census data.

- **`data_atrous.py`**  
  Utilities for loading raster data, administrative masks, and census tables.

- **`evaluate.py`**  
  Functions used to compute evaluation metrics such as:
  - R²
  - Mean Absolute Error (MAE)
  - Mean Squared Error (MSE)

More detailed implementation can be explored directly in these files.

---

# 2. High-Level Evaluation Pipeline

The evaluation process follows these steps:

1. Load the predicted population raster.
2. Load administrative region masks.
3. Load official population statistics from INS.
4. Aggregate predicted population within each region.
5. Compare predicted totals with census data.
6. Compute statistical indicators.

This procedure measures how well the model reproduces **official population distribution across regions**.

---

# 3. Running the Evaluation

Example command:

```bash
python3 r_squared.py \
--raster tunisia10_popVAE_full_GAG_1024_30_best_weights_popVAE_full_Tunisia_GAG_1024_30.h5_predicted.tif \
--csv ins_population.csv \
```

Parameters
```bash
--raster      Path to the predicted population raster
--csv         CSV file containing INS population statistics
--region      Country or region name
--nb_masks    Number of administrative region masks
--region Tunisia \
--nb_masks 24
```

