import os
import glob
import rasterio
from rasterio.features import geometry_mask
import geopandas as gpd
import numpy as np
import pandas as pd


# Load the grid shapefile
grid_shapefile_path = r'D:\CENS_projects\SEVAMOD\Data__new_S3_project\grid_10.shp' #Change to your grid path and name
grid_gdf = gpd.read_file(grid_shapefile_path)

raster_folder = r'D:\CENS_projects\SEVAMOD\Data__new_S3_project\2022_July_Chl' #Change to your folder containing all rasters that you need
raster_files = glob.glob(os.path.join(raster_folder, '*.tif'))



def zonal_stats(grid_gdf, raster_path, nodata=-9999):
    with rasterio.open(raster_path) as src:
        # Read the raster data and transform the coordinates
        raster_array = src.read(1)
        raster_affine = src.transform

    # Use the geometry_mask function to create a mask for each polygon
    stats = []
    for idx, row in grid_gdf.iterrows():
        mask = geometry_mask(
            [row.geometry],
            out_shape=raster_array.shape,
            transform=raster_affine,
            invert=True,
            # filled=True,
            all_touched=False
        )

        # Extract the raster values within the polygon using the mask, excluding NoData values
        masked_raster = raster_array[mask]
        masked_raster = masked_raster[masked_raster != nodata]

        count = masked_raster.size

        # Check if the masked_raster array is empty
        if count > 0:
            # Calculate the statistics
            mean = np.mean(masked_raster)
            median = np.median(masked_raster)
            min = np.min(masked_raster)
            max = np.max(masked_raster)
        else:
            # Set statistics to NaN (or another value) if the polygon contains no valid data
            mean = median = min = max = np.nan

        stats.append([count, mean, median, min, max])

    return stats


results = []

for raster_path in raster_files:
    raster_name = os.path.basename(raster_path)
    stats = zonal_stats(grid_gdf, raster_path)

    # Append the results to the list
    for i, row in enumerate(stats):
        results.append([i, raster_name] + row)

# Convert the results to a pandas DataFrame
results_df = pd.DataFrame(
    results,
    columns=['polygon_id', 'raster_name', 'count', 'mean', 'median', 'min', 'max']
)

print(results_df)

results_df.to_excel(r'D:\CENS_projects\SEVAMOD\Data__new_S3_project\2022_July_Chl\zonal_box10.xlsx', index=False) #Write path and excel name here
