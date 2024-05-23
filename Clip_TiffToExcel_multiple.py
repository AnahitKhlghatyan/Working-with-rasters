import os
import rasterio
import rasterio.mask
from collections import defaultdict
import glob
import fiona

rasterfolder = r'C:/Users/Aza/Desktop/M'
shp = 'C:/Users/Aza/Desktop/M/sevan_area.shp'

# Read shapefile
with fiona.open(shp, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

#Add all files to a list
filelist = []
for path, dirc, files in os.walk(rasterfolder):
    for name in files:
        if name.endswith('.tif'):
            fname = os.path.join(path, name)
            with rasterio.open(fname) as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta

                out_meta.update({"driver": "GTiff",
                            "height": out_image.shape[1],
                            "width": out_image.shape[2],
                            "transform": out_transform})

            with rasterio.open(name + '_clip', "w", **out_meta) as dest:
                dest.write(out_image)

            filelist.append(out_image)


# with rasterio.open('C:/Users/Aza/Desktop/M\CHL_eo-sevan_EOMAP_20200203_065537_SENT3_m0300_32bit.tif') as src:
#     out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
#     out_meta = src.meta
#
# out_meta.update({"driver": "GTiff",
#                 "height": out_image.shape[1],
#                 "width": out_image.shape[2],
#                 "transform": out_transform})
#
# with rasterio.open('clip2.tif', "w", **out_meta) as dest:
#     dest.write(out_image)