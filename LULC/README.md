# LULC Dataset Generation

This folder contains the workflow used to generate the **Land Use / Land Cover (LULC)** dataset used in the popVAT study.

The dataset was produced using **Google Earth Engine (GEE)** and the **Dynamic World dataset**.

---

# Dataset Source

Dynamic World Land Cover

Provider: Google  
Dataset ID:

```
GOOGLE/DYNAMICWORLD/V1
```

Resolution:

```
10 meters
```

Reference:

https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1

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

# Time Period

The dataset was generated for the following year:

```
2020
```

---

# Processing Platform

All processing was performed using:

```
Google Earth Engine (JavaScript API)
https://code.earthengine.google.com/
```

---

# Workflow Overview

1. Define the study area using GAUL boundaries.
2. Filter Dynamic World images by year.
3. Create yearly composites using the mode reducer.
4. Export the final raster to Earth Engine assets.
5. Download and integrate into the project dataset.

---

# Google Earth Engine Script

The following script was used to generate the dataset.

```javascript
// Define a function to stack images for a given region and year
var CollectImagesForRegionAndYear = function(regionName, level, admName, startYear, endYear) {

  // Define region of interest
  var country = ee.FeatureCollection('FAO/GAUL/2015/' + level)
    .filter(ee.Filter.eq(admName, regionName));

  var geometry = country.geometry();
  var roi = country.geometry();

  // Iterate over years
  for (var year = startYear; year <= endYear; year++) {

    var startDate = year + '-01-01';
    var endDate = year + '-12-31';

    // Load Dynamic World data
    var dw = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
                 .filterDate(startDate, endDate)
                 .filterBounds(geometry);

    var classification = dw.select('label');

    var dwComposite = classification.reduce(ee.Reducer.mode());

    var dwVisParams = {
      min: 0,
      max: 8,
      palette: [
        '#419BDF', '#397D49', '#88B053', '#7A87C6',
        '#E49635', '#DFC35A', '#C4281B', '#A59B8F', '#B39FE1'
      ]
    };

    Map.addLayer(dwComposite.clip(geometry), dwVisParams,
      'Classified Composite - ' + regionName + ' ' + year);

    if (regionName === 'Sfax') {
      regionName = 'sfax';
    }

    // Export to GEE assets
    Export.image.toAsset({
      image: dwComposite,
      description: 'DynamicWorld_' + regionName + '_' + year,
      assetId: 'users/aissanasralli/' + regionName + '/' + year + '/original/DynamicWorld_' + regionName + '_' + year,
      scale: 10,
      region: geometry,
      maxPixels: 1e13
    });
  }
};

// Run for Tunisia
CollectImagesForRegionAndYear('Tunisia', 'level0', 'ADM0_NAME', 2016, 2020);
```

---

# Output

The script exports yearly LULC rasters to **Google Earth Engine assets**.

Example outputs:

```
DynamicWorld_Tunisia_2016
DynamicWorld_Tunisia_2017
DynamicWorld_Tunisia_2018
DynamicWorld_Tunisia_2019
DynamicWorld_Tunisia_2020
```

These rasters represent the **most frequent land cover class per pixel** for each year.

---

# Land Cover Classes

Dynamic World includes the following classes:

| Value | Class |
|------|------|
| 0 | Water |
| 1 | Trees |
| 2 | Grass |
| 3 | Flooded Vegetation |
| 4 | Crops |
| 5 | Shrub & Scrub |
| 6 | Built Area |
| 7 | Bare Ground |
| 8 | Snow & Ice |

---

# Final Dataset Used in popVAT

After exporting the rasters from Google Earth Engine, the dataset was downloaded and prepared for integration with the other ancillary variables.

Final file used in the model:

```
LULC.tif
```

This raster was aligned with the spatial resolution and projection used for the final dataset.

---

# Notes for Reproducibility

• Processing was performed entirely in Google Earth Engine  
• Ensure the same **region definition and years** are used  
• Export scale must remain **10 meters**  
• Output rasters must be reprojected and aligned with the main dataset before use
