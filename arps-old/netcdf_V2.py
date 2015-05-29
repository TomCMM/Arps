#!/usr/bin/python
#======================================================================================================
# 	DESCRIPTION
#		Make a subplot of the variables from the ARPS simulation
#
#	USER INPUT
#		INPUT file path and filename
#		OUTPUT Path
#
#	VERSION
#		V2 -> Vertical cross Section
#	TODO
#		-Split this function in module 1) open the file 
#		-PUT THE REAL COORDINATE FOR THE PLOT NOT JUST CHANGE THE TICKS(see code comparison TRMM)
#		-make a function which importe all the variable of 'f'
#		- Enlever contour land et remplacer par geopolitical map
#		-Optimizer le calculer du total hydrometeor
#=======================================================================================================

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



#=======================
#====== user Input
#=======================
#var = raw_input("Enter arps input file (Netcdf format) #-> ")
var = 'r300m.net000000'

#filename
LenDateFormat=6# length of the hours (date) format
Pref=var[0:(len(var)-LenDateFormat)] # Prefix of the file
Date=var[(len(var)-LenDateFormat):] # hours
filename=Pref+Date # complete file name
hour=Date # initializing counting

#dirpath 
InputDirPath='/home/thomas/PhD/arps/sim/140214/out300m_control_netcdf/'# path for the input netCDF file 
OutDirPath='/home/thomas/PhD/arps/res/fig_14-02-14/control' # path for the output grahics

while  os.path.isfile(InputDirPath+filename)==True:
 


#==============================
#====== Open File
#==============================
print('\n --------------------- \n Open file:'+InputDirPath+filename)


f = netcdf.netcdf_file(InputDirPath+filename, 'r')
ResoH=f.THISDMP# history frequency
Initime_H=f.INITIAL_TIME[11:13]

#------ Take variable from the file
Initime_YMD=f.INITIAL_TIME[:10]# take the Year/month/day of the simulation
RunName=f.RUNNAME# name of the simulation
CtrLon=f.CTRLON	# Longitude centre
CtrLat=f.CTRLAT # Latitude centre 
x_stag=f.variables['x_stag']# distance x
y_stag=f.variables['y_stag']# distance Y
z_stag=f.variables['z_stag']# Distance Z
Dx=f.DX# Horizontal resolution Est-Ouest
Dy=f.DY# Horizontal resolution Nord-Sud
PT=f.variables['PT']# Temperature potential in Kelvin
PT=PT[:,:,:,:]-273.15# Transformation in degree
Qv=f.variables['QV']#'Water vapor specific humidity'
Qvs=f.variables['QVSFLX']# Surface flux of moisture
Pt=f.variables['PRCRATE4']# totale precipitation rate (m.s-1)
Veg=f.variables['VEGTYP']
Pr=f.variables['P']# Pressure (PA)
Pbar=f.variables['PBAR']# Pressure (PA)
Pbar=Pbar[:,:,:]*10**-2# Pressure hPa
Prtot=Pr[0,:,:,:]+Pbar
QI=f.variables['QI']# ice mixing ratio 
QH=f.variables['QH']# Hail mixing ratio
QS=f.variables['QS']# Snow ixing ratio 
QR=f.variables['QR']#Rain mixing ratio 
QC=f.variables['QC']#Cloud mixing ratio
U=f.variables['U']# wind
V=f.variables['V']# wind 
Hgt=f.variables['ZP'][0,:,:]# Elevation
ZP=f.variables['ZP'][:,:,:]
#------ Transform variable
Lon_00=CtrLon-((len(y_stag[:])-1)/2)*(Dy/(110*1000))# Position du point en bas a droite
Lat_00=CtrLat-((len(x_stag[:])-1)/2)*(Dx/(110*1000))# !!!!! jai approximer avec 110 km par degree!!! trouver une meilleur approximation
Lat=y_stag[:]/110000+Lat_00
Lon=x_stag[:]/110000+Lon_00
Pr=PT[:,:,:,:]*10**-2# Pressure hPa
# Intergreated QT : Total hydrometeor mixing ratio
#QT=zeros((x_stag.shape[0]-1,y_stag.shape[0]-1))
#for sss in range(0,x_stag.shape[0]-1,1):
#QT[:,sss]=QI[0,:,:,sss].sum(axis=0)+QH[0,:,:,sss].sum(axis=0)+QS[0,:,:,sss].sum(axis=0)+QR[0,:,:,sss].sum(axis=0)+QC[0,:,:,sss].sum(axis=0)

#Total hydrometeors
QT=QI[:,:,:,:]+QH[:,:,:,:]+QS[:,:,:,:]+QR[:,:,:,:]+QC[:,:,:,:]

# get the latitude, longitude
Lon1E=y_stag[:].min
Lon2E=y_stag[:].max
Lat1N=x_stag[:].min
Lat2N=x_stag[:].max

#============================
#====== Fig parameter
#============================
# Fig dimension
screen_width=1920
screen_height=1080
DPI=96# (pixel by inches) Resolution of the screen
wFig=screen_width/DPI #size in inches 
hFig=screen_height/DPI#
fig=plt.figure(figsize=(wFig,hFig))
#fig.tight_layout()
hour=int(hour)
plt.suptitle(RunName+' ' +Initime_YMD+' '+ str(int(Initime_H)+(hour/3600)-1)+'h',fontsize=20)
plt.axis([Lon1E(0),Lon2E(0),Lat1N(0),Lat2N(0)])

# Parameters to plot the wind
Nbarbs=50 # 1 barbs every Nbarbs (density)
Lbarbs=5 # length of the barbs
Nticks=60 # Ticks every ...


X, Y = np.meshgrid(x_stag[1:], y_stag[1:])
Up=U[0,13,:,1:]# wind at 5km 
Vp=V[0,13,1:,:]# wind at 5km 
Up=Up[::Nbarbs,::Nbarbs]
Vp=Vp[::Nbarbs,::Nbarbs]
Sp=np.sqrt(Up**2+Vp**2)
Xp=X[::Nbarbs,::Nbarbs]
Yp=Y[::Nbarbs,::Nbarbs]

Up = np.ma.masked_array(Up,Sp==0)# remove low value of wind
Vp = np.ma.masked_array(Vp,Sp==0)

# Ticks axis
Ticks_Lat=[ round(elem, 2) for elem in Lat[1::Nticks] ]
Ticks_Lon=[ round(elem, 2) for elem in Lon[1::Nticks] ]

#===== Position Cross section
LatCS=-21.86

ICS=np.searchsorted(Lat,LatCS, side="left")+1
CrossPosI=y_stag[ICS]
#a300m.net000000.png
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

Lat=np.array(Lat)
Lon=np.array(Lon)
LatStaI=[]
LonStaI=[]
StaName=[]
for ista,sta in enumerate(StaPos['Posto']):
	print('open station=> '+sta)
	LatI=np.searchsorted(Lat,float(StaPos['Lat '][ista]), side="left")
	LonI=np.searchsorted(Lon,float(StaPos['Lon'][ista]), side="left")
	if LatI!=0 and LonI!=0:
		LatStaI=LatStaI+[LatI]
		LonStaI=LonStaI+[LonI]
		StaName=StaName+[StaPos['Posto'][ista]]
		print("In map => "+ StaPos['Posto'][ista] +" at "+ str(LatI) +" and " +str(LonI))


##################################
#	Horizontal  plot
###################################
#1)===== Plot Surface Temperature
Plt1=plt.subplot(2,2,1)
title=('Surface Temperature(C) horizontal section')
plt.title(title)
print(title)

# create the map of position


# contour land
CL3=plt.contour(X,Y,Hgt,levels=[0],colors = 'k')

# contour Temperature Potentiel Surface
#Tmax=int(PT[0,1,:,:].max())
#Tmin=int(PT[0,1,:,:].min())
Tmax=35
Tmin=25
NCT=300 # number of temperature contour
levelsT=np.linspace(Tmin,Tmax,NCT)


CT1=plt.contourf(X,Y,PT[0,1,:,:],cmap=get_cmap('BuRd'),levels=levelsT)# filed conteur
#CT1=plt.pcolor(X,Y,PT[0,1,:,:],cmap=get_cmap('BuRd'))# filed conteur

Chgt1=plt.contour(X,Y,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/30)),cmap=get_cmap('gist_gray'))
#plt.colorbar(Chgt1)

# Set the ticks label
CT1.ax.set_xticks( x_stag[1::Nticks])
CT1.ax.set_xticklabels(Ticks_Lon) 

CT1.ax.set_yticks( y_stag[1::Nticks])
CT1.ax.set_yticklabels(Ticks_Lat)

#Grid
CT1.ax.grid(True, zorder=0)
CT1.ax.grid(True, zorder=0)

# Colorbar
Cl1=plt.colorbar(CT1)
Cl1.set_label('Temperature in C')

# wind barbs
Cw1=plt.barbs(Xp,Yp,Up,Vp,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))

scatter(np.array(LonStaI)*Dx,np.array(LatStaI)*Dy,marker='o',c='r',s=15)
#===== Plot station Position
for i,txt in enumerate(StaName):
	annotate(txt,(np.array(LonStaI[i])*Dx,np.array(LatStaI[i])*Dy))

#====== Plot Cross Section position 
plt.plot([x_stag[1:].min(),x_stag[1:].max()],[CrossPosI]*2,'--r',lw=3)

# Axis limits
plt.xlim(x_stag[1:].min(),x_stag[1:].max())
plt.ylim(y_stag[1:].min(),y_stag[1:].max())




##################################
#	Vertical plot
###################################


#======= Create the map of the position

#1)===== Plot Surface Temperature
Plt1=plt.subplot(2,2,3)
title=('Surface Temperature(C) Vertical profil')
plt.title(title)
print(title)

ElevMax=25

ZZ=(ZP[1:,ICS,:]+ZP[:-1,ICS,:])/2# compute the elevation 
PP=PT[0,:,ICS,:]
X, Y = np.meshgrid(x_stag[1:], range(47))

QT_mmin=5*1e-4
Tmax=35
Tmin=25
NCT=300 # number of temperature contour
levelsT=np.linspace(Tmin,Tmax,NCT)
CT1=plt.contourf(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BdRd'),levels=levelsT)
#CT1=plt.pcolor(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BuRd'))

# Set the ticks label
CT1.ax.set_xticks(map(int,x_stag[1::100]))
CT1.ax.set_xticklabels(map(int,x_stag[1::100])) 

CT1.ax.set_yticks(map(int,ZZ[:ElevMax,0]))
CT1.ax.set_yticklabels(map(int,ZZ[:ElevMax,0]))
Cl1=plt.colorbar(CT1)
Cl1.set_ticks(map(int,np.linspace(Tmin,Tmax,10)), update_ticks=True)
Cl1.set_ticklabels(map(int,np.linspace(Tmin,Tmax,10)),update_ticks=True)
Cl1.set_label('Temperature in C')
0

#2)===== Plot Humidity Specific Surface
Plt2=plt.subplot(2,2,2)
title=('Surface Specific Humidity (kg.kg-1)')
plt.title(title)
print(title)

Hmax=2.5*10e-3
Hmin=2.5*10e-4
NCH=500 # number of humidity contour
levelsH=np.linspace(Hmin,Hmax,NCH)

QQ=Qv[0,:,ICS,:]
CT2=plt.contourf(X[:ElevMax,:],ZZ[:ElevMax,:],QQ[:ElevMax],cmap=get_cmap('Blues'),levels=levelsH)# filed contour

Cl2=plt.colorbar(CT2)
Cl2.set_label('Specific humidity')
#Cl2.ax.set_yticks( levelsH)# axis ticks 
#Cl2.ax.set_yticklabels(levelsH)# axis label
Cl2.ax.set_yticks(np.linspace(Hmin,Hmax,10))
Cl2.ax.set_yticklabels(np.linspace(Hmin,Hmax,10))

# change the format of the ticks
#Cl2.formatter.set_scientific(True)
#Cl2.formatter.set_powerlimits((0,4))

#Cl2.format_data_short()
#Cl2.update_ticks() 

# Set the ticks label
CT2.ax.set_xticks( x_stag[1::Nticks])
CT2.ax.set_xticklabels(Ticks_Lat) 
CT2.ax.set_yticks(map(int,ZZ[:ElevMax,0]))
NCQT_m=20
CT2.ax.set_yticklabels(map(int,ZZ[:ElevMax,0]))

#4)===== Plot total hydrometeors mixing ratio 
Plt4=plt.subplot(2,2,4)
title=('Total hydrometeor mixing ratio (kg/kg-1)')
plt.title(title) 
print(title)

QT_m=np.ma.masked_where(QT<10**-5,QT)

QT_mmax=5*1e-3

QT_mmin=5*1e-4
NCQT_m=20
levelsQT_m=np.linspace(QT_mmin,QT_mmax,NCQT_m)
NlevelsQT_m=np.around(levelsQT_m,decimals=4)

QT_m=QT[0,:,ICS,:]
CT4=plt.contourf(X[:ElevMax,:],ZZ[:ElevMax,:],QT_m[:ElevMax,:],cmap=get_cmap('BuRd'),levels=NlevelsQT_m)# filed contour
Cl4_Hm=plt.colorbar(CT4)
Cl4_Hm.set_label('Total mixing ratio (kg/kg-1)')

# change the format of the ticks
Cl4_Hm.formatter.set_scientific(True)
Cl4_Hm.formatter.set_powerlimits((0,2))
Cl4_Hm.update_ticks() 



plt.savefig(OutDirPath+filename+'.png',dpi=DPI)
print('Saving:'+OutDirPath+filename+'.png \n -----------------------\n')

#plt.show()


# Next Time
hour=int(hour)+int(ResoH) # change the hour for the next file to be open
filename=Pref+Date[:-len(str(hour))]+str(hour)








