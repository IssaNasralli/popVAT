LU data used in the study (polygons shapefile)  are available here: 👉 [Download](https://drive.google.com/file/d/15xiLOmsAcHI7q3TVR2uf9jCzOOxWFTwJ/view?usp=sharing)


# Land Use (LU) Processing

This folder contains the data and instructions used to generate the **non-residential building mask** used in the popVAT study.

The processing workflow was performed using **ArcGIS Pro 3** and a Python script.

---

# 1. Input Data

The following datasets are required:

Building polygons extracted from OpenStreetMap (OSM)

Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif  
(Building floor dataset derived from WSF2019)

Make sure that all datasets are located in the same working directory or that the paths in the script are updated accordingly.

---

# 2. Software Requirements

ArcGIS Pro 3  
Python environment provided with ArcGIS (ArcPy)

Required Python libraries:

arcpy  
numpy  
os

---

# 3. Python Script

Use the file LU_filter.py


---

# 4. Create Non-Residential Mask

Open **Raster Calculator** in ArcGIS Pro and apply the following expression:

```
Con(IsNull("non_residential_buildings.tif"), 1, Con("non_residential_buildings.tif" > 7422, 0, 1))
```

Output file:

```
non_residential_buildings0or1.tif
```

This raster represents:

1 → residential or unknown  
0 → non-residential

---

# 5. Extract Residential Buildings

Use Raster Calculator again:

```
"non_residential_buildings0or1.tif" * "Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif"
```

Output:

```
Tunisia_floor_WSF2019_WGS_84_32N_0to1_residentiel.tif
```

---

# 6. Final Step – Clip Raster

Clip the raster using the Tunisia study area boundary to produce:

```
Tunisia_floor_WSF2019_WGS_84_32N_0to1_residentiel_final.tif
```

Tool:

ArcGIS Pro → Clip Raster

---

# 7. Output Files

The final outputs used in the study are:

```
non_residential_buildings0or1.tif
Tunisia_floor_WSF2019_WGS_84_32N_0to1_residentiel.tif
Tunisia_floor_WSF2019_WGS_84_32N_0to1_residentiel_final.tif
```

---

# 8. Notes for Reproducibility

• Ensure all datasets share the same projection  
• The building polygons must be reprojected to match the raster coordinate system  
• Spatial indexing improves processing speed  
• Raster cell size must match the WSF dataset resolution
