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
#		V2.2 -> New vertical cross Section with more detail
#		V2.3 -> Vertical cross sction NS + distance selection
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
InputDirPath='/home/thomas/PhD/arps/sim/140214/out300m_V9_netcdf/'# path for the input netCDF file 
OutDirPath='/home/thomas/PhD/arps/res/fig_14-02-14/V9/NS/' # path for the output grahics

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
	QS=f.variables['QS']# Snow ixing ratio 
	QR=f.variables['QR']#Rain mixing ratio 
	QC=f.variables['QC']#Cloud mixing ratio
	U=f.variables['U']# wind
	V=f.variables['V']# wind 
	Hgt=f.variables['ZP'][0,:,:]# Elevation
	ZP=f.variables['ZP'][:,:,:]#Altitude of the point
	#------ Transform variable
	Lon_00=CtrLon-((len(y_stag[:])-1)/2)*(Dy/(110*1000))# Position du point en bas a droite
	Lat_00=CtrLat-((len(x_stag[:])-1)/2)*(Dx/(110*1000))# !!!!! jai approximer avec 110 km par degree!!! trouver une meilleur approximation
	Lat=y_stag[:]/110000+Lat_00
	Lon=x_stag[:]/110000+Lon_00

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


	##########################################
	#	Specific variable
	##########################################
	#------Constant
	P0=100000
	Rd= 287.06
	Cp=1004.5#J/(kg K)
	Cpd=1004.7#J/(kg K)
	Rv=461.52#
	Cl =4218#J/(kg K)
	Ci =2106#J/(kg K)
	Lv=2.501*10**6#J/Kg
	g=9.81#

	#%rtc=(THi.*(Cl+Ci))+THl.*Cl; # VErify THIS
	rtc=QT*Cl# Total hydrometeor 
	Eps=Rd/Rv#

	#-------- Potential Virtual Temperature
	ThetaV=(PTk[:,:,:,:]*((1+(Qv[:,:,:,:]/Eps))/(1+QT)))

	#-------- Buoyancy
	#Oe=g*((PVT-IOe)./IOe);

	#-------- Real Temperature
	RTk=PTk[:,:,:,:]*(Pr*10**2/P0)**(Rd/Cp);

	#-------- Partial Pressure
	#vapor
	Prv=((Qv[:,:,:,:]*(Pr*10**2))/(0.622+Qv[:,:,:,:]))
	#Dry air
	Prd=Pr*10**2-Prv

	#---------Saturation vapor pressure------
	#with T in c
	#Ps (kPa)
	# CIMO GUIDE , WMO, 2006
	Prs=6.112*np.exp(17.62*(RTk-273.15)/(243.12+(RTk-273.15)))*10**2

	#------Relative Humidity--------
	H=(Prv/Prs)*100

	#-------Equivalent potential temperature
	First=RTk*(P0/Prd)**(Rd/(Cpd+rtc))
	Second=H**((-Qv[:,:,:,:]*Rv)/(Cpd+rtc))
	Third=np.exp((Lv*Qv[:,:,:,:])/((Cpd+rtc)*RTk))
	ThetaE=First*Second*Third



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
	Nbarbs=100 # 1 barbs every Nbarbs (density)
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
	# Put 0 on the cross section that you don't want
	Sens='NS'# NS for Nord Sud OR EW for East West
	LatCS1=-23.17#-22.35
	LatCS2=-22.52#-21.7
	LonCS1=-46.0#-46.3#
	LonCS2=-46.0#-46.3#

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
	LatSta=[]
	LonSta=[]
	StaName=[]
	for ista,sta in enumerate(StaPos['Posto']):
		print('open station=> '+sta)
		LatI=np.searchsorted(Lat,float(StaPos['Lat '][ista]), side="left")
		LonI=np.searchsorted(Lon,float(StaPos['Lon'][ista]), side="left")
		if LatI!=0 and LonI!=0:
			LatSta=LatSta+[float(StaPos['Lat '][ista])]# Use in compareGFS_OBS.py
			LonSta=LonSta+[float(StaPos['Lon'][ista])]#Use in compareGFS_OBS.py
			LatStaI=LatStaI+[LatI]
			LonStaI=LonStaI+[LonI]
			StaName=StaName+[StaPos['Posto'][ista]]
			print("In map => "+ StaPos['Posto'][ista] +" at "+ str(LatI) +" and " +str(LonI))


	##################################
	#	Horizontal  plot
	###################################
	#1)===== Plot Surface Temperature
	Plt1=plt.subplot(2,2,1)
	title=('Surface Temperature (K)')
	plt.title(title)
	print(title)

	# create the map of position


	# contour land
	CL3=plt.contour(X,Y,Hgt,levels=[0],colors = 'k')

	# contour Temperature Potentiel Surface
	#Tmax=int(PT[0,1,:,:].max())
	#Tmin=int(PT[0,1,:,:].min())
	Tmax=310
	Tmin=280
	NCT=300 # number of temperature contour
	levelsT=np.linspace(Tmin,Tmax,NCT)


	CT1=plt.contourf(X,Y,RTk[0,1,:,:],cmap=get_cmap('BuRd'),levels=levelsT)# filed conteur
	#CT1=plt.pcolor(X,Y,PT[0,1,:,:],cmap=get_cmap('BuRd'))# filed conteur

	Chgt1=plt.contour(X,Y,Hgt,levels=range(int(300),int(Hgt.max()),int((Hgt.max()-Hgt.min())/20)),cmap=get_cmap('gist_gray'))
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
	scatter(np.array(LonStaI)*Dx,np.array(LatStaI)*Dy,marker='o',c='r',s=20)
	####################################
	#	Coordinate Cross Section
	###################################
	if Sens == 'NS':
		ICS_Lat=range((np.searchsorted(Lat,LatCS1, side="left")+1),(np.searchsorted(Lat,LatCS2, side="left")+1))
		ICS_Lon=np.searchsorted(Lon,LonCS1, side="left")+1
		CrossPosI_Lat=[y_stag[ICS_Lat[0]],y_stag[ICS_Lat[-1]]]
		CrossPosI_Lon=[y_stag[ICS_Lon]]*2
		X, Y = np.meshgrid(y_stag[ICS_Lat], range(47))
	else:
		ICS_Lon=range((np.searchsorted(Lon,LonCS1, side="left")+1),(np.searchsorted(Lon,LatCS2, side="left")+1))
		ICS_Lat=np.searchsorted(Lat,LatCS1, side="left")+1
		CrossPosI_Lon=[x_stag[ICS_Lon[0]],x_stag[ICS_Lon[-1]]]
		CrossPosI_Lat=[x_stag[ICS_Lat]]*2
		X, Y = np.meshgrid(x_stag[ICS_Lon], range(47))

	#===== Plot station Position
	for i,txt in enumerate(StaName):
		annotate(txt,(np.array(LonStaI[i])*Dx,np.array(LatStaI[i])*Dy),fontsize=10)

	#====== Plot Cross Section position 
	plt.plot(CrossPosI_Lon,CrossPosI_Lat,'--r',lw=3)

	# Axis limits
	plt.xlim(x_stag[1:].min(),x_stag[1:].max())
	plt.ylim(y_stag[1:].min(),y_stag[1:].max())



	##################################
	#	Vertical plot
	###################################
	#1)===== Equivalent Potential temperature
	Plt1=plt.subplot(2,2,3)
	title=('Equivalent Potential Temperature (K)')
	plt.title(title)

	print(title)

	ElevMax=25
	ZZ=(ZP[1:,ICS_Lat,ICS_Lon]+ZP[:-1,ICS_Lat,ICS_Lon])/2# compute the elevation 
	PP=ThetaE[0,:,ICS_Lat,ICS_Lon].T
	OO=QT[0,:,ICS_Lat,ICS_Lon].T


	Tmax=360
	Tmin=310
	NCT=300 # number o
	levelsT=np.linspace(Tmin,Tmax,NCT)
	CT1=plt.contourf(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BdRd'),levels=levelsT)
	#CT1=plt.pcolor(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BuRd'))

	# Set the ticks label
	CT1.ax.set_xticks(map(int,X[1,::100]))
	CT1.ax.set_xticklabels(map(int,X[1,::100])) 

	CT1.ax.set_yticks(map(int,ZZ[:ElevMax,0]))
	CT1.ax.set_yticklabels(map(int,ZZ[:ElevMax,0]))

	Cl1=plt.colorbar(CT1)
	Cl1.set_ticks(map(int,np.linspace(Tmin,Tmax,10)), update_ticks=True)
	Cl1.set_ticklabels(map(int,np.linspace(Tmin,Tmax,10)),update_ticks=True)
	Cl1.set_label('Temperature in C')

	plt.contour(X[:ElevMax,:],ZZ[:ElevMax,:],OO[:ElevMax,:])
	#3)===== Potential temperature
	Plt1=plt.subplot(2,2,2)
	title=('Specific humidity (K)')
	plt.title(title)

	print(title)

	ElevMax=25
	ZZ=(ZP[1:,ICS_Lat,ICS_Lon]+ZP[:-1,ICS_Lat,ICS_Lon])/2# compute the elevation 
	PP=Qv[0,:,ICS_Lat,ICS_Lon].T

	Hmax=2.5*10e-3
	Hmin=2.5*10e-4
	NCH=50 # number of humidity contour
	levelsT=np.linspace(Hmin,Hmax,NCH)
	CT1=plt.contourf(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BdRd'),levels=levelsT)
	#CT1=plt.pcolor(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BuRd'))

	# Set the ticks label
	CT1.ax.set_xticks(map(int,X[1,::100]))
	CT1.ax.set_xticklabels(map(int,X[1,::100])) 

	CT1.ax.set_yticks(map(int,ZZ[:ElevMax,0]))
	CT1.ax.set_yticklabels(map(int,ZZ[:ElevMax,0]))

	Cl1=plt.colorbar(CT1)
	#Cl1.set_ticks(map(int,np.linspace(Hmin,Hmax,10)), update_ticks=True)
	#Cl1.set_ticklabels(map(int,np.linspace(Hmin,Hmax,10)),update_ticks=True)
	Cl1.set_label('Humidity in kg/kg')


	#4)===== Real temperature
	Plt1=plt.subplot(2,2,4)
	title=('Real Temperature (K)')
	plt.title(title)

	print(title)

	ElevMax=25
	ZZ=(ZP[1:,ICS_Lat,ICS_Lon]+ZP[:-1,ICS_Lat,ICS_Lon])/2# compute the elevation 
	PP=RTk[0,:,ICS_Lat,ICS_Lon].T

	QT_mmin=5*1e-4
	Tmax=310
	Tmin=250
	NCT=300 # number of temperature contour
	levelsT=np.linspace(Tmin,Tmax,NCT)
	CT1=plt.contourf(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BdRd'),levels=levelsT)
	#CT1=plt.pcolor(X[:ElevMax,:],ZZ[:ElevMax,:],PP[:ElevMax,:],cmap=get_cmap('BuRd'))

	# Set the ticks label
	CT1.ax.set_xticks(map(int,X[1,::100]))
	CT1.ax.set_xticklabels(map(int,X[1,::100])) 

	CT1.ax.set_yticks(map(int,ZZ[:ElevMax,0]))
	CT1.ax.set_yticklabels(map(int,ZZ[:ElevMax,0]))

	Cl1=plt.colorbar(CT1)
	Cl1.set_ticks(map(int,np.linspace(Tmin,Tmax,10)), update_ticks=True)
	Cl1.set_ticklabels(map(int,np.linspace(Tmin,Tmax,10)),update_ticks=True)
	Cl1.set_label('Temperature in C')


	plt.savefig(OutDirPath+filename+'.png',dpi=DPI)
	print('Saving:'+OutDirPath+filename+'.png \n -----------------------\n')

	#plt.show()


	# Next Time
	hour=int(hour)+int(ResoH) # change the hour for the next file to be open
	filename=Pref+Date[:-len(str(hour))]+str(hour)








