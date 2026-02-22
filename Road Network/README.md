Road Network data used in the study (lines shapefile)  are available here: 👉 [Download](https://drive.google.com/file/d/15xiLOmsAcHI7q3TVR2uf9jCzOOxWFTwJ/view?usp=sharing)
# Road Network Processing

This folder contains the workflow used to generate the **road intersection density raster** used as an ancillary variable in the popVAT model.

All operations were performed using **ArcGIS Pro 3**.

The process consists of three main stages:

1. Filtering major roads from OpenStreetMap data  
2. Snapping and cleaning the road network  
3. Calculating road intersection density  

Final output of this folder:

```
road.tif
```

---

# Input Data

Road network shapefile extracted from **OpenStreetMap (OSM)**.

The shapefile must include the attribute describing road type (commonly named `highway`).

Example location in the repository:

```
Road Network/
    roads_osm.shp
```

---

# Software Requirements

ArcGIS Pro 3

Required tools:

• Select By Attributes  
• Export Features  
• Integrate  
• Intersect  
• Point Density  

---

# Step 1 — Filter Major Road Types

### 1. Add Road Network to ArcGIS Pro

1. Open **ArcGIS Pro**.
2. Create a new project or open an existing one.
3. In the **Catalog pane**, locate the road network shapefile.
4. Drag the shapefile onto the map.

---

### 2. Open the Attribute Table

1. Right-click the road network layer in the **Contents pane**.
2. Click **Attribute Table**.

---

### 3. Select Major Roads

1. Go to the **Analysis tab**.
2. Click **Select → Select By Attributes**.
3. Choose the road network layer.

Use the following SQL query:

```
"highway" IN ('motorway', 'primary', 'secondary', 'tertiary')
```

This selects the main road types used in the study.

---

### 4. Export Selected Roads

1. Right-click the road layer.
2. Click **Data → Export Features**.
3. Enable **Selected Features**.
4. Save the output shapefile.

Example output:

```
major_roads.shp
```

---

# Step 2 — Snap and Clean Road Network

This step removes gaps and ensures that road intersections are correctly connected.

### 1. Prepare Data

Add the filtered road network (`major_roads.shp`) to the project.

---

### 2. Enable Snapping

1. Go to the **Edit tab**.
2. Open **Snapping**.
3. Enable snapping.

---

### 3. Configure Snapping Settings

Open **Snapping Settings** and enable:

• Vertex  
• Edge  
• End

---

### 4. Run the Integrate Tool

1. Open **Analysis → Tools**.
2. Search for **Integrate**.

Set parameters:

Input Features  
```
major_roads.shp
```

Cluster Tolerance  
```
Define according to dataset precision
```

This operation snaps nearby road segments together to ensure proper connectivity.

---

# Step 3 — Generate Intersection Points

Road intersections are required to compute density.

Use the **Intersect Tool**.

Steps:

1. Open **Analysis → Tools**.
2. Search for **Intersect**.
3. Select the road network layer as input.
4. Run the tool.

Output:

```
road_intersections.shp
```

---

# Step 4 — Calculate Intersection Density

### Open Point Density Tool

1. Go to **Analysis → Tools**.
2. Search for **Point Density**.

---

### Parameters

Input Point Features

```
road_intersections.shp
```

Population Field

```
None
```

Output Raster

```
road.tif
```

Cell Size

```
100
```

Neighborhood

Shape  
```
Circle
```

Radius  

```
500
```

Units  

```
Map Units (meters)
```

Area Units  

Square kilometers or square meters depending on the project settings.

---

# Output

The final dataset produced is:

```
road.tif
```

This raster represents **road intersection density**, which is used as an input feature for the popVAT model.

---

# Notes for Reproducibility

• The road network originates from OpenStreetMap.  
• Only major road types were used in the study.  
• Snapping ensures intersections are properly connected.  
• The density parameters (100 m cell size and 500 m radius) were selected to represent urban accessibility.

---

# Next Processing Step

This dataset is later combined with other ancillary datasets to build the final input raster used in the popVAT model.
