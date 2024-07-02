# -*- coding: utf-8 -*-

from osgeo import gdal
import os, shutil, zipfile, argparse
import numpy as np

#%%
def UnzipData(path,folderpath):

    if os.path.isdir(folderpath):
        shutil.rmtree(folderpath)
    
    #print folderpath
    os.makedirs(folderpath)
    #print path
    with zipfile.ZipFile(path, "r") as z:
        z.extractall(folderpath)
    
  
def Raster_row_boundaries(raster):
    
    row_sum_index = np.where(np.sum(raster,axis=1) != 0)
    top_row = row_sum_index[0][0]
    last_row = row_sum_index[0][-1]
    
    if top_row < 0:
        top_row = 0
    if last_row < 0:
        last_row = 0
        
    return top_row, last_row

def Raster_col_boundaries(raster):
    
    col_sum_index = np.where(np.sum(raster,axis=0) != 0)
    left_col = col_sum_index[0][0]
    right_col = col_sum_index[0][-1]
    
    if left_col < 0:
        left_col = 0
    if right_col < 0:
        right_col = 0
        
    return left_col, right_col

def Read_Raster(raster_file, raster_NoData = -999):
    #print('Processing: ' + raster_file)
    raster_ds = gdal.Open(raster_file, gdal.GA_ReadOnly)
    raster_NoData = raster_ds.GetRasterBand(1).GetNoDataValue()
    raster = raster_ds.GetRasterBand(1).ReadAsArray()     
    
    return raster, raster_NoData, raster_ds


def ReadBilFile(bil):
    
    gdal.GetDriverByName('EHdr').Register()
    img = gdal.Open(bil)
    band = img.GetRasterBand(1)
    data = band.ReadAsArray()
    return data

def GetPixelCentroids(raster):
    upx, xres, xskew, upy, yskew, yres = raster.GetGeoTransform()
    cols = raster.RasterXSize
    rows = raster.RasterYSize
    
    centroids_X = np.ones((1,cols))*-999
    centroids_Y = np.ones((rows,1))*-999
    
    for j in range(rows):
        if j == 0:
            centroids_Y[j,0] = upy - np.abs(yres)/2.0
        else:
            centroids_Y[j,0] = centroids_Y[j-1,0] - np.abs(yres) 
            
    for i in range(cols):
        if i == 0:
            centroids_X[0,i] = upx + np.abs(xres)/2.0 
        else:
            centroids_X[0,i] = centroids_X[0,i-1] + np.abs(xres)
    
    return centroids_X, centroids_Y



#%%
if __name__ == '__main__':
##%% Parse Path to DEM File
    # parser = argparse.ArgumentParser(description='Inputs File')
    # parser.add_argument('-p', '--path', required='True', type=str, nargs='+',
    #                     help='Path to text file with list of input parameters')
    
    # args = parser.parse_args()
    # main_path = args.path[0].replace('\\','/')
    # csv_file_name = args.path[1].replace('\\','/')
    # system_boundary = args.path[2].replace('\\','/')
    # begin_year = int(args.path[3])
    # end_year = int(args.path[4])
    
    main_path = r'C:\Users\interactwel\Desktop\PRISM datasets\Precipitation'
    # main_path = '/Users/sammy/Library/CloudStorage/Box-Box/PRISM_data_Script/Precipitation'
    # system_boundary = '/Users/sammy/Library/CloudStorage/Box-Box/PRISM_data_Script/Prism_raster/Region_PRISMb.tif'
    system_boundary = r'C:\Users\interactwel\Desktop\PRISM datasets\Prism_raster\NEW\small_raster_Final_June2024.tif'
    begin_year = 2018
    end_year = 2022
    csv_file_name = 'Prism_jennings_watershed_precipitation_June2024.csv'

    pathunzip = main_path + '/temp'
    
    #%%
    if system_boundary.find('/'):
        path = system_boundary
    else:
        path = main_path + '/' + system_boundary
    region, region_NoData, region_obj = Read_Raster(system_boundary)
   
    region[region != region_NoData] = 1
    region[region == region_NoData] = 0
    
    centroids_X, centroids_Y = GetPixelCentroids(region_obj)
    
    top_row, last_row = Raster_row_boundaries(region)
    left_col, right_col = Raster_col_boundaries(region)
    region_org = region
    region = region[top_row:last_row+1,left_col:right_col+1]
    
    PRISM_centroids = np.zeros((len(region.flatten()),3))
    
    n=0
    for i in range(top_row,last_row+1):
        for j in range(left_col,right_col+1):
            PRISM_centroids[n,0] = n 
            PRISM_centroids[n,1] = centroids_X[0,j]
            PRISM_centroids[n,2] = centroids_Y[i,0] 
            
            n = n + 1
        
    np.savetxt(main_path + '/' + 'PRISM_Raster_Centroids_1981_2019.csv', PRISM_centroids, delimiter=",")
    
    #%%
    nrows = 0
    for year in range(begin_year,end_year+1):
        path = main_path + '/' + str(year)
        fnames = os.listdir(path)
        nrows = nrows + len(fnames)
        
    ncols = len(region.flatten()) + 3 # Year, Mon, Day
    
    #%%
    #nrows = 1825
    #ncols = 637560
    PRISM_Data = np.ones((nrows ,ncols ))*-999
    nrow = 0
    for year in range(begin_year,end_year+1):
    
        path = main_path + '/' + str(year)
        fnames = os.listdir(path)
        fnames = sorted(fnames)
        # print(fnames)
        for name in fnames:
            
            #if len(name) < 45: # added for daily temperature values
            if len(name) < 41: # added for daily min temp.
                dash_index = [i for i in range(len(name)) if name[i] == '_']
                datestr = name[dash_index[-2]+1:dash_index[-1]]
                PRISM_Data[nrow,0] = int(datestr[0:4])
                PRISM_Data[nrow,1] = int(datestr[4:6])
                PRISM_Data[nrow,2] = int(datestr[6:])
                
                pathzip = path + '/' + name
                UnzipData(pathzip,pathunzip)
                
                temp_fnames = os.listdir(pathunzip)
                main_bil_file = [tname for tname in temp_fnames if '.bil' in tname[-4:]]
                print(main_bil_file[0])
                data = ReadBilFile(pathunzip + '/' + main_bil_file[0])
                data_org = data
                data = data[top_row:last_row+1,left_col:right_col+1]
                data_reg = data
                data = np.transpose(data.flatten())
                PRISM_Data[nrow,3:3+len(data)] = data
                nrow = nrow + 1
    
    np.savetxt(main_path + '/' + csv_file_name, PRISM_Data, delimiter=",")