# DESCRITPION
#    1) Import a Grib file in Python 
#    2) Plot the atmospheric variables
#
    
#==========================================================================================================

#==================
#====== User input
#==================
# set latitutde and longitude    
Lat1S=-10#S
Lon1W=25#W
Lat2S=55#S lat1 << lat2
Lon2W=90#W lon1 << lon2

Lat1N=-Lat2S#N
Lon2E=(360-Lon1W)#E
Lat2N=-Lat1S#N
Lon1E=(360-Lon2W)#E
filename='1225-gfs.t18z.pgrb2
f00'# name of the grid file to import
OutPath='/dados1/arps/dataI/gfs/12-17_12_2013/'

#==================
#====== Library 
#==================

from pylab import *
import pygrib # module to import Grib file 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.ndimage

#==================
#====== Open
#==================
grbs = pygrib.open(OutPath+filename) # open the grib file

grb = grbs.select(name='Albedo')[0]

# Print an inventory of the file
grbs.seek(0)
for grb in grbs:
    grb

# To be apply to all the other variable

T2m=grbs.select(name='2 metre temperature',level=2)
# =======Select the variable needed
T0m=grbs[212] #Temperature surface [K]
T2m=grbs[222] # Temperature 2m [K]
Tg10cm=grbs[213] # Temperature -10cm [K]
Hs2m=grbs[223] #Specfici humidity 2m [kg/kg]
H2m=grbs[224] #Relative humidity 2m [%]

U2m=grbs[225] # wind 10m above the surface (horizontal component)
V2m=grbs[226] # wind 10m above the surface (vertical component)
Land=grbs[297] # Land-sea mask:(0 - 1) 

Kis=grbs[274] # short-wave indident (W/m**2)
Kil=grbs[275] # longwave indient (W/m**2)]
Kus=grbs[276] # short-wave upward (W/m**2)
Kul=grbs[278] # longwave upwards (W/m**2)

Ps=grbs[210] # surface pressure [Pa]
Ghts=grbs[211] # Geopotential Height [gpm] 

Pe=grbs[222] # Potential evaporation [w/m**2]

Cpr=grbs[230] # Convective precipitation[kg/m^2/s] 
Pr=grbs[231] # Precipitation rate [kg/m^2/s]
Tp=grbs[232] # Total Precipitation:kg m**-2
Cp=grbs[233] #Convective precipitation (water):kg m**-2

Wr=grbs[234] #Water runoff:kg m**-2 
Lhn=grbs[239] #Latent heat net flux:W m**-2 
Shn=grbs[240]#:Sensible heat net flux:W m**-2 
Ghf=grbs[241]#:Ground heat flux:W m**-2
Mfu=grbs[242]#:Momentum flux, u component:N m**-2 (avg):
Mfv=grbs[243]#:Momentum flux, v component:N m**-2 (avg)
Cape=grbs[250]#:Convective available potential energy:J kg**-1
Cin=grbs[251]#:Convective inhibition:J kg**-1 (instant):r
TCC=grbs[259]#:Total Cloud Cover:% (avg)
Alb=grbs[341]#:Albedo:% (avg):


for key in T2m.keys():
    key=str(key)# transform the unicode into a string
    T0m[key]


# value (to cite all keys use (grb.keys))
#T0mV=T0m.values

# Get the latitude and longitude of the grid
#lats, lons = grbs.latlons()

# maybe I can join the first step of importing the data  with this step
#extract data and get lat/lon values for a subset
dataT2m, lats, lons = T2m.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataH2m, lats, lons = H2m.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataU2m, lats, lons = U2m.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataV2m, lats, lons = V2m.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataLand, lats, lons = Land.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)

dataKis, lats, lons = Kis.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataKil, lats, lons = Kil.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataKus, lats, lons = Kus.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataKul, lats, lons = Kul.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)

dataPe, lats, lons = Pe.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)

dataCpr, lats, lons = Cpr.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)
dataPr, lats, lons = Pr.data(lat1=Lat1N,lat2=Lat2N,lon1=Lon1E,lon2=Lon2E)


################################ Test
# Make figure and axes with dimension as desired
wFig=10
hFig=10

fig=plt.figure(figsize=(wFig,hFig))

plt.axis([Lon1E,Lon2E,Lat1N,Lat2N])# defined axis

# Parameters to plot the wind
Nbarbs=8 # 1 barbs every Nbarbs (density)
Lbarbs=4 # length of the barbs
speedW=np.sqrt(dataU2m**2+dataV2m**2)

U=dataU2m[::Nbarbs,::Nbarbs]
V=dataV2m[::Nbarbs,::Nbarbs]
S=np.sqrt(U**2+V**2)
X=lons[::Nbarbs,::Nbarbs]
Y=lats[::Nbarbs,::Nbarbs]

U = np.ma.masked_array(U,S==0)
V = np.ma.masked_array(V,S==0)

# range of value to be ploted
NlineC=5 # number of line contour
RT2m=range(int(np.amin(dataT2m)),int(np.amax(dataT2m)),NlineC) # range temperature
Rpe=range(int(np.amin(dataPe)),int(np.amax(dataPe)),(int(np.amax(dataPe))-int(np.amin(dataPe)))/NlineC) # range potential evaporation
# Total Irradiance
dataTi=dataKis+dataKil

#====== Plot Temperature
plt.subplot(2,2,1)
plt.title('Surface Temperature (K)')

# contour land
CL1=plt.contour(lons,lats,dataLand,levels=[0],colors = 'k')

# contour Temperature
CT1=plt.contourf(lons,lats,dataT2m,cmap=get_cmap('BuRd'))# filed contour
plt.colorbar(CT1)

# wind barbs
Cwind1=plt.barbs(X,Y,U,V,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))

#====== Plot Humidity
plt.subplot(2,2,2)
plt.title('Relative Humidity (%)')
# contour land
CL2=plt.contour(lons,lats,dataLand,levels=[0],colors = 'k')

# contour humidity
CH2=plt.contourf(lons,lats,dataH2m,cmap=get_cmap('Blues'))# contour line
plt.colorbar(CH2)

# wind barbs
Cwind2=plt.barbs(X,Y,U,V,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))

#====== Plot Precipitation
plt.subplot(2,2,3)
plt.title('Precipitation rate (kg/m^2)')

# contour land
CL3=plt.contour(lons,lats,dataLand,levels=[0],colors = 'k')
# contour precipitation
#CH3=plt.contour(lons,lats,dataPr,cmap=get_cmap('Blues'))# contour line
#plt.colorbar(CH3)
#plt.clabel(CH3, inline=1, fontsize=14)
# wind barbs
Cwind3=plt.barbs(X,Y,U,V,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))



#===== plot Irradiance total + evapotranspiration
plt.subplot(2,2,4)
plt.title('Evaporationtranspiration + Irradiance')

# contour land
CL4=plt.contour(lons,lats,dataLand,levels=[0],colors = 'k')

# contour Irradiance
CI4=plt.contourf(lons,lats,dataTi,cmap=get_cmap('PuRd'))# contour line


# contour evapotranspiration
CPe4=plt.contour(lons,lats,dataPe,levels=Rpe,linewidths=3,cmap=get_cmap('Greens'))# contour line



plt.show()# display the plot





