# User inputs
path = r'D:\CENS_projects\ML for GEO\Botanical\Clipped'
filename1 = r'Thermal_october_Clip1'
filename2 = r'classified_02_Clip1'

# Name
name_eol1 = filename1
name_eol2 = filename2

# import libraries
import rasterio.mask
import pandas as pd

# read raster
with rasterio.open(path+'/'+filename1+'.tif') as src:
    array1 = src.read(1)

with rasterio.open(path+'/'+filename2+'.tif') as src1:
    array2 = src1.read(1)

# Create excel file from raster
arr1 = pd.DataFrame(array1)
for i in arr1:
    for j in arr1[i]:
        if j == '-3.402823e+38':
            arr1[i] = arr1[i].replace('-3.402823e+38', None)
# print(arr1)

ar1 = (pd.Series(arr1.values.ravel('F'))).reset_index().drop('index', axis=1)
# ar1.to_csv('{}_pixelwise.xlsx'.format(path+'/'+name_eol1))
print(ar1)


arr2 = pd.DataFrame(array2)
for i in arr2:
    for j in arr2[i]:
        if j == 255:
            arr2[i] = arr2[i].replace(255, None)
# print(arr2)

ar2 = (pd.Series(arr2.values.ravel('F'))).reset_index().drop('index', axis=1)
# ar2.to_csv('{}_pixelwise.xlsx'.format(path + '/' + name_eol2))
print(ar2)

df = pd.DataFrame()
df['Class'] = ar2
df['Thermal'] = ar1
print(df)


