# DESCRIPTION
#	Compute the reflectivity of the hydrometeors concentrations 
#	from the Thompson microphysics scheme used by the ARPS model

#	REFERENCES
#	Equation used for the calculation of the hydrometeors distribution are explained in :
#
#	Thompson et al. 2004
#	Explicit forecasts of winter precipitation using an improved bulk mi- crophysics scheme. Part I: Description and sensitivity analy- sis. 
#	Mon. Wea. Rev
#
#	Thompson et al. 2008  
#	Explicit Forecasts of Winter Precipitation Using an Improved Bulk Microphysics Scheme. Part I: Description and Sensitivity Analysis
#	Monthly weather review
#
#	Author
#	Thomas Martin, 2014
#==================================================

#===============================================================================
# Python Library
#===============================================================================
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


#===============================================================================
# User input
#===============================================================================
#var = raw_input("Enter arps input file (Netcdf format) #-> ")
var = 'r300m.net039600'

#filename
LenDateFormat=6# length of the hours (date) format
Pref=var[0:(len(var)-LenDateFormat)] # Prefix of the file
Date=var[(len(var)-LenDateFormat):] # hours
filename=Pref+Date # complete file name
hour=Date # initializing counting

#dirpath 
InputDirPath='/home/thomas/PhD/arps/sim/140214/out300m_control_netcdf/'# path for the input netCDF file 
OutDirPath='/home/thomas/PhD/arps/res/fig_14-02-14/V15/NS/' # path for the output grahics

f = netcdf.netcdf_file(InputDirPath+filename, 'r')
ResoH=f.THISDMP# history frequency
Initime_H=f.INITIAL_TIME[11:13]

#------ Take variable from the file
# This is not necessary with the new version of the code netcdf_lib
# but I let it there as it helps to understand the equations
Initime_YMD=f.INITIAL_TIME[:10]# take the Year/month/day of the simulation
RunName=f.RUNNAME# name of the simulation
CtrLon=f.CTRLON	# Longitude centre
CtrLat=f.CTRLAT # Latitude centre 
x_stag=f.variables['x_stag']# distance x
y_stag=f.variables['y_stag']# distance Y
z_stag=f.variables['z_stag']# Distance Z
Dx=f.DX# Horizontal resolution Est-Ouest
Dy=f.DY# Horizontal resolution Nord-Sud
PTk=f.variables['PT']# Temperature potential in Kelvin
PT=PTk[:,:,:,:]-273.15# Transformation in degree
Qv=f.variables['QV']#'Water vapor specific humidity'
Qvs=f.variables['QVSFLX']# Surface flux of moisture
Pt=f.variables['PRCRATE4']# totale precipitation rate (m.s-1)
Veg=f.variables['VEGTYP']
Pr=f.variables['P']# Pressure (PA)
Pr=Pr[:,:,:,:]*10**-2# Pressure (hPA)
Pbar=f.variables['PBAR']# Pressure (hPA)
Pbar=Pbar[:,:,:]*10**-2# Pressure hPa
Prtot=Pr[0,:,:,:]+Pbar
QI=f.variables['QI']# ice mixing ratio 
QH=f.variables['QH']# Hail mixing ratio
QG=QH# Graupel and Hail are similar
QS=f.variables['QS']# Snow ixing ratio 
QR=f.variables['QR']#Rain mixing ratio 
QC=f.variables['QC']#Cloud mixing ratio
U=f.variables['U']# wind
V=f.variables['V']# wind 
Hgt=f.variables['ZP'][0,:,:]# Elevation
ZP=f.variables['ZP'][:,:,:]#Altitude of the point

#------ Transform variable
Lon_00=CtrLon-((len(y_stag[:])-1)/2)*(Dy/(110*1000))# Position of the bottom right point SEE GEOPY !!!!! I made this for the radar
Lat_00=CtrLat-((len(x_stag[:])-1)/2)*(Dx/(110*1000))# !!!!! I have made the approximation that 1Degree = 110km!!! IN the futur find a better approximation
Lat=y_stag[1::]/110000+Lat_00
Lon=x_stag[1::]/110000+Lon_00

#====== Constant
Rd= 287.05 # Specific gaz constant for dry air
Rv= 461.495 # Specific gas constant for humid air 
P0=100000
Cp=1004.5 #heat capacity J/(kg K)
rho_s=100 # density Snow
rho_g=400 # density graupel
rho_solid=917 # density Solid
rho_w=1000 # density Water
ki2=0.176# dielectric constant Ice
kl2=0.930# Dielectric constant water


#====== Specific variable
#-------- Real Temperature
RTk=PTk[:,:,:,:]*(Pr*10**2/P0)**(Rd/Cp);

#-------- Partial Pressure
#vapor
Prv=((Qv[:,:,:,:]*(Pr*10**2))/(0.622+Qv[:,:,:,:])) #(Pa)
#Dry air
Prd=Pr*10**2-Prv # (Pa)

#-------- Density Air (humid)
Rho_air=Prd/(Rd*RTk) + Prv/(Rv*RTk)

#===============================================================================
# Distribution Parameters
#===============================================================================
#------ Intercept parameters (used in the Tompson scheme simulation)
N0r=8*10**6# rain m-4
N0s=3*10**6# snow m-4
N0g=4*10**4# graupel m-4

conv=1*10**(-8) # N0x need to be in cm -4 and not in m-4 in some equations
conv2=1*10**(-3) # convert g to kg


#----- Lambda parameters
L_r=((math.pi*rho_w*conv2*N0r*conv)/(Rho_air*conv2*QR.data))**0.25 # Rain  
L_s=((math.pi*rho_s*conv2*N0s*conv)/(Rho_air*conv2*QS.data))**0.25 # Snow
L_g=((math.pi*rho_g*conv2*N0g*conv)/(Rho_air*conv2*QG.data))**0.25 # Graupel


#----- Reflectivity
#Z_r=math.gamma(7)*N0r*(L_r*10**2)**-7
#Z_r=Z_r*10**18
#Z_r=10*np.log10(Z_r)
#Z_r[isnan(Z_r)]=0
#Z_r[isinf(Z_r)]=0
#Z_r[Z_r<0]=0
#Z_r[Z_r<15]=0# seuil superieur a 15dbz

#Z_s=((ki2/kl2)*(rho_s/rho_solid)**2)*(math.gamma(7)*N0s*(L_s*10**2)**-7)
#Z_s=Z_s*10**18
#Z_s=10*np.log10(Z_s)
#Z_s[isnan(Z_s)]=0
#Z_s[isinf(Z_s)]=0
#Z_s[Z_s<0]=0
#Z_s[Z_s<15]=0# seuil superieur a 15dbz

#Z_g=((ki2/kl2)*(rho_g/rho_solid)**2)*(math.gamma(7)*N0g*(L_g*10**2)**-7)
#Z_g=Z_g*10**18
#Z_g=10*np.log10(Z_g)
#Z_g[isnan(Z_g)]=0
#Z_g[isinf(Z_g)]=0
#Z_g[Z_g<0]=0
#Z_s[Z_s<15]=0# seuil superieur a 15dbz



#===============================================================================
# Compute the reflectivity of each hydrometeors and the total reflectivity
#===============================================================================

Z_r=math.gamma(7)*N0r*(L_r*10**2)**-7 # Rain reflectivity
Z_s=((ki2/kl2)*(rho_s/rho_solid)**2)*(math.gamma(7)*N0s*(L_s*10**2)**-7) # Snow reflectivity
Z_g=((ki2/kl2)*(rho_g/rho_solid)**2)*(math.gamma(7)*N0g*(L_g*10**2)**-7) # Graupel reflectivity

Z=Z_s+Z_g+Z_r

Z=Z*10**18 # convert in DBZ
Z=10*np.log10(Z) # convert in DBZ
Z[isnan(Z)]=0 # Put zero where nan
Z[isinf(Z)]=0 # Put zero where infinte value
Z[Z<0]=0 # Put zero on negative values

#===============================================================================
# 2) RADAR
#===============================================================================
#------ Constant 
Elev_angle=2.9
# Earth radius (m)
R=6371.0072*10**3
# Altitude Radar
H_rad=925
#Latitude position 
Lat_ctr=-23.60
#Longitude position of the radar
Lon_ctr=-45.9722

# Equivalent earth radius
#Authalic radius of the earth ("equal area -hypothetical perfect sphere")
Re=R*(4/3)

#------ Radar range 
zeniths=np.array([])
zeniths=np.append(zeniths,np.arange(0.5,60,0.5))
zeniths=np.append(zeniths,np.arange(60,120,1))
zeniths=np.append(zeniths,np.arange(120,242,2))*1000

azimuths=range(0,360)

#% Equation Doviak and Zrnic (2.28b and 2.28c)
H_pos=(np.sqrt(zeniths**2+(H_rad+Re)**2+2*zeniths*(Re+H_rad)*sin((np.pi/180)*Elev_angle))-Re)
			
#%length (m)
Dist_pos=(np.arctan(zeniths*np.cos(Elev_angle*(np.pi/180))/ (zeniths*np.sin(Elev_angle*(np.pi/180))+Re+H_rad))*Re)		


#============= Transform Polar to cartesian
import geopy 
from geopy.distance import VincentyDistance

def polar2cart(r, theta):
	x = r * np.cos(theta)
	y = r * np.sin(theta)
	return x, y

Lat_rad=np.array([])
Lon_rad=np.array([])
origin = geopy.Point(Lat_ctr, Lon_ctr)
for i in azimuths:
	for j in Dist_pos:	
		y,x=polar2cart(j,i*(np.pi/180))# convert into meters distance X and Y 
		if x>=0:
			Lon_rad = np.append(Lon_rad,VincentyDistance(kilometers=np.abs(x)/1000).destination(origin,90).longitude)
		else:
			Lon_rad = np.append(Lon_rad,VincentyDistance(kilometers=np.abs(x)/1000).destination(origin,270).longitude)
		if y>=0:
			Lat_rad = np.append(Lat_rad,VincentyDistance(kilometers=np.abs(y)/1000).destination(origin, 0).latitude)
		else:
			Lat_rad = np.append(Lat_rad,VincentyDistance(kilometers=np.abs(y)/1000).destination(origin, 180).latitude)


H_rad=np.tile(H_pos,(360,1)).flatten()

#===============================================================================
# Interpolate model value on radar position (Lat, lon, H)
#===============================================================================

from scipy.interpolate import griddata
import time


Lon_mod,Lat_mod=np.meshgrid(Lon,Lat)
Lon_mod=np.tile(Lon_mod,(47,1,1))
Lat_mod=np.tile(Lat_mod,(47,1,1))

Pos_mod=np.array([Lon_mod.flatten(),Lat_mod.flatten(),ZP[1::,:,:].flatten()]).transpose()
Pos_rad=np.array([Lon_rad,Lat_rad,H_rad]).transpose()


Z_rad=np.array([])
rad_Lat=np.array([])
rad_Lon=np.array([])
rad_val=np.array([])
H_rad2=np.array([])
#===== Quickly find the first indice to reduce the interpolation to 8 point
for idx in range(0,len(Lon_rad)):
	if Lat_rad[idx]<Lat.max() and Lat_rad[idx]>Lat.min() and Lon_rad[idx]<Lon.max() and Lon_rad[idx]>Lon.min(): # select only the point in the domain
		rad_val=np.append(rad_val,values.flatten()[idx])#Need to get the values for the radar script
		rad_Lat=np.append(rad_Lat,Lat_rad[idx])# take only the value of Lat and Longitude which are in the simulation domain
		rad_Lon=np.append(rad_Lon,Lon_rad[idx])
		ILat=next(i for i,v in enumerate(Lat) if v > Lat_rad[idx])# Find the Indice of Lat, Lon in the simulation vector corresponding to the radar position  
		ILon=next(i for i,v in enumerate(Lon) if v > Lon_rad[idx])
		ILon=np.array([[ILon,ILon-1]*2])
		ILat=np.repeat(np.array([ILat,ILat-1]),[2,2],axis=0)
		IH=np.array([])
		Hz=np.array([])
		for j in range(0,4):
			IH=np.append(IH,next(i for i,v in enumerate(ZP[:,ILon[0][j],ILat[j]]) if v > H_rad[idx]))
		#print("Interpolating the point --> Lat: "+str(Lat_rad[idx])+" Indice "+str(ILat)+" Lon: "+ str(Lon_rad[idx])+ " Indice "+str(ILon))
		ILat=np.tile(ILat,2)
		ILon=np.tile(ILon,2)
		IH=np.append(IH,IH-1)
		Zz=np.array([])
		Latz=np.array([])
		Lonz=np.array([])
		for j in range(0,8):
			Zz=np.append(Zz,Z[0,IH[j],ILat[j],ILon[0][j]])
			Latz=np.append(Latz,Lat[ILat[j]])
			Lonz=np.append(Lonz,Lon[ILon[0][j]])
			Hz=np.append(Hz,ZP[IH[j],ILon[0][j],ILat[j]])
		Pos_modN=np.array([Lonz,Latz,Hz]).transpose()
		Pos_radN=np.array([[Lon_rad[idx]],[Lat_rad[idx]],[H_rad[idx]]]).transpose()
		Z_rad=np.append(Z_rad,griddata(Pos_modN,Zz,Pos_radN))
		H_rad2=np.append(H_rad2,griddata(Pos_modN,Hz,Pos_radN))






#===============================================================================
# 
#===============================================================================
import matplotlib.mlab as ml
Lati = np.linspace(rad_Lat.min(),rad_Lat.max(),300)
Loni = np.linspace(rad_Lon.min(),rad_Lon.max(),300)

Z_sim=ml.griddata(rad_Lon,rad_Lat,Z_rad,Loni,Lati)
H_sim=ml.griddata(rad_Lon,rad_Lat,H_rad2,Loni,Lati)
Z_radari=ml.griddata(rad_Lon,rad_Lat,rad_val,Loni,Lati)

#====== Masked array
Z_sim_m=np.ma.masked_where(Z_sim<20,Z_sim)
Z_radar_m=np.ma.masked_where(Z_radari<20,Z_radari)

#===== Make colormap
def radar_colormap():
    nws_reflectivity_colors = [
    "#646464", # ND
    "#ccffff", # -30
    "#cc99cc", # -25
    "#996699", # -20
    "#663366", # -15
    "#cccc99", # -10
    "#999966", # -5
    "#646464", # 0
    "#04e9e7", # 5
    "#019ff4", # 10
    "#0300f4", # 15
    "#02fd02", # 20
    "#01c501", # 25
    "#008e00", # 30
    "#fdf802", # 35
    "#e5bc00", # 40
    "#fd9500", # 45
    "#fd0000", # 50
    "#d40000", # 55
    "#bc0000", # 60
    "#f800fd", # 65
    "#9854c6", # 70
    "#fdfdfd" # 75
    ]
    cmap = mpl.colors.ListedColormap(nws_reflectivity_colors)
    return cmap



plt.figure(3)
plt.contourf(Lon_mod[1,:,:],Lat_mod[1,:,:],Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/100)),cmap=get_cmap('gist_gray'))
contour(Loni,Lati,H_sim,levels=range(int(300),int(H_sim.max()),int((H_sim.max()-H_sim.min())/10)))
plt.colorbar()

plt.figure(1)
plt.contourf(Lon_mod[1,:,:],Lat_mod[1,:,:],Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/100)),cmap=get_cmap('gist_gray'))
contour_levels = np.arange(-30, 80, 5)
contourf(Loni,Lati,Z_sim_m,cmap=cmap,levels=contour_levels)
plt.colorbar()

plt.figure(2)
plt.contourf(Lon_mod[1,:,:],Lat_mod[1,:,:],Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/100)),cmap=get_cmap('gist_gray'))
contour_levels = np.arange(-30, 80, 5)
contourf(Loni,Lati,Z_radar_m,levels=contour_levels,cmap=cmap)
plt.colorbar()
plt.show()
















