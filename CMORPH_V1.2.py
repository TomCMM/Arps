#=======================================================
#Thomas July 2014
#	DESCRIPTION
#		IMPORT AND PLOT THE CMORPH PRODUCT
# 
#========================================================


#=====================
#===== Library
#=====================
from __future__ import division # to be able to get a floatting point (for the divis
import os.path # to check if the file exist 
from scipy.io import netcdf
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.ndimage
from pylab import *
import matplotlib.gridspec as gridspec
import csv
from os import listdir
from os.path import isfile, join
from scipy import interpolate

#=======================
#====== user Input
#=======================

#------ Input ARPS/
InputDirPath='/home2/sim/out300m_V27_netcdf/'
fn = 'r300m.net000000'

#------ Input cmorph
InputDirPath_cmorph='/home/thomas/PhD/obs-lcb/CMORPH/FEV14/201402/'
filename_cmorph='cmorph14022014.nc'

#------ Output
OutDirPath='/home/thomas/PhD/arps/res/fig_14-02-14/CMORPH/V27/' 

# Check if the repertory exist and create one if not
if not os.path.exists(OutDirPath):
    os.makedirs(OutDirPath)



Hourcum=3600#Number of hours of accumulation in Second
UTC=0
#====================
#	OPEN FILE CMORPH
#===================

f_cmorph = netcdf.netcdf_file(InputDirPath_cmorph+filename_cmorph, 'r')

Prec_cmorph=f_cmorph.variables['cmorph']
Time_cmorph=f_cmorph.variables['time']
lat_cmorph=f_cmorph.variables['latitude']
lon_cmorph=f_cmorph.variables['longitude'][:]-360
Initime_cmorph=datetime.datetime.strptime(f_cmorph.variables['time'].units,'hours since %Y-%m-%d %H')

Date_cmorph=[Initime_cmorph+datetime.timedelta(hours=d+UTC) for d in Time_cmorph]


#===================
#-----Open ARPS file
#===================
Arpsfiles = sorted([ f for f in listdir(InputDirPath) if isfile(join(InputDirPath,f)) ])
for  cpt,fn in enumerate(Arpsfiles):
f = netcdf.netcdf_file(InputDirPath+fn, 'r')
Initime_arps=datetime.datetime.strptime(f.INITIAL_TIME,'%Y-%m-%d_%H:%M:%S')
Date_arps=Initime_arps+datetime.timedelta(seconds=int(fn[-6:]))
Rainc_arps=f.variables['RAINC']
Raing_arps=f.variables['RAING']
P_arps=Rainc_arps[0,:,:]+Raing_arps[0,:,:]# compute the total cumulated rain

#============================
#-----Open ARPS file + 3hours
#============================

fname_3h=InputDirPath+fn[0:9].ljust(len(fn)-len(str(int(fn[-6:])+Hourcum)),'0')+str((int(fn[-6:])+Hourcum))
Date_arps3h=Date_arps+datetime.timedelta(seconds=Hourcum)
f_3h = netcdf.netcdf_file(fname_3h, 'r')

# Take the variables
Rainc_arps_3h=f_3h.variables['RAINC']
Raing_arps_3h=f_3h.variables['RAING']
Hgt=f_3h.variables['ZP'][1,:,:]# Elevation
P_arps_3h=Rainc_arps_3h[0,:,:]+Raing_arps_3h[0,:,:]# compute the total cumulated rain


#---- Compute the accumulated precipitation for 3h 
Pcum_3h_arps=P_arps_3h-P_arps

#========================
#----- Define the domain
#========================
ctrlat=f.CTRLAT
ctrlon=f.CTRLON
truelon=f.TRUELON
truelat1=f.TRUELAT1
truelat2=f.TRUELAT2


#========================
#	Projection
#========================
from pyproj import Proj
pnyc = Proj(proj='lcc',datum='WGS84',lat_1=truelat1,lat_2=truelat2,lat_0=ctrlat,lon_0=ctrlon)

x_stag=f.variables['x_stag']
y_stag=f.variables['y_stag']
#X, Y = np.meshgrid(x_stag[1:]-(x_stag[:].max())/2, y_stag[1:]-(y_stag[:].max())/2)
Lon_arps,Lat_arps= pnyc(x_stag[1:]-(x_stag[:].max())/2,y_stag[1:]-(y_stag[:].max())/2, inverse=True)



#=======================
#Set CMORPH =  ARPS domain
#======================= 
lon_min_idx=[i for i,v in enumerate(map(float,lon_cmorph[:])) if v > Lon_arps.min()][0]
lon_max_idx=[i for i,v in enumerate(map(float,lon_cmorph[:])) if v < Lon_arps.max()][-1]
lat_min_idx=[i for i,v in enumerate(map(float,lat_cmorph[:])) if v > Lat_arps.min()][0]
lat_max_idx=[i for i,v in enumerate(map(float,lat_cmorph[:])) if v < Lat_arps.max()][-1]

Nlat_cmorph=lat_cmorph[lat_min_idx : lat_max_idx]
Nlon_cmorph=lon_cmorph[lon_min_idx : lon_max_idx]


#Prec_cmorph_d=np.sum(Prec_cmorph[Date_cmorph.index(Date_arps),lat_min_idx : lat_max_idx,lon_min_idx : lon_max_idx],axis=0)
Prec_cmorph_d=np.sum(Prec_cmorph[Date_cmorph.index(Date_arps):Date_cmorph.index(Date_arps3h),lat_min_idx : lat_max_idx,lon_min_idx : lon_max_idx],axis=0) # select the same domain than ARPS and convert in 'mm'
#Prec_cmorph_d=Prec_cmorph_d.T#Replace longitude to the x axis and latitude to the 

#Create a new grid domain which fit the cmorpg grid + Downscale
NLon_arps=np.linspace(lon_cmorph[lon_min_idx],lon_cmorph[lon_max_idx], num=((lon_max_idx-lon_min_idx)*40))# Increase arps resolution to 200m (multiple of 8km)
NLat_arps=np.linspace(lat_cmorph[lat_min_idx],lat_cmorph[lat_max_idx], num=((lat_max_idx-lat_min_idx)*40))#


Interp=interpolate.RectBivariateSpline(Lat_arps,Lon_arps,Pcum_3h_arps)
NPcum_3h_arps=Interp(NLat_arps,NLon_arps)



def downsample(myarr,factor,estimator=mean):
    """
    Downsample a 2D array by averaging over *factor* pixels in each axis.
    Crops upper edge if the shape is not a multiple of factor.

    This code is pure numpy and should be fast.

    keywords:
	estimator - default to mean.  You can downsample by summing or
	    something else if you want a different estimator
	    (e.g., downsampling error: you want to sum & divide by sqrt(n))
    """
    ys,xs = myarr.shape
    crarr = myarr[:ys-(ys % int(factor)),:xs-(xs % int(factor))]
    dsarr = estimator( np.concatenate([[crarr[i::factor,j::factor]
	for i in range(factor)]
	for j in range(factor)]), axis=0)
    return dsarr

NPcum_3h_arps_8km=downsample(NPcum_3h_arps,40,estimator=mean)


###################################
# Position of the Stations
###################################
StaPosFile="/home/thomas/PhD/obs-lcb/staClim/LatLonSta.csv"
StaPos={}
with open (StaPosFile) as StaPosF:
	reader_IAC=csv.reader(StaPosF,delimiter=",")
	header_IAC=reader_IAC.next()
	for h in header_IAC:
		StaPos[h]=[]
	for row in reader_IAC:
		for h,v in zip(header_IAC,row):
			StaPos[h].append(v)

LatSta=[]
LonSta=[]
StaName=[]
for ista,sta in enumerate(StaPos['Posto']):
	print('open station=> '+sta)
	if float(StaPos['Lat '][ista]) !=-99.9 and float(StaPos['Lon'][ista])!=-99.9:
		if float(StaPos['Lat '][ista]) > Nlat_cmorph.min() and float(StaPos['Lat '][ista]) < Nlat_cmorph.max() and float(StaPos['Lon'][ista]) > Nlon_cmorph.min() and float(StaPos['Lon'][ista]) < Nlon_cmorph.max():
			LatSta=LatSta+[float(StaPos['Lat '][ista])]# Use in compareGFS_OBS.py
			LonSta=LonSta+[float(StaPos['Lon'][ista])]#Use in compareGFS_OBS.py
			StaName=StaName+[StaPos['Posto'][ista]]



#======================
# 	PLOT
#======================
screen_height=1080
screen_width=1920
DPI=96# (pixel by inches) Resolution of the screen

wFig=screen_width/DPI #size in inches 
hFig=screen_height/DPI#
fig=plt.figure(figsize=(wFig,hFig))

#----- Plot the Cmorph accumulated data
Plt1=plt.subplot(2,1,1)
title=('1 hourly accumulated from CMORPH (mm)')
plt.title(title)

Pmax=40
Pmin=6e-5
NCP=10 # number of precepitation contour

levelsP=np.linspace(Pmin,Pmax,NCP)

CT1=plt.contourf(Nlon_cmorph,Nlat_cmorph,Prec_cmorph_d,levels=levelsP,alpha=0.7)
Cl1=plt.colorbar(CT1)
if cpt==0:
	TotPrecCmorph=Prec_cmorph_d
else:
	TotPrecCmorph=TotPrecCmorph+Prec_cmorph_d


Hgt=f.variables['ZP'][0,:,:]# Elevation
Chgt1=plt.contourf(Lon_arps,Lat_arps,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/20)),cmap=get_cmap('gist_gray'),alpha=0.5)

scatter(np.array(LonSta),np.array(LatSta),marker='o',c='r',s=20)
#===== Plot station Position
for i,txt in enumerate(StaName):
	print(i)
	print(txt)
	annotate(str(txt),(np.array(LonSta[i]),np.array(LatSta[i])),fontsize=10)



#----- Plot the ARPS accumulated data
Plt2=plt.subplot(2,1,2)
title=('1 hourly Accumulated Precipitation from ARPS (mm)')
plt.title(title)

CT2=plt.contourf(Nlon_cmorph,Nlat_cmorph,NPcum_3h_arps_8km,levels=levelsP,alpha=0.7)

if cpt==0:
	TotPrecArps=NPcum_3h_arps_8km
else:
	TotPrecArps=TotPrecArps+NPcum_3h_arps_8km
TotPrecArps=TotPrecArps+NPcum_3h_arps_8km
Cl2=plt.colorbar(CT2)
Hgt=f.variables['ZP'][0,:,:]# Elevation
Chgt1=plt.contourf(Lon_arps,Lat_arps,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/20)),cmap=get_cmap('gist_gray'),alpha=0.5)

scatter(np.array(LonSta),np.array(LatSta),marker='o',c='r',s=20)
#===== Plot station Position
for i,txt in enumerate(StaName):
	annotate(txt,(np.array(LonSta[i]),np.array(LatSta[i])),fontsize=10)

plt.savefig(OutDirPath+fn+'.png',dpi=DPI)
print('Saving:'+OutDirPath+fn+'.png \n -----------------------\n')

####################################
#Print Total cumulated Precipitation
####################################
screen_height=1080
screen_width=1920
DPI=96# (pixel by inches) Resolution of the screen

wFig=screen_width/DPI #size in inches 
hFig=screen_height/DPI#
fig=plt.figure(figsize=(wFig,hFig))
#----- Plot the Cmorph accumulated data
Plt1=plt.subplot(2,1,1)
title=('1 hourly accumulated from CMORPH (mm)')
plt.title(title)

Pmax=200
Pmin=10
NCP=10 # number of precepitation contour

levelsP=np.linspace(Pmin,Pmax,NCP)

CT1=plt.contourf(Nlon_cmorph,Nlat_cmorph,TotPrecCmorph,levels=levelsP,alpha=0.7)
Cl1=plt.colorbar(CT1)


Hgt=f.variables['ZP'][0,:,:]# Elevation
Chgt1=plt.contourf(Lon_arps,Lat_arps,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/20)),cmap=get_cmap('gist_gray'),alpha=0.5)

scatter(np.array(LonSta),np.array(LatSta),marker='o',c='r',s=20)
#===== Plot station Position
for i,txt in enumerate(StaName):
	print(i)
	print(txt)
	annotate(str(txt),(np.array(LonSta[i]),np.array(LatSta[i])),fontsize=10)



#----- Plot the ARPS accumulated data
Plt2=plt.subplot(2,1,2)
title=('1 hourly Accumulated Precipitation from ARPS (mm)')
plt.title(title)

CT2=plt.contourf(Nlon_cmorph,Nlat_cmorph,TotPrecArps,levels=levelsP,alpha=0.7)
Cl2=plt.colorbar(CT2)
Hgt=f.variables['ZP'][0,:,:]# Elevation
Chgt1=plt.contourf(Lon_arps,Lat_arps,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/20)),cmap=get_cmap('gist_gray'),alpha=0.5)

scatter(np.array(LonSta),np.array(LatSta),marker='o',c='r',s=20)
#===== Plot station Position
for i,txt in enumerate(StaName):
	annotate(txt,(np.array(LonSta[i]),np.array(LatSta[i])),fontsize=10)

plt.savefig(OutDirPath+'Total'+'.png',dpi=DPI)
print('Saving:'+OutDirPath+'Total'+'.png \n -----------------------\n')



