# Plot the 3 h accumulated precipitation (mm) from ARPS and TRMM
# The paths for the 2 arps file need to be specified 
# The path for the TRMM file need to be specified  

#====== Modification
#->17/Dec/13 -> First version of the programm

#====== TO DO
 
#-> write this function as a module
#-> simplified the code by making function

from scipy.io import netcdf
import numpy as np
import sys # to get information about the computer
import matplotlib.pyplot as plt
from projpytom import P_lcc
#-----Open TRMM file
fn_TRMM='3B40RT.2013120216.7.G3.nc'
IDP_TRMM='/home/thomas/PhD/arps/obs/TRMM/data/'# path input .bin TRMM  file 
fname_TRMM=IDP_TRMM+fn_TRMM
f_TRMM = netcdf.netcdf_file(fname_TRMM, 'r')

# Take the variables
Prec_TRMM=f_TRMM.variables['precipitation'].data
lat_TRMM=f_TRMM.variables['lat']
lon_TRMM=f_TRMM.variables['lon']

#-----Open ARPS file 
fn='r27km.net003600'
IDP='/data1/arps/testtom3/realexp/run/out27km_netcdf/'
fname=IDP+fn
f = netcdf.netcdf_file(fname, 'r')

# Take the variables
Rainc_arps=f.variables['RAINC']
Raing_arps=f.variables['RAING']
P_arps=Rainc_arps[0,:,:]+Raing_arps[0,:,:]# compute the total cumulated rain

#-----Open ARPS file + 3hours
fn_3h='r27km.net014400'
IDP_3h='/data1/arps/testtom3/realexp/run/out27km_netcdf/'
fname_3h=IDP_3h+fn_3h
f_3h = netcdf.netcdf_file(fname_3h, 'r')

# Take the variables
Rainc_arps_3h=f_3h.variables['RAINC']
Raing_arps_3h=f_3h.variables['RAING']
Hgt=f_3h.variables['ZP'][1,:,:]# Elevation
P_arps_3h=Rainc_arps_3h[0,:,:]+Raing_arps_3h[0,:,:]# compute the total cumulated rain

#---- Compute the accumulated precipitation for 3h 
Pcum_3h_arps=P_arps_3h-P_arps

#----- Define the domain
ctrlat=f.CTRLAT
ctrlon=f.CTRLON
truelat1=f.TRUELAT1
truelat2=f.TRUELAT2
truelon=f.TRUELON

x_stag=f.variables['x_stag']
y_stag=f.variables['y_stag']
X, Y = np.meshgrid(x_stag[1:]-(x_stag[:].max())/2, y_stag[1:]-(y_stag[:].max())/2)
Lon_arps,Lat_arps=P_lcc(X,Y,truelat1,truelat2,ctrlat,ctrlon,inv=True)

#Set TRMM =  ARPS domain 
lon_min_idx = np.argmin(np.abs(lon_TRMM[:] - Lon_arps.min()))# find the position of the border of the arps domain
lon_max_idx = np.argmin(np.abs(lon_TRMM[:] - Lon_arps.max()))
lat_min_idx = np.argmin(np.abs(lat_TRMM[:] - Lat_arps.min()))
lat_max_idx = np.argmin(np.abs(lat_TRMM[:] - Lat_arps.max()))

Lon_TRMM, Lat_TRMM = np.meshgrid(lon_TRMM[lon_min_idx : lon_max_idx], lat_TRMM[lat_min_idx : lat_max_idx])
Prec_TRMM_d=Prec_TRMM[lat_min_idx : lat_max_idx,lon_min_idx : lon_max_idx] # select the same domain than ARPS and convert in 'mm'

#------ mask value = -9999  
Prec_TRMM_m=np.ma.masked_where(Prec_TRMM_d==-9999,Prec_TRMM_d)
Prec_TRMM_m=Prec_TRMM_m*3# to put (mm/h) in mm

#OOOOO PLOT
screen_height=1080
screen_width=1920
DPI=96# (pixel by inches) Resolution of the screen

wFig=screen_width/DPI #size in inches 
hFig=screen_height/DPI#
plt.suptitle(fn+' - '+ fn_3h)


#----- Plot the TRMM accumulated data
Plt1=plt.subplot(2,1,1)
title=('3 hourly Accumulated Precipitation from TRMM (mm)')
plt.title(title)

CT1=plt.contourf(Lon_TRMM,Lat_TRMM,Prec_TRMM_m)
Cl1=plt.colorbar(CT1)

#----- Plot the arps accumulated data
Plt2=plt.subplot(2,1,2)
title=('3 hourly Accumulated Precipitation from ARPS (mm)')
plt.title(title)
L3=plt.contour(Lon_arps,Lat_arps,Hgt,levels=[0],colors = 'k')#contour land
CT2=plt.contourf(Lon_arps,Lat_arps,Pcum_3h_arps)
Cl2=plt.colorbar(CT2)





T1=plt.contourf(Lon_TRMM,Lat_TRMM,Prec_TRMM)
