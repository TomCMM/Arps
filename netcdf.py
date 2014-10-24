#!/usr/bin/python
# 	Make a subplot of the variables from the ARPS simulation
#
#Import the NETCDF file, the PATH and the name of the file need to be specified.
#
#
#===== To do
#-> PUT THE REAL COORDINATE FOR THE PLOT NOT JUST CHANGE THE TICKS(see code comparison TRMM)
#-> make a function which importe all the variable of 'f'

from __future__ import division # to be able to get a floatting point (for the divis
import os.path # to check if the file exist 
from scipy.io import netcdf
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.ndimage
from pylab import *
#import pygrib
import matplotlib.gridspec as gridspec
#from plot import cmappytom

# user Input
#var = raw_input("Enter arps input file (Netcdf format) #-> ")
var = 'r300m.net000000'

#filename
LenDateFormat=6# length of the hours (date) format
Pref=var[0:(len(var)-LenDateFormat)] # Prefix of the file
Date=var[(len(var)-LenDateFormat):] # hours
filename=Pref+Date # complete file name
hour=Date # initializing counting

#dirpath 
InputDirPath='/home2/sim/out300m_V25_netcdf/'# path for the input netCDF file 
OutDirPath='/home/thomas/PhD/arps/res/fig_14-02-14/V25/prec/' # path for the output graphics

# Check if the repertory exist and create one if not
if not os.path.exists(OutDirPath):
    os.makedirs(OutDirPath)

while  os.path.isfile(InputDirPath+filename)==True:
	#----- Open the Netcdf file
	print('\n --------------------- \n Open file:'+InputDirPath+filename)
	f = netcdf.netcdf_file(InputDirPath+filename, 'r')
	ResoH=f.THISDMP# history frequency
	Initime_H=f.INITIAL_TIME[11:13]
	hour=int(hour)+int(ResoH) # change the hour for the next file to be open
	filename=Pref+Date[:-len(str(hour))]+str(hour)

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
	PT=f.variables['PT']# Temperature potential in degree
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

	#------ Transform variable
	Lon_00=CtrLon-((len(y_stag[:])-1)/2)*(Dy/(110*1000))# Position du point en bas a droite
	Lat_00=CtrLat-((len(x_stag[:])-1)/2)*(Dx/(110*1000))# !!!!! jai approximer avec 110 km par degree!!! trouver une meilleur approximation
	Lat=y_stag[:]/110000+Lat_00
	Lon=x_stag[:]/110000+Lon_00
	Pr=PT[:,:,:,:]*10**-2# Pressure hPa
	# Intergreated QT : Total hydrometeor mixing ratio
	QT=zeros((x_stag.shape[0]-1,y_stag.shape[0]-1))
	for sss in range(0,x_stag.shape[0]-1,1):
		QT[:,sss]=QI[0,:,:,sss].sum(axis=0)+QH[0,:,:,sss].sum(axis=0)+QS[0,:,:,sss].sum(axis=0)+QR[0,:,:,sss].sum(axis=0)+QC[0,:,:,sss].sum(axis=0)

	Hgt=f.variables['ZP'][1,:,:]# Elevation

	# get the latitude, longitude
	Lon1E=y_stag[:].min
	Lon2E=y_stag[:].max
	Lat1N=x_stag[:].min
	Lat2N=x_stag[:].max


	#+++++++++++++++++++++ Colormap
	# define custom color (rgb format)
	lightsteelblue=(202/255,225/255,255/255)
	royalblue=(39/255,64/255,139/255)
	forestgreen=(0/255,50/255,0/255)
	palegreen =(124/255,205/255,124/255)

	#BlBd = cmappytom([lightsteelblue,royalblue])# Blue dark to Blue light
	#Veg_map=cmappytom([forestgreen,palegreen])# Vegetation type colormap

	#++++++++++++++++++++++ END colormap

	#OOOOOO PLOT
	#----- Fig parameter

	# Fig dimension
	screen_width=1920
	screen_height=1080
	DPI=96# (pixel by inches) Resolution of the screen
	wFig=screen_width/DPI #size in inches 
	hFig=screen_height/DPI#
	fig=plt.figure(figsize=(wFig,hFig))
	#fig.tight_layout()
	plt.suptitle(RunName+' ' +Initime_YMD+' '+ str(int(Initime_H)+(hour/3600)-1)+'h',fontsize=20)
	plt.axis([Lon1E(0),Lon2E(0),Lat1N(0),Lat2N(0)])

	# Parameters to plot the wind
	Nbarbs=50 # 1 barbs every Nbarbs (density)
	Lbarbs=5 # length of the barbs


	# create the map of position
	X, Y = np.meshgrid(x_stag[1:], y_stag[1:])

	Up=U[0,13,:,1:]# wind at 5km 
	Vp=V[0,13,1:,:]# wind at 5km 
	Up=Up[::Nbarbs,::Nbarbs]
	Vp=Vp[::Nbarbs,::Nbarbs]
	Sp=np.sqrt(Up**2+Vp**2)
	Xp=X[::Nbarbs,::Nbarbs]# contour Vegetation
	Yp=Y[::Nbarbs,::Nbarbs]

	Up = np.ma.masked_array(Up,Sp==0)# remove low value of wind
	Vp = np.ma.masked_array(Vp,Sp==0)

	# Ticks axis
	Ticks_Lat=[ round(elem, 2) for elem in Lat[1::30] ]
	Ticks_Lon=[ round(elem, 2) for elem in Lon[1::30] ]


	#1)===== Plot Surface Temperature
	Plt1=plt.subplot(2,2,1)
	title=('Surface Temperature(C) + wind-5km')
	plt.title(title)
	print(title)
	# contour land
	CL3=plt.contour(X,Y,Hgt,levels=[0],colors = 'k')

	# contour Temperature Potentiel Surface
	#Tmax=int(PT[0,1,:,:].max())
	#Tmin=int(PT[0,1,:,:].min())
	Tmax=40
	Tmin=2
	NCT=20 # number of temperature contour
	levelsT=np.linspace(Tmin,Tmax,NCT)
	CT1=plt.contourf(X,Y,PT[0,1,:,:],cmap=get_cmap('BuRd'),levels=levelsT)# filed conteur
	#CT1=plt.pcolor(X,Y,PT[0,1,:,:],cmap=get_cmap('BuRd'))# filed conteur

	# Set the ticks label
	CT1.ax.set_xticks( x_stag[1::30])
	CT1.ax.set_xticklabels(Ticks_Lat) 

	CT1.ax.set_yticks( y_stag[1::30])
	CT1.ax.set_yticklabels(Ticks_Lon)

	Cl1=plt.colorbar(CT1)
	Cl1.set_label('Temperature in C')
	# wind barbs
	Cw1=plt.barbs(Xp,Yp,Up,Vp,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))

	#2)===== Plot Humidity Specific Surface
	Plt2=plt.subplot(2,2,2)
	title=('Surface Specific Humidity (kg.kg-1) + wind-5km')
	plt.title(title)
	print(title)

	# contour land
	CL2=plt.contour(X,Y,Hgt,levels=[0],colors = 'k')

	Hmax=2.5*10e-3
	Hmin=2.5*10e-4
	NCH=10 # number of temperature contour
	levelsH=np.linspace(Hmin,Hmax,NCH)
	CT2=plt.contourf(X,Y,Qv[0,1,:,:],cmap=get_cmap('Blues'),levels=levelsH)# filed contour

	Cl2=plt.colorbar(CT2)
	Cl2.set_label('Specific humidity')
	Cl2.ax.set_yticks( levelsH)# axis ticks 
	Cl2.ax.set_yticklabels(levelsH)# axis label


	# change the format of the ticks
	Cl2.formatter.set_scientific(True)
	Cl2.formatter.set_powerlimits((0,4))
	Cl2.update_ticks() 


	# Set the ticks label
	CT2.ax.set_xticks( x_stag[1::30])
	CT2.ax.set_xticklabels(Ticks_Lat) 
	CT2.ax.set_yticks( y_stag[1::30])
	CT2.ax.set_yticklabels(Ticks_Lon)

	# wind barbs
	Cw2=plt.barbs(Xp,Yp,Up,Vp,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))

	#3)===== Plot Total precipitation rate
	Plt3=plt.subplot(2,2,3)
	title=('Totale Precipitation rate (m.s-1) + wind-5km')
	plt.title(title)
	print(title)
	# contour land
	CL3=plt.contour(X,Y,Hgt,levels=[0],colors = 'k')

	# contour elevation
	Chgt1=plt.contourf(X,Y,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/100)),cmap=get_cmap('gist_gray'))
	plt.colorbar(Chgt1)

	# contour Vegetation
	#Vegmax=int(Veg[:,:].max())
	#Vegmin=int(Veg[:,:].min()) 
	#levelsVeg=np.arange(Vegmin,Vegmax,1)

	#CVeg3=plt.contourf(X,Y,Veg[:,:],levels=levelsVeg,cmap=get_cmap('YlGn'))
	#Cl3_veg=plt.colorbar(CVeg3)

	# Set the ticks label
	#CVeg3.ax.set_xticks( x_stag[1::30])
	#CVeg3.ax.set_xticklabels(Ticks_Lat) 

	#CVeg3.ax.set_yticks( y_stag[1::30])
	#CVeg3.ax.set_yticklabels(Ticks_Lon)

	# contour Total precipitation at the surface
	Pt_m=np.ma.masked_where(Pt[0,:,:]==0,Pt[0,:,:])
	#Pmax=Pt[0,:,:].max()
	#Pmin=Pt[0,:,:].min()
	Pmax=5e-2
	Pmin=1e-2
	NCP=10 # number of precepitation contour
	levelsP=np.linspace(Pmin,Pmax,NCP)
	NlevelsP=np.around(levelsP,decimals=4)
	CT3=plt.contourf(X,Y,Pt_m[:,:],cmap=get_cmap('BuRd'),levels=NlevelsP)# filed contour
	Cl3_precep=plt.colorbar(CT3)
	Cl3_precep.set_label('Precipitation rate (m.s-1)')

	# change the format of the ticks
	Cl3_precep.formatter.set_scientific(True)
	Cl3_precep.formatter.set_powerlimits((0,2))
	Cl3_precep.update_ticks() 


	# wind barbs
	Cw1=plt.barbs(Xp,Yp,Up,Vp,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))


	#4)===== Plot total hydrometeors mixing ratio 
	Plt4=plt.subplot(2,2,4)
	title=('Total hydrometeor mixing ratio (kg/kg-1) + wind-5km ')
	plt.title(title)
	print(title)

	# contour land
	CL4=plt.contour(X,Y,Hgt,levels=[0],colors = 'k')

	# contour surface flux of moisture
	#Qvsmax=Qvs[0,:,:].max()
	#Qvsmin=Qvs[0,:,:].min()
	#QVSmax=1.5*1e-5
	#QVSmin=-5*1e-4
	#NCQVS=20 # number of temperature contour
	#levelsQVS=np.linspace(QVSmin,QVSmax,NCQVS)

	#NlevelsQVS=np.around(levelsQVS,decimals=6)

	#CQVS4=plt.contourf(X,Y,Qvs[0,:,:],cmap=get_cmap('pink'),levels=NlevelsQVS)# filed contour
	#Cl4_QVS=plt.colorbar(CQVS4)
	#Cl4_QVS.set_label('Surface flux moisture')

	# change the format of the ticks
	#Cl4_QVS.formatter.set_scientific(True)
	#Cl4_QVS.formatter.set_powerlimits((0,2))
	#Cl4_QVS.update_ticks() 

	# Set the ticks label
	#CQVS4.ax.set_xticks( x_stag[1::30])
	#CQVS4.ax.set_xticklabels(Ticks_Lat) 

	#CQVS4.ax.set_yticks( y_stag[1::30])
	#CQVS4.ax.set_yticklabels(Ticks_Lon)


	# contour elevation
	Chgt1=plt.contourf(X,Y,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/100)),cmap=get_cmap('gist_gray'))
	plt.colorbar(Chgt1)


	# contour Total hydrometeor mixing ratio
	QT_m=np.ma.masked_where(QT<10**-3,QT)

	# contour elevation
	#Chgt1=plt.contourf(X,Y,Hgt,levels=range(Hgt.min(),Hgt.max(),int(Hgt.max()-Hgt.min())/10),cmap=get_cmap('gist_earth'))
	#plt.colorbar(Chgt1)

	# contour Total hydrometeros + mask
	#QT_mmax=QT_m[:,:].max()
	#QT_mmin=QT_m[:,:].min()
	QT_mmax=0.2
	QT_mmin=1*1e-2
	NCQT_m=10 
	levelsQT_m=np.linspace(QT_mmin,QT_mmax,NCQT_m)
	NlevelsQT_m=np.around(levelsQT_m,decimals=4)

	CT4=plt.contourf(X,Y,QT_m,cmap=get_cmap('BuRd'),levels=NlevelsQT_m)# filed contour
	Cl4_Hm=plt.colorbar(CT4)
	Cl4_Hm.set_label('Total mixing ratio (kg/kg-1)')

	# change the format of the ticks
	Cl4_Hm.formatter.set_scientific(True)
	Cl4_Hm.formatter.set_powerlimits((0,2))
	Cl4_Hm.update_ticks() 


	# wind barbs
	Cw1=plt.barbs(Xp,Yp,Up,Vp,length=Lbarbs, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))

	# Correct the axis to be aligned
	pos1 = Plt1.get_position().bounds
	pos2 = Plt2.get_position().bounds
	pos3 = Plt3.get_position().bounds
	pos4 = Plt4.get_position().bounds

	# set the x limits (left and right) to first axes limits
	# set the y limits (bottom and top) to the last axes limits
	newpos1 = [pos3[0],pos2[1],pos3[2],pos2[3]]#[left,bottom,right,top] 
	newpos2 = [pos4[0],pos1[1],pos4[2],pos1[3]]

	Plt1.set_position(newpos1)
	Plt2.set_position(newpos2)

	#----- save the figure in a separate file
	plt.savefig(OutDirPath+filename+'.png',dpi=DPI)
	print('Saving:'+OutDirPath+filename+'.png \n -----------------------\n')



