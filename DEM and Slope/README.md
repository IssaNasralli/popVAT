# DEM and Slope Dataset

This folder describes the procedure used to generate the **Digital Elevation Model (DEM)** and **Slope** datasets used as ancillary variables in the popVAT model.

The datasets were produced using **Google Earth Engine (GEE)** and the **SRTM DEM dataset**.

---

# Dataset Source

SRTM Global Digital Elevation Model

Provider: USGS / NASA

Dataset ID:

```
USGS/SRTMGL1_003
```

Spatial Resolution:

```
30 meters
```

Reference:

https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003

---

# Study Area

Country:

```
Tunisia
```

Administrative boundaries were obtained from:

```
FAO/GAUL/2015
```

---

# Processing Platform

Processing was performed using:

```
Google Earth Engine (JavaScript API)
https://code.earthengine.google.com/
```

---

# Workflow Overview

1. Load GAUL administrative boundaries.
2. Extract Tunisia boundary.
3. Load SRTM DEM dataset.
4. Clip DEM to Tunisia.
5. Compute terrain slope.
6. Export DEM and slope rasters.

---

# Google Earth Engine Script

The following script was used to generate the datasets.

```javascript
// Load the GAUL dataset
var gaul = ee.FeatureCollection("FAO/GAUL/2015/level0");

// Filter Tunisia
var tunisia = gaul.filter(ee.Filter.eq('ADM0_NAME', 'Tunisia'));

// Load SRTM DEM
var srtm = ee.Image("USGS/SRTMGL1_003");

// Clip DEM
var demTunisia = srtm.clip(tunisia);

// Display DEM
Map.centerObject(tunisia, 7);
Map.addLayer(
  demTunisia,
  {min: 0, max: 3000, palette: ['blue', 'green', 'yellow', 'brown', 'white']},
  'SRTM DEM Tunisia'
);

// Compute slope
var slopeTunisia = ee.Terrain.slope(demTunisia);

// Display slope
Map.addLayer(
  slopeTunisia,
  {min: 0, max: 60, palette: ['00FFFF', '008000', 'FFFF00', 'FFA500', 'FF0000']},
  'Slope Tunisia'
);

// Export DEM
Export.image.toDrive({
  image: demTunisia,
  description: 'SRTM_DEM_Tunisia',
  scale: 30,
  region: tunisia.geometry(),
  fileFormat: 'GeoTIFF',
  maxPixels: 1e9
});

// Export slope
Export.image.toDrive({
  image: slopeTunisia,
  description: 'SRTM_Slope_Tunisia',
  scale: 30,
  region: tunisia.geometry(),
  fileFormat: 'GeoTIFF',
  maxPixels: 1e9
});
```

---

# Output Files

The script exports the following rasters:

```
SRTM_DEM_Tunisia.tif
SRTM_Slope_Tunisia.tif
```

These files represent:

• Elevation (DEM)  
• Terrain slope derived from the DEM

---

# Final Files Used in popVAT

After download and alignment with the project dataset:

```
dem.tif
slope.tif
```

Both rasters were reprojected and aligned with the spatial grid used for the final dataset.

---

# Notes for Reproducibility

• Processing was done entirely in Google Earth Engine  
• Export resolution must remain **30 meters**  
• Region must correspond exactly to the **Tunisia GAUL boundary**  
• Output rasters should be aligned with other input layers before training the model
