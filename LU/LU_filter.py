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

# Create a spatial index for the reprojected layer
print("Creating a spatial index for the reprojected layer")
arcpy.management.AddSpatialIndex("Tunisia_all_poly_reprojected")

# Define the reprojected building layer for use in your program
building_layer = "Tunisia_all_poly_reprojected"

# Create feature layer outside the loop
print("Creating feature layer")
arcpy.MakeFeatureLayer_management(building_layer, "building_layer")

# Define a query to select non-residential buildings based on specified tags
print("Defining a query to select non-residential buildings")
query = """ "amenity" IN ('school', 'hospital', 'university', 'place_of_worship', 'theatre', 'library', 'restaurant', 
                        'cafe', 'bank', 'shopping_center', 'marketplace', 'community_centre', 'police', 'fire_station', 
                        'public_building') OR "building_m" IN ('office', 'industrial', 'retail', 'commercial') 
                        OR "office" IN ('government', 'company', 'administrative') """

# Apply the query to select non-residential buildings
print("Applying the query to select non-residential buildings")
arcpy.SelectLayerByAttribute_management("building_layer", "NEW_SELECTION", query)

# Create a temporary directory for intermediate files
temp_dir = os.path.join(arcpy.env.scratchFolder, "temp_rasters")
os.makedirs(temp_dir, exist_ok=True)

# Rasterize the selected polygons to match the raster resolution and extent
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

# Check if the rasterization was successful and the file exists
if not arcpy.Exists(polygon_raster):
    raise RuntimeError(f"Rasterization failed or file not created: {polygon_raster}")

print(f"Raster file {polygon_raster} created successfully")

#then please apply this condition on rastor calculator to create a mask of 0 and 1 non_residential_buildings0or1.tif:
#Con(IsNull("non_residential_buildings.tif"), 1, Con("non_residential_buildings.tif" > 7422, 0, 1))
#then please apply this condition on raster calculator to create Tunisia_floor_WSF2019_WGS_84_32N_0to1_residentiel.tif:
#"non_residential_buildings0or1.tif" * "Tunisia_floor_WSF2019_WGS_84_32N_0to1.tif"
#then please don't forget to use clip raster based on Tunisia_floor_WSF2019_WGS_84_32N_0to1_residentiel_final.tif
