# popVAT: Population Mapping using Variational Autoencoder with Transfer Learning

## 1. Introduction

This repository provides the implementation of **popVAT**, an extension of the **popVAE** framework for high-resolution population mapping.  
popVAT uses the **same datasets as popVAE**, while the **deep learning model is modified** to improve performance.

The overall workflow and the location of the study area (**Tunisia**) are illustrated in **Figure 1-a of popVAE**:

![ ](area.png)
---

# 2. Dataset

This section explains the **data assembly, preprocessing and transformation workflow** used in the study.  
The full workflow is illustrated in **Figure 1 of popVAT**:
![ ](flowchart.png)

The dataset consists of **population data** and several **ancillary datasets**.

---

# 2.1 Population Data

Four population datasets were used:

- WorldPop  
- GPWv4  
- LandScan  
- INS (Institut National de la Statistique – Tunisia)

Original sources:

- WorldPop: https://hub.worldpop.org/doi/10.5258/soton/wp00536
- GPWv4: https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-gpwv4-popdens-r11-4.11
- LandScan: https://landscan.ornl.gov/ 
- INS: https://www.ins.tn/statistiques/111

Because some of these datasets require downloading **global rasters and extracting Tunisia**, we provide ready-to-use files.

Folder:

Population Data/

Files:

POP.tif  
gpwv4.tif  
landscan.tif  
ins_population.csv 

Users can either download the original datasets or directly use the provided files.

---

# 2.2 Ancillary Data

## 2.2.1 Educational POI

Educational POIs include:

- Schools  
- Preparatory schools  
- Institutes  

The original tabular dataset download link is provided in the folder "Educational POI".

Because the source platform continuously updates the dataset (overwriting old versions),  
the exact version used in this study is also provided in the folder "Educational POI":POI.xls

Detailed workflow is provided in the foler "Educational POI"

Final Raster KDE files (three files: KDE_Institute.tif, KDE_Preparatory_School.tif and KDE_School.tif) are available here: 👉 [Download](https://drive.google.com/file/d/1SuQS-xPlnfEbJ7ugH-FrqkZTjLAvFdV-/view?usp=sharing)

---

# 2.2.3 Land Use (LU)

Land Use data were extracted from **OpenStreetMap (OSM)**.

Download via HOT Export Tool:

https://export.hotosm.org/

LU data used in the study (polygons shapefile) are provided in the folder "LU"

Rasterization of non-residential areas instructions are provided in the same folder.

---

# 2.2.4 Building Footprint

Original dataset: WSF2019  
https://download.geoservice.dlr.de/WSF2019/

Since the dataset is distributed as tiles, we provide the assembled Tunisia file: WSF2019.tif  👉 [Download](https://drive.google.com/file/d/1J0v0zZ0NSz3B5LQY5kWo04d__JzPMrGY/view?usp=sharing)

### Processing

1. WSF2019 was checked against the **non-residential binary mask**.
2. Building heights from WSF 3D were used.
3. Heights were reclassified:

Number of floors = pixel height / 3 meters

4. Floors were multiplied with the checked WSF2019 dataset.

Detailed steps are provided in the folder "Building Foot print"

Final dataset used in the study: Tunisia_floor_WSF2019_WGS_84_32N_0to1_residentiel.tif   👉 [Download](https://drive.google.com/file/d/1qPOQBsoA2vIOGjng7ZVT7OWqlF6S1oxa/view?usp=sharing)

---

# 2.2.5 Road Network

Road network data were extracted from **OpenStreetMap (OSM)**.

Processing:

1. Major roads were selected (excluding residential and service roads).
2. Batch Processing tool was used to snap road segments.
3. Intersect tool identified intersection points.
4. Point Density tool generated the raster layer.

Data used in the study are provided in the folder "Road Network"

Final dataset used in the study: road_densities_12128.tif   👉 [Download](https://drive.google.com/file/d/1VFsWsCtAvKQP5ZiUpeHONPsvq_HDS9ri/view?usp=sharing)


---

# 2.2.6 Satellite Imagery

Satellite imagery was obtained using **Google Earth Engine**.

Detailed workflow is provided in the folder "Satellite Imagery"
Final dataset used in the study: MODIS.tif   👉 [Download](https://drive.google.com/file/d/1mTkBDegUozfW1Ffla3Dv5yIhrBFuEGwF/view?usp=sharing)


---

# 2.2.7 LULC

LULC data were also obtained using **Google Earth Engine**.

Details are available in the folder "LULC"

Final dataset used in the study: LULC.tif   👉 [Download](https://drive.google.com/file/d/1TUnvS1eyw--JxcGEyXqEAmc3b82ajoLW/view?usp=sharing)

---

# 2.2.8 GAUL

Administrative boundaries were obtained using **Google Earth Engine**.

Processing:

Each governorate boundary shapefile was converted to raster with:

Width: 3807  
Height: 8116  

Pixel values:

Inside boundary = 1

Outside boundary = 0

Details are available in the folder "GAUL"

Files are provided in the folder "Tunisia_Regions": 24 tif files (24 gouvernorates)

---

# 2.2.9 DEM and Slope

Datasets obtained using **Google Earth Engine**.

Processing details in the folder "DEM and Slope"

Final datasets:

dem.tif  and slope.tif

Final dataset used in the study: dem.tif and slope.tif are compreesed in one file  👉 [Download](https://drive.google.com/file/d/1QWDfKUUns6UzAl5zQU3J6j7ba8rO7Iqt/view?usp=sharing)

---

# 2.2.11 NTL

Nighttime light data were obtained using **Google Earth Engine**.

Details listed in the folder "NTL"

Final dataset used in the study: Nighttime_Lights_Tunisia_2020.tif   👉 [Download](https://drive.google.com/file/d/1nDOA5-HVc2mT9du5E-cqIfn_mgDjYw_X/view?usp=sharing)


---

# 2.3 Visualizing and Inspecting the Dataset in ArcGIS Pro

The final dataset (`tunisia10.tif`) is a multi-band raster that can be easily explored using ArcGIS Pro.

### Step 1 — Download the dataset
Download the file from the link below and extract it if necessary.  👉 [Download](https://drive.google.com/file/d/12YaLwfOp-IPpgUMciMzb_lOR_eK4aL5B/view?usp=sharing)


### Step 2 — Open ArcGIS Pro
Launch ArcGIS Pro and create a new project (Map project is sufficient).

### Step 3 — Add the raster dataset
1. In the **Catalog Pane**, click **Folders → Add Folder Connection**.
2. Navigate to the folder containing `tunisia10.tif`.
3. Drag and drop the raster into the map.

Alternatively:
Map → Add Data → Browse to `tunisia10.tif`.

### Step 4 — Inspect the bands
1. Right-click the raster layer.
2. Select **Properties**.
3. Go to the **Source** tab to view:
   - Number of bands
   - Pixel type
   - Spatial resolution
   - Coordinate system.

The dataset contains **10 bands** derived from the original 12 layers.

### Step 5 — Display individual bands
To visualize a specific band:

1. Right-click the layer → **Symbology**.
2. Choose **Singleband Gray** to inspect one band.
3. Select the band index (Band 1–10).

### Step 6 — Create RGB composites
To visualize multiple layers together:

1. Open **Symbology**.
2. Choose **RGB Composite**.
3. Assign bands to Red, Green, and Blue channels.

Example:
- R = Band 4  
- G = Band 3  
- B = Band 2  

This helps visually analyze spatial patterns.

### Step 7 — Extract band values
To inspect pixel values:

1. Go to **Explore Tool**.
2. Click anywhere on the raster.
3. Pixel values for all bands will appear.

### Step 8 — Export or process the raster (optional)
Users can run additional geospatial analysis:

Toolbox → Spatial Analyst → Raster Processing tools such as:
- Clip
- Reproject Raster
- Raster Calculator
- Zonal Statistics

### Notes
- Recommended coordinate system: **WGS84 / UTM Zone 32N (EPSG:32632)**.
- Make sure the raster is fully loaded before running analysis.

- 
---

# 3. popVAT Architecture

The popVAT architecture extends popVAE with a modified deep learning model.

Architecture diagram:

Figure_2_popVAT.png

Detailed explanation:

Model architecture of popVAT/

---

# 4. Training

Training scripts and configuration files are provided in:

Model training of popVAT/

This includes:

- Hyperparameters  
- Model configuration  
- Training procedure  

---

# 5. Evaluation

Evaluation scripts and metrics are provided in:

Evaluation of popVAT/

Includes:

- Testing procedure  
- Metrics  
- Result generation  

---

# Reproducibility

Steps to reproduce the study:

1. Download datasets or use the provided ones.
2. Follow preprocessing instructions inside each folder.
3. Assemble the final dataset.
4. Train the model using provided scripts.
5. Run the evaluation scripts.

All intermediate and final datasets are provided whenever possible to ensure reproducibility.

---

# Citation

If you use this repository, please cite the corresponding publications of **popVAT** and **popVAE**.

---

# License

Specify the license used for this repository.
