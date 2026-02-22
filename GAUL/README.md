# GAUL – Administrative Boundaries Processing

This folder contains the workflow used to obtain and process the **administrative boundaries of Tunisia** used in the popVAT study.

The boundaries are required to:

• Define the study area  
• Extract Tunisia from global datasets  
• Create masks for each governorate  
• Aggregate predicted population values per governorate for evaluation against official census data (INS)

Data source:

FAO Global Administrative Unit Layers (GAUL)

Dataset in Google Earth Engine:

```
FAO/GAUL/2015
```

---

# Software Used

Google Earth Engine (JavaScript API)  
ArcGIS Pro 3  
ArcPy (Spatial Analyst)

---

# Overview of the Workflow

1. Download Tunisia administrative boundaries from Google Earth Engine
2. Export the 24 governorates shapefile
3. Convert each governorate into a raster mask
4. Use the masks to aggregate population estimates

Final outputs:

```
Tunisia_Regions_Project.shp
Tunisia_Region_0.tif
Tunisia_Region_1.tif
...
Tunisia_Region_23.tif
```

Each raster represents a **binary mask** for one governorate.

---

# Step 1 — Extract Tunisia Boundary (Google Earth Engine)

This step retrieves the Tunisia administrative dataset from GAUL.

### GEE Script

```javascript
// Define a region of interest for Tunisia
var tunisiaRegions = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM0_NAME', 'Tunisia'));

// Specify export folder
var exportPath = 'tunisiaRegions';

// Display on the map
Map.addLayer(tunisiaRegions, {color: 'FF0000'}, 'Tunisia Administrative Regions');

// Zoom to Tunisia
Map.centerObject(tunisiaRegions, 6);

// Export to Google Drive
Export.table.toDrive({
  collection: tunisiaRegions,
  description: 'Tunisia_Regions',
  folder: exportPath,
  fileFormat: 'SHP'
});
```

Output:

```
Tunisia_Regions.shp
```

This shapefile contains the **24 Tunisian governorates**.

---

# Step 2 — Verify the 24 Governorates

The exported dataset corresponds to:

```
FAO/GAUL/2015/level1
```

Which represents **first administrative level boundaries**.

For Tunisia this equals:

```
24 governorates
```

These polygons are used for model evaluation.

---

# Step 3 — Project the Shapefile

Before rasterization, the shapefile must be projected to the same coordinate system used by the population dataset.

Example output:

```
Tunisia_Regions_Project.shp
```

Projection must match the population raster used in the model.

---

# Step 4 — Create Governorate Masks

Each governorate polygon is converted into a raster mask.

These masks allow population values to be aggregated per administrative unit.

### Python Script (ArcPy)

```python
import arcpy
import os

script_dir = "F:\\A Projects_tunisia\\ArcGIS\\MAsk"

pop_tif_path = os.path.join(script_dir, "POP.tif")

desc = arcpy.Describe(pop_tif_path)
pop_extent = desc.extent
pop_cellsize = desc.meanCellWidth

arcpy.env.workspace = script_dir
arcpy.env.overwriteOutput = True
arcpy.env.extent = pop_extent
arcpy.env.cellSize = pop_cellsize

in_features = os.path.join(script_dir, "Tunisia_Regions_Project.shp")

if not arcpy.Exists(in_features):
    raise FileNotFoundError(f"The shapefile {in_features} does not exist.")

output_dir = os.path.join(script_dir, "Tunisia_Regions")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for district_id in range(24):

    try:

        sql_expression = f"FID = {district_id}"

        temp_layer = f"temp_layer_{district_id}"

        arcpy.management.MakeFeatureLayer(in_features, temp_layer, sql_expression)

        out_raster = os.path.join(output_dir, f"Tunisia_Region_{district_id}.tif")

        if arcpy.Exists(out_raster):
            arcpy.management.Delete(out_raster)

        temp_raster = os.path.join(output_dir, f"temp_{district_id}.tif")

        arcpy.conversion.PolygonToRaster(
            temp_layer,
            "FID",
            temp_raster,
            "CELL_CENTER",
            "",
            pop_cellsize
        )

        con_result = arcpy.sa.Con(arcpy.sa.Raster(temp_raster) >= 0, 1)

        con_result.save(out_raster)

        arcpy.management.Delete(temp_raster)

        print(f"Mask created for District {district_id}")

    except Exception as e:
        print(f"Error processing District {district_id}: {e}")

    finally:
        if arcpy.Exists(temp_layer):
            arcpy.management.Delete(temp_layer)

print("All districts processed.")
```

---

# Output Masks

The script produces 24 rasters:

```
Tunisia_Region_0.tif
Tunisia_Region_1.tif
...
Tunisia_Region_23.tif
```

Each raster contains:

```
1 = inside governorate
0 / NoData = outside
```

These masks are aligned with the population raster grid.

---

# Purpose in the popVAT Study

The masks are used to:

1. Sum predicted population per governorate
2. Compare results with official census data from **INS**
3. Evaluate model accuracy at administrative level

---

# Notes for Reproducibility

• GAUL version used: **2015**  
• Administrative level: **Level 1 (Governorates)**  
• All rasters must match the population raster extent and resolution  
• Cell size and extent are derived from `POP.tif`

---

# Final Folder Structure

Example structure:

```
GAUL
 ├── Tunisia_Regions.shp
 ├── Tunisia_Regions_Project.shp
 └── Tunisia_Regions
      ├── Tunisia_Region_0.tif
      ├── Tunisia_Region_1.tif
      └── ...
```
