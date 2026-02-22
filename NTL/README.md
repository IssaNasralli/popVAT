# Nighttime Lights (NTL)

This folder describes how the **Nighttime Lights (NTL)** dataset used in the popVAT study was generated.

Nighttime lights data were processed using **Google Earth Engine (GEE)** and the **VIIRS Day/Night Band monthly composites**.

---

# Dataset Source

VIIRS Nighttime Lights

Provider: NOAA

Dataset ID:

```
NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG
```

Description:

Monthly cloud-free composites of nighttime lights produced from the VIIRS Day/Night Band sensor.

Dataset documentation:

https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG

Spatial resolution:

```
~463 meters
```

---

# Study Area

Country:

```
Tunisia
```

Administrative boundary dataset used:

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

# Processing Overview

The workflow consists of the following steps:

1. Load the GAUL administrative boundaries.
2. Extract the Tunisia boundary.
3. Load VIIRS Nighttime Lights monthly images.
4. Filter images by date and location.
5. Compute a yearly median composite.
6. Export the raster to Google Drive.

---

# Google Earth Engine Script

The following script was used to generate the Nighttime Lights dataset.

```javascript
// Define a function to collect Nighttime Lights images for a given region and year
var CollectNighttimeLightsForRegionAndYear = function(regionName, level, admName, startYear, endYear) {

  // Define region of interest
  var country = ee.FeatureCollection('FAO/GAUL/2015/' + level)
    .filter(ee.Filter.eq(admName, regionName));

  var geometry = country.geometry();

  // Iterate over years
  for (var year = startYear; year <= endYear; year++) {

    var startDate = year + '-01-01';
    var endDate = year + '-12-31';

    // Load VIIRS dataset
    var dataset = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG')
      .filter(ee.Filter.date(startDate, endDate))
      .filterBounds(geometry);

    var nighttime = dataset.select('avg_rad');

    var nighttimeVis = {
      min: 0.0,
      max: 60.0
    };

    // Create median composite
    var medianComposite = nighttime.median();

    // Display layers
    Map.centerObject(geometry, 6);
    Map.addLayer(medianComposite, nighttimeVis,
      'Nighttime Lights - ' + regionName + ' ' + year);

    Map.addLayer(geometry, {color: 'FF0000'}, 'Country Boundary');

    if (regionName === 'Sfax') {
      regionName = 'sfax';
    }

    // Export image
    Export.image.toDrive({
      image: medianComposite,
      description: 'Nighttime_Lights_' + regionName + '_' + year,
      folder: 'Nighttime_Lights_Images',
      fileNamePrefix: 'Nighttime_Lights_' + regionName + '_' + year,
      scale: 463,
      region: geometry,
      crs: 'EPSG:32632',
      maxPixels: 1e13
    });
  }
};

// Run for Tunisia
CollectNighttimeLightsForRegionAndYear(
  'Tunisia',
  'level0',
  'ADM0_NAME',
  2020,
  2020
);
```

---

# Output

The script exports the following raster to Google Drive:

```
Nighttime_Lights_Tunisia_2020.tif
```

This raster represents the **median nighttime light intensity** for Tunisia in 2020.

---

# Final Dataset Used in popVAT

After downloading and aligning with the other datasets, the following file is used in the model:

```
NTL.tif
```

The raster is reprojected and aligned to match the spatial grid used in the final dataset.

---

# Notes for Reproducibility

• Processing performed using Google Earth Engine  
• Dataset: NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG  
• Composite method: median of monthly images  
• Export resolution: 463 m  
• Projection used: EPSG:32632
