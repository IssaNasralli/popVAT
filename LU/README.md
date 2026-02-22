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

Run the following script:

LU_filter.py

```
import arcpy
import numpy as np
import os

# Convert raster to NumPy array
print("Converting raster to NumPy array")
raster = "Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif"
arr = arcpy.RasterToNumPyArray(raster)

# Get raster properties
print("Getting raster properties")
desc = arcpy.Describe(raster)
origin_x = desc.extent.XMin
origin_y = desc.extent.YMin
cell_size_x = desc.meanCellWidth
cell_size_y = desc.meanCellHeight
raster_spatial_ref = desc.spatialReference

# Reproject the building polygon layer if necessary
print("Reprojecting the building polygon layer")
#arcpy.management.Project("Tunisia_all_poly", "Tunisia_all_poly_reprojected", raster_spatial_ref)

# Create a spatial index
print("Creating a spatial index for the reprojected layer")
arcpy.management.AddSpatialIndex("Tunisia_all_poly_reprojected")

# Define building layer
building_layer = "Tunisia_all_poly_reprojected"

# Create feature layer
print("Creating feature layer")
arcpy.MakeFeatureLayer_management(building_layer, "building_layer")

# Query for non-residential buildings
print("Defining a query to select non-residential buildings")
query = """ "amenity" IN ('school', 'hospital', 'university', 'place_of_worship', 'theatre', 'library', 'restaurant', 
                        'cafe', 'bank', 'shopping_center', 'marketplace', 'community_centre', 'police', 'fire_station', 
                        'public_building') OR "building_m" IN ('office', 'industrial', 'retail', 'commercial') 
                        OR "office" IN ('government', 'company', 'administrative') """

# Apply query
print("Applying the query")
arcpy.SelectLayerByAttribute_management("building_layer", "NEW_SELECTION", query)

# Temporary directory
temp_dir = os.path.join(arcpy.env.scratchFolder, "temp_rasters")
os.makedirs(temp_dir, exist_ok=True)

# Rasterize polygons
print("Rasterizing the selected polygons")
polygon_raster = os.path.join(temp_dir, "non_residential_buildings.tif")

arcpy.conversion.PolygonToRaster(
    in_features="building_layer",
    value_field="FID",
    out_rasterdataset=polygon_raster,
    cell_assignment="MAXIMUM_AREA",
    priority_field="NONE",
    cellsize=cell_size_x
)

if not arcpy.Exists(polygon_raster):
    raise RuntimeError(f"Rasterization failed or file not created: {polygon_raster}")

print(f"Raster file {polygon_raster} created successfully")
```

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
