# Building Foot Print Processing

This folder contains the scripts used to generate the **building footprint layer** used in the popVAT study.

The workflow combines:

• WSF3D Building Volume  
• WSF2019 settlement layer  
• ArcGIS Pro processing

All operations were performed using **ArcGIS Pro 3 with ArcPy**.

The final product generated here is later used in the **LU folder workflow**.

---

# Overview of the Workflow

1. Clip the WSF3D Building Volume to Tunisia and estimate building floors.
2. Reproject the WSF2019 dataset to the working coordinate system.
3. Normalize the WSF2019 dataset.
4. Combine the normalized WSF dataset with estimated building floors.

Final output produced in this folder:

```
Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif
```

Further processing continues in the **LU folder**.

---

# Software Requirements

ArcGIS Pro 3  
Spatial Analyst Extension  
Python environment included with ArcGIS (ArcPy)

Python libraries used:

```
arcpy
os
numpy
```

---

# Input Data

Required datasets:

WSF3D Building Volume  
WSF2019 settlement dataset  
Tunisia boundary shapefile

Example structure:

```
data
 ├── raw
 │    ├── GeoTif
 │    │     WSF3D_V02_BuildingVolume.tif
 │    │     Tunisia_WSF2019.tif
 │    └── shapefile
 │          Tunisia_Boundary.shp
```

---

# Step 1 — Clip Building Volume and Estimate Floors

Script:

```
clip_building_volume.py
```

Purpose:

• Clip WSF3D dataset to Tunisia  
• Estimate number of floors  

Assumption:

Average floor height = **3 meters**

Code:

```python
import arcpy

raster_tif = r"F:\Projects_tunisia\data\raw\GeoTif\WSF3D_V02_BuildingVolume.tif"

arcpy.env.workspace = r"F:\Projects_tunisia\ArcGIS\Building"

boundary_shapefile = r"F:\Projects_tunisia\data\raw\shapefile\boundaries\Tunisia\Tunisia_Boundary.shp"

output_clipped_raster = r"F:\Projects_tunisia\ArcGIS\Building\Tunisia_floor.tif"

clipped_raster = arcpy.sa.ExtractByMask(raster_tif, boundary_shapefile)

clipped_raster = clipped_raster / 4000 / 3

clipped_raster.save(output_clipped_raster)

print("Clipping and processing completed successfully.")
```

Output:

```
Tunisia_floor.tif
```

---

# Step 2 — Reproject WSF2019 Dataset

Script:

```
reproject_wsf.py
```

Purpose:

Convert dataset to **WGS84 UTM Zone 32N**

Code:

```python
import arcpy
arcpy.env.workspace = r"F:\Projects_tunisia\ArcGIS\Building"

target_cs = arcpy.SpatialReference(32632)
source_cs = arcpy.SpatialReference(4326)

worldpop_path = r"F:\Projects_tunisia\data\raw\GeoTif\Tunisia_WSF2019.tif"

reprojected_worldpop = worldpop_path.replace(".tif", "_WGS_84_32N.tif")

arcpy.ProjectRaster_management(
    in_raster=worldpop_path,
    out_raster=reprojected_worldpop,
    out_coor_system=target_cs
)
```

Output:

```
Tunisia_WSF2019_WGS_84_32N.tif
```

---

# Step 3 — Normalize WSF2019 Dataset

Script:

```
normalize_wsf.py
```

Purpose:

• Normalize raster values  
• Handle large rasters by tiling  
• Mosaic tiles back together

Code:

```python
import arcpy
from arcpy.sa import *
import os

arcpy.env.workspace = r"F:\Projects_tunisia\ArcGIS\Building"
arcpy.env.overwriteOutput = True

arcpy.CheckOutExtension("Spatial")

input_raster = r"F:\Projects_tunisia\data\raw\GeoTif\Tunisia_WSF2019_WGS_84_32N.tif"

temp_workspace = r"F:\Projects_tunisia\ArcGIS\Building\temp"

if not arcpy.Exists(temp_workspace):
    arcpy.CreateFolder_management(arcpy.env.workspace, "temp")

output_raster = r"F:\Projects_tunisia\ArcGIS\Building\Tunisia_WSF2019_WGS_84_32N_0To1.tif"

def normalize_raster(in_raster, out_raster):
    float32_raster = Float(in_raster)
    float32_raster = SetNull(float32_raster == float32_raster.noDataValue, float32_raster)
    normalized_raster = (float32_raster - float32_raster.minimum) / (float32_raster.maximum - float32_raster.minimum)
    normalized_raster.save(out_raster)

num_tiles = 4
raster = arcpy.Raster(input_raster)
tile_width = raster.extent.width / num_tiles
tile_height = raster.extent.height / num_tiles

normalized_tiles = []

for i in range(num_tiles):
    for j in range(num_tiles):

        xmin = raster.extent.XMin + i * tile_width
        ymin = raster.extent.YMin + j * tile_height
        xmax = xmin + tile_width
        ymax = ymin + tile_height

        tile_raster = os.path.join(temp_workspace, f"tile_{i}_{j}.tif")

        arcpy.management.Clip(
            in_raster=input_raster,
            rectangle=f"{xmin} {ymin} {xmax} {ymax}",
            out_raster=tile_raster
        )

        normalized_tile = os.path.join(temp_workspace, f"normalized_tile_{i}_{j}.tif")

        normalize_raster(tile_raster, normalized_tile)

        normalized_tiles.append(normalized_tile)

arcpy.management.MosaicToNewRaster(
    input_rasters=normalized_tiles,
    output_location=os.path.dirname(output_raster),
    raster_dataset_name_with_extension=os.path.basename(output_raster),
    pixel_type="32_BIT_FLOAT",
    number_of_bands=1,
    mosaic_method="BLEND"
)

arcpy.Delete_management(temp_workspace)
```

Output:

```
Tunisia_WSF2019_WGS_84_32N_0To1.tif
```

---

# Step 4 — Combine Floors with WSF Dataset

Script:

```
combine_layers.py
```

Purpose:

Weight the WSF settlement layer by the estimated number of building floors.

Code:

```python
import arcpy
arcpy.env.workspace = r"F:\Projects_tunisia\ArcGIS\Building"

Tunisia_floor = "Tunisia_floor_WGS_84_32N.tif"
Tunisia_WSF2019_0to1 = "Tunisia_WSF2019_WGS_84_32N_0To1.tif"

Tunisia_floor_WSF2019_0to1 = "Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif"

arcpy.CheckOutExtension("Spatial")

Tunisia_floor_raster = arcpy.Raster(Tunisia_floor)
Tunisia_WSF2019_0to1_raster = arcpy.Raster(Tunisia_WSF2019_0to1)

Tunisia_floor_WSF2019_0to1_raster = arcpy.sa.Times(
    Tunisia_floor_raster,
    Tunisia_WSF2019_0to1_raster
)

Tunisia_floor_WSF2019_0to1_raster.save(Tunisia_floor_WSF2019_0to1)

print("Weighted raster file created successfully.")
```

Output:

```
Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif
```

---

# Final Output of this Folder

```
Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif
```

This raster represents:

Estimated building floors × normalized settlement probability.

The next processing steps are described in the **LU folder**.

---

# Notes

• Ensure all rasters share the same projection  
• Spatial Analyst extension must be enabled  
• Processing large rasters may require significant RAM  
• Temporary tiles are used to avoid memory issues
