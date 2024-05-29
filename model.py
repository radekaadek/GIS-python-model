import geopandas as gpd
import pandas as pd
from osgeo import gdal
gdal.DontUseExceptions()
import os

# Load the data
pomniki = gpd.read_file('PomnikiPrzyrodyPoint.shp')
rezerwaty = gpd.read_file('PomnikiPrzyrodyPoint.shp')
# Get pomniki inside rezerwaty
pomniki_rezerwaty = gpd.sjoin(pomniki, rezerwaty, how='left', predicate='within')
# Create a buffer around pomniki
tree_buffer, glaz_buffer = 10, 5
trees = pomniki_rezerwaty[pomniki_rezerwaty['obiekt_left'] == 'drzewo'].copy()
trees['geometry'] = trees.buffer(tree_buffer)
glazy = pomniki_rezerwaty[pomniki_rezerwaty['obiekt_left'] == 'g³az narzutowy'].copy()
glazy['geometry'] = glazy.buffer(glaz_buffer)
# Join the buffers into one GeoDataFrame by joining the geometries
buffers = pd.concat([trees, glazy])
# Join the rows by geometries
buffers = buffers.dissolve()
# Save to a wkb and rasterize with gdal
shp_file = 'buffers.shp'
buffers.to_file(shp_file)
raster = 'buffer.tif'
rasterize = gdal.Rasterize(raster, shp_file, format='GTiff', outputType=gdal.GDT_Byte, xRes=10, yRes=10)
# remove all that starts with buffer
for f in os.listdir():
    if f.startswith('buffers'):
        os.remove(f)

