# Satellite Imagery Processing

This folder contains the workflow used to generate the **satellite imagery dataset** used as an input variable for the popVAT model.

The dataset was created using **Google Earth Engine (GEE)** and the **MODIS MCD43A4 product**.

Final output generated from this process:

```
MODIS.tif
```

---

# Data Source

Satellite imagery was obtained from the following dataset:

MODIS Nadir BRDF-Adjusted Reflectance (NBAR)  
Collection: MODIS/061/MCD43A4  
Spatial Resolution: 500 meters

Dataset documentation:

https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD43A4

---

# Platform

Google Earth Engine

Code language:

JavaScript

You can run the script in the **GEE Code Editor**:

https://code.earthengine.google.com/

---

# Processing Overview

The workflow performs the following operations:

1. Define Tunisia as the region of interest using GAUL boundaries.
2. Collect MODIS imagery for the selected year.
3. Select spectral bands used in the study.
4. Build a median composite.
5. Export the dataset.

---

# Selected MODIS Bands

The following reflectance bands were used:

Band 1 – Red  
Band 3 – Blue  
Band 4 – Green  

These bands allow the generation of a **true color composite**.

---

# Google Earth Engine Script

```javascript
// Define a function to collect MODIS images for a given region and year
var CollectMODISForRegionAndYear = function(regionName, level, admName, startYear, endYear) {

  var country = ee.FeatureCollection('FAO/GAUL/2015/' + level)
    .filter(ee.Filter.eq(admName, regionName));

  var roi = country.geometry();

  var modisCollection = ee.ImageCollection([]);

  for (var year = startYear; year <= endYear; year++) {

    var startDate = year + '-01-01';
    var endDate = year + '-12-31';

    var dataset = ee.ImageCollection('MODIS/061/MCD43A4')
      .filter(ee.Filter.date(startDate, endDate))
      .select([
        'Nadir_Reflectance_Band1',
        'Nadir_Reflectance_Band4',
        'Nadir_Reflectance_Band3'
      ])
      .filterBounds(roi);

    modisCollection = modisCollection.merge(dataset);
  }

  var medianComposite = modisCollection.median();

  var trueColorVis = {
    min: 0.0,
    max: 4000.0,
    gamma: 1.4,
  };

  Map.centerObject(roi, 6);
  Map.addLayer(medianComposite, trueColorVis, 'MODIS Median Composite - ' + regionName);
  Map.addLayer(roi, { color: 'FF0000' }, 'Region of Interest');

  Export.image.toDrive({
    image: medianComposite,
    description: 'MODIS_Median_Composite_' + regionName,
    folder: 'MODIS_Images',
    fileNamePrefix: 'modis_median_composite_' + regionName,
    scale: 500,
    region: roi,
    crs: 'EPSG:32632',
    maxPixels: 1e13
  });
};

// Run the function
CollectMODISForRegionAndYear('Tunisia', 'level0', 'ADM0_NAME', 2020, 2020);
```

---

# How to Run the Code

1. Open Google Earth Engine Code Editor.
2. Create a new script.
3. Paste the code above.
4. Click **Run**.
5. Start the export task in the **Tasks panel**.

The output will be exported to your **Google Drive**.

---

# Output

After downloading the exported image from Google Drive, rename it as:

```
MODIS.tif
```

This raster represents the **median MODIS composite for Tunisia**.

---

# Notes

• Spatial resolution: 500 meters  
• Projection used during export: EPSG:32632 (WGS84 UTM Zone 32N)  
• Median compositing reduces cloud contamination and noise.

---

# Role in the popVAT Model

This satellite imagery layer is used as an **ancillary variable** to capture land surface characteristics related to population distribution.
