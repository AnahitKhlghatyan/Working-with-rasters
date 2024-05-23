# User inputs
path = r'D:\CENS_projects\ML for GEO\Mapping_rasters_new'

# import libraries
import rasterio
import rasterio.mask
import numpy as np
import pandas as pd
import geopandas as gpd
import fiona
import subprocess
import os
import matplotlib.pyplot as plt

# read raster
lst = []
name_lst = []
for path, dirc, files in os.walk(path):
    for name in files:
        if name.endswith('.tif'):
            fname = os.path.join(path, name)
            name_eol = name
            name_lst.append(name_eol)
            with rasterio.open(fname) as src:
                array = src.read(1)
                lst.append(array)
print(name_lst)
# Convert to excel
ar_lst = []
for i in lst:
    arr = pd.DataFrame(i)
    arr = arr.values.ravel('F')
    arr = pd.DataFrame(arr)
    arr = arr.loc[~(arr[0] ==-9999.0)].reset_index().drop('index', axis=1)
    ar_lst.append(arr)

df = pd.DataFrame()
for i in range(len(ar_lst)):
    df['{}'.format(name_lst[i])] = ar_lst[i]
# df = df.T
print(df)

# df.to_csv(r'\\10.1.27.3\share\Eolytics_Sevan\2017\CHL\2017.csv')