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
import datetime
import os.path # basename and folder name of a path
import glob # # Import all the file of a folder

class SpecVar():
	Cst={"P0":100000,
		"Rd":287.06,
		"Cp":1004.5,#J/(kg K)
		"Cpd":1004.7,#J/(kg K)
		"Rv":461.52,#
		"Cl":4218,#J/(kg K)
		"Ci":2106,#J/(kg K)
		"Lv":2.501*10**6,#J/Kg
		"g":9.81}

	def __init__(self, arpsobject = None):
		self.module={
			'QT': self.__QT,
			'PTc': self.__PTc,
			'Phpa': self.__Phpa,
			'Pbarhpa': self.__Pbarhpa,
			'Ptot': self.__Ptot,
			'ThetaV': self.__ThetaV,
			'Tk': self.__Tk,
			'Pv': self.__Pv,
			'Pd': self.__Pd,
			'Psat': self.__Psat,
			'Rh': self.__Rh,
			'ThetaE':self.__ThetaE,
			'LatLon':self.__LatLon
		}
		self.attributes= { }
		self.varname={
			'QT':'Total hydrometeors',
			'PTc':'Potential Temperature in degree',
			'Phpa':'Pressure in Hectopascale',
			'Pbarhpa':'Pressure in Hectopascale',
			'Ptot':'Total pressure',
			'ThetaV':'Virtual potential temperature',
			'Tk':'Real temperature in Kelvin',
			'Pv':'Vapor pressur in Pa',
			'Pd':'Dry pressure in Pa',
			'Psat':'Pressure at saturation ',
			'Rh':'relative humidity',
			'ThetaE':'potential equivalent temperature',
			'LatLon':'Vector position [latitude,longitude]'
		}

	def __QT(self, arps, variable):
		"""
		Calculate Total hydrometeors
		"""
		print("Calculate Total hydrometeors")

		QI = arps.get('QI')
		QH = arps.get('QH')
		QR = arps.get('QR')
		QC = arps.get('QC')
		QS = arps.get('QS')

		data=QI.data + QH.data + QR.data + QC.data + QS.data
		result = scipy.io.netcdf.netcdf_variable(data, QI.typecode(), QI.shape, QI.dimensions)
		result.long_name=self.varname['QT']

		return result
	def __PTc(self, arps, variable):
		"""
		Calculate Potential temperature in degree
		"""
		print("Calculate Potential temperature in degree")

		PT=arps.get('PT')
		data=PT.data-273.15
		results=scipy.io.netcdf.netcdf_variable(data,PT.typecode(),PT.shape,PT.dimensions)
		results.long_name=self.varname['PTc']
		results.units='C'
		return results
	def __Phpa(self, arps, variable):
		"""
		Calculate the Pressure in hectopascale
		"""
		print('Calculate the Pressure in Hectopascale')
		P=arps.get('P')
		data=P.data*10**-2
		results=scipy.io.netcdf.netcdf_variable(data,P.typecode(),P.shape,P.dimensions)
		results.long_name=self.varname['Phpa']
		results.units='hpa'
		return results 
	def __Pbarhpa(self, arps, variable):
		"""
		Calculate the Pressure in hectopascale
		"""
		print('Calculate the pressure in hectopascale')
		PBAR=arps.get('PBAR')
		data=PBAR.data*10**-2
		results=scipy.io.netcdf.netcdf_variable(data,PBAR.typecode(),PBAR.shape,PBAR.dimensions)
		results.long_name=self.varname['Pbarhpa']
		results.units='hpa'

		return results
	def __Ptot(self, arps, variable):
		"""
		Calculate the totale Pressure in hectopascale
		"""
		print('calculate the totale pressur in hectopascale') 
		Phpa=arps.get('Phpa')
		Pbarhpa=arps.get('Pbarhpa')
		data=Phpa.data+Pbarhpa.data
		results=scipy.io.netcdf.netcdf_variable(data,Phpa.typecode(),Phpa.shape,Phpa.dimensions)
		results.longname=self.varname['Ptot']

		return results
	def __ThetaV(self, arps, variable):
		"""
		Calculate the virtual potential temperature
		"""
		print("Calculate the virtual potential temperature")
		Eps=self.Cst['Rd']/self.Cst['Rv']

		QT=arps.get('QT')
		PT=arps.get('PT')
		QV=arps.get('QV')
		data=PT.data*((1+(QV.data/Eps))/(1+QT.data))

		results=scipy.io.netcdf.netcdf_variable(data,QT.typecode(),QT.shape,QT.dimensions)
		results.long_name=self.varname['ThetaV']
		results.units='C'

		return results 
	def __Tk(self, arps, variable):
		"""
		Calculate the Real Temperature in Kelvin
		"""
		print("Calculate the Real temperature in Kelvin")
		P=arps.get('P')
		PT=arps.get('PT')
		data=PT.data*(P.data/self.Cst['P0'])**(self.Cst['Rd']/self.Cst['Cp'])
		results=scipy.io.netcdf.netcdf_variable(data,P.typecode(),P.shape,P.dimensions)
		results.long_name=self.varname['Tk']
		results.units='k'

		return results
	def __Pv(self, arps, variable):
		"""
		Calculate the vapor Pressure
		"""
		print('Calculate the partial vapor Pressure')
		QV= arps.get('QV')
		P=arps.get('P')
		data=((QV.data*(P.data))/(0.622+QV.data))
		results=scipy.io.netcdf.netcdf_variable(data,QV.typecode(),QV.shape,QV.dimensions)
		results.long_name=self.varname['Pv']
		results.units='Pa'

		return results
	def __Pd(self, arps, variable):
		"""
		Calculate the partial dry air pressure
		"""
		print('Calculate the partial dry air Pressure')
		Pv=arps.get('Pv')
		P=arps.get('P')
		data=P.data-Pv.data
		results=scipy.io.netcdf.netcdf_variable(data,P.typecode(),P.shape,P.dimensions)
		results.long_name=self.varname['Pd']
		results.units='Pa'

		return results
	def __Psat(self, arps, variable):
		"""
		Calculate vapor pressure at saturation
		CIMO GUIDE , WMO, 2006
		"""
		print('Calculate the vapor pressure at saturation')
		Tk=arps.get('Tk')
		data=6.112*np.exp(17.62*(Tk.data-273.15)/(243.12+(Tk.data-273.15)))*10**2
		results=scipy.io.netcdf.netcdf_variable(data,Tk.typecode(),Tk.shape,Tk.dimensions)
		results .long_name=self.varname['Psat']

		return results
	def __Rh(self, arps, variable):
		"""
		Calculate the relative humidity
		"""
		print('Calculate the relative humidity')
		Pv=arps.get('Pv')
		Psat=arps.get('Psat')
		data=(Pv.data/Psat.data)*100
		results=scipy.io.netcdf.netcdf_variable(data,Pv.typecode(),Pv.shape,Pv.dimensions)
		results.long_name=self.varname['Rh']
		results.units='%'

		return results
	def __ThetaE(self, arps, variable):
		"""
		Calculate the Equivalent Potential Temperature
		"""
		print('Calculate the Equivalent Potential Temperature')
		QT=arps.get('QT')
		Tk=arps.get('Tk')
		Pd=arps.get('PD')
		QV=arps.get('QV')
		Rh=arps.get('Rh')
		rtc=QT.data*self.Cst['Cl']# Total hydrometeor 
		First=Tk.data*(self.Cst['P0']/Pd.data)**(self.Cst['Rd']/(self.Cst['Cpd']+rtc))
		Second=Rh**((-QV.data*self.Cst['Rv'])/(self.Cst['Cpd']+rtc))
		Third=np.exp((self.Cst['Lv']*QV.data)/((self.Cst['Cpd']+rtc)*Tk.data))
		data=First*Second*Third
		results=scipy.io.netcdf.netcdf_variable(data,QV.typecode(),QV.shape,QV.dimensions)
		results.long_name=self.varname['ThetaE']
		results.units='k'

		return results
	def __LatLon(self, arps, variable):
		"""
		Calculate the matrix latitude longitude of the domain
		based on a Lambert conformal conic projection 
		"""
		try:
			from pyproj import Proj
		except ImportError:
			print('Cant find the module pyproj')

		truelat1=arps.getatt('TRUELAT1')
		truelat2=arps.getatt('TRUELAT2')
		ctrlat=arps.getatt('CTRLAT')
		ctrlon=arps.getatt('CTRLON')
		x_stag=arps.get('x_stag')
		y_stag=arps.get('y_stag')

		pnyc = Proj(proj='lcc',datum='WGS84',lat_1=truelat1,lat_2=truelat2,lat_0=ctrlat,lon_0=ctrlon)
		Lon_arps,Lat_arps= pnyc(x_stag[1:]-(x_stag[:].max())/2,y_stag[1:]-(y_stag[:].max())/2, inverse=True)
		
		results={ }
		results['Lon']=scipy.io.netcdf.netcdf_variable(Lon_arps,y_stag.typecode(),y_stag.shape[0]-1,y_stag.dimensions)
		results['Lat']=scipy.io.netcdf.netcdf_variable(Lat_arps,x_stag.typecode(),x_stag.shape[0]-1,x_stag.dimensions)
		results['Lat'].long_name=self.varname['LatLon']
		results['Lon'].long_name=self.varname['LatLon']
		return results 

class BaseVars():
	def __init__(self, InPath):
		f = netcdf.netcdf_file(InPath, 'r')
		self.__dict__ = f.__dict__.copy() # copy the attributs of the object
		self.__dict__['data'] = f.variables
		del(self.variables)

		self.module = { }
		self.attributes = {
			"InPath":InPath,
			"dirname":os.path.dirname(InPath),
			"basename":os.path.basename(InPath)
		}
		self.varname = { }
		
		for var in self.data.iterkeys():
			self.module[var] = self.get
			self.varname[var]= self.data[var].long_name

		for att in f._attributes:
			self.attributes[att] = f._attributes[att]
			
	def get(self, arps, variable):
		return self.data[variable]

class arps():
	def __init__(self):
		self.__knowvariables = { }
		self.__cachedata = { }
		self.__attributes = { }
		self.__varname = { }

	def load(self, plugin):
		for (k,v) in plugin.module.iteritems():
			if k in self.__knowvariables:
				print >>sys.stderr,"%s is already know." % k
			self.__knowvariables[k] = v
		for (k,v) in plugin.attributes.iteritems():
			if k in self.__attributes:
				print >>sys.stderr,"%s is already know." % k
			self.__attributes[k] = v
		for (k,v) in plugin.varname.iteritems():
			if k in self.__varname:
				print >>sys.stderr,"%s is already know." % k
			self.__varname[k] = v
	def get(self, variable):
		try:
			data = self.__cachedata[variable]
			return data
		except KeyError, e:
			try:
				fn = self.__knowvariables[variable]
				data = fn(self, variable)

#               remove caching
# 				return data

				self.__cachedata[variable] = data
			except KeyError,e:
				print >>sys.stderr, "%s is not know,\n%s" % (variable, str(e))
				return None
		return self.__cachedata[variable]	
	def remove(self,variable):
		try:
			del self.__knowvariables[variable]
			del self.__cachedata[variable]
		except KeyError,e:
			print('The variable is not known')
	def showvar(self):
		for i in self.__varname:
			print(i+':'+' '*5+str(self.__varname[i]))
	def showatt(self):
		for i in self.__attributes:
			print(i+':'+' '*5+str(self.__attributes[i]))
	def getatt(self,attribute):
		try:
			att=self.__attributes[attribute]
			return att
		except KeyError:
			print('This attribute is not know')
	def addatt(self,attribute,value):
		self.__attributes[attribute]=value

class ArpsFigures():
	def __init__(self,arps):
		self.para= { }
		self.paradef= {
			'OutPath':'/home/thomas/',
			'screen_width':1920,
			'screen_height':1080,
			'DPI':96,
			'Latmin':self.arps.get('LatLon')['Lat'].data.min(),
			'Latmax':self.arps.get('LatLon')['Lat'].data.max(),
			'Lonmin':self.arps.get('LatLon')['Lon'].data.min(),
			'Lonmax':self.arps.get('LatLon')['Lon'].data.max(),
			'Altmin':self.arps.get('z_stag').data[1],
			'Altmax':self.arps.get('z_stag').data[:],
			'Altcross':0
			}
		self.__figwidth()
		self.__subtitle(arps)
		self.arps=arps # Es ce que ca duplique les donnés de arps ?????????????	
	def __figwidth(self):
		width=self.getpara('screen_width')
		height=self.getpara('screen_height')
		DPI=self.getpara('DPI')
		wfig=width/DPI #size in inches 
		hfig=height/DPI
		self.setpara('wfig',wfig)
		self.setpara('hfig',hfig)
	def __subtitle(self,arps):
		"""
		Write the subtitle of the plot
		"""
		basename=arps.getatt('basename')
		self.setpara('subtitle', basename)
	def setpara(self,parameter,value):
		self.para[parameter]=value
		print(str(parameter)+'  '+ str(value))
	def getpara(self,parameter):
		try:
			return self.para[parameter]
		except KeyError:
			print(parameter + ' has been not set -> Default value used ['+str(self.paradef[parameter])+']')
			try:
				return self.paradef[parameter]
			except KeyError:
				print(parameter+ ' dont exist')
	def __levels(self,varname):
		self.paradef['nlevel']=10# number of discrete variabel level
		self.paradef['varmax']=int(self.arps.get(varname).data.max())
		self.paradef['varmin']=int(self.arps.get(varname).data.min())
		varmax=self.getpara('varmax')
		varmin=self.getpara('varmin')
		nlevel=self.getpara('nlevel')
		levels=np.linspace(varmin,varmax,nlevel)
		return levels
	def getvar(self,varname):
		"""
		This module select data on the needed domain
		"""
		data=self.arps.get(varname).data
		dimensions=self.arps.get(varname).dimensions
		Lonmin=self.getpara('Lonmin')
		Lonmax=self.getpara('Lonmax')
		Latmin=self.getpara('Latmin')
		Latmax=self.getpara('Latmax')
		Altcross=self.getpara('Altcross')
		Lat=self.arps.get('LatLon')['Lat'].data
		Lon=self.arps.get('LatLon')['Lon'].data
		Alt=self.arps.get('z_stag').data[:]
		ILatmin=min(range(len(Lat)), key=lambda i: abs(Lat[i]-Latmin))
		ILatmax=min(range(len(Lat)), key=lambda i: abs(Lat[i]-Latmax))+1
		ILonmin=min(range(len(Lon)), key=lambda i: abs(Lon[i]-Lonmin))
		ILonmax=min(range(len(Lon)), key=lambda i: abs(Lon[i]-Lonmax))+1
		IAltcross=min(range(len(Alt)), key=lambda i: abs(Alt[i]-Altcross))
		print(Lonmin)
		print(Lonmax)
		print(ILatmax)
		print(ILatmin)
		self.setpara('NewLat',Lat[ILatmin:ILatmax])
		self.setpara('NewLon',Lon[ILonmin:ILonmax])
		print(varname+'  have '+str(dimensions)+'  dimensions')
		print('Latitude selected -> [' + str(Latmin) + ' - '+ str(Latmax)+ '] Nearest Indices ['+str(ILatmin)+' - '+str(ILatmax)+ ']')
		print('Longitude selected ->  ['+ str(Lonmin) + ' - '+ str(Lonmax)+ ']  Nearest Indices ['+str(ILonmin)+' - '+str(ILonmax)+ ']')
		print('Altitude selected ->  ['+ str(Altcross)+ '] Nearest Indices' +'['+str(IAltcross)+ ']')
		if shape(dimensions)[0] == 4:
			try:
				Ndata=data[0,IAltcross, ILatmin : ILatmax,ILonmin : ILonmax]
				self.paradef['varmax']=Ndata.max()
				self.paradef['varmin']=Ndata.min()
				return Ndata
			except:
				print('Cannot access the data')
		if shape(dimensions)[0]==3:
			print('3 dimensions --------------------')
			try:
				Ndata=data[0, ILatmin : ILatmax,ILonmin : ILonmax]
				self.paradef['varmax']=Ndata.max()
				self.paradef['varmin']=Ndata.min()
				return Ndata
			except:
				print('Cannot access the data')
	def contourf(self,varname):
		var=self.getvar(varname)
		print(var)
		X=self.getpara('NewLon')
		Y=self.getpara('NewLat')
		print(X.shape)
		print(Y.shape)
		print(X)
		print(Y)
		print(var.shape)
		levels=self.__levels(varname)
		plot=plt.contourf(X,Y,var,cmap=get_cmap('BuRd'),levels=levels)
		return plot
	def contour(self,varname):
		var=self.getvar(varname)
		X=self.getpara('NewLon')
		Y=self.getpara('NewLat')
		print(X)
		print(Y)
		print(X.shape)
		print(Y.shape)
		print(var.shape)
		levels=self.__levels(varname)
		plot=plt.contour(X,Y,var,levels=levels,cmap=get_cmap('gist_gray'))
		return plot
	def windvector(self):
		"""
		x: vector position horizontal length (n)
		y: vector position vertical length (m)
		U: matrix zonal wind shape (m*n)
		V: matrix meridional wind shape (m*n)
		"""
		self.paradef['Nbarb']=10
		self.paradef['Lbarb']=5
		Nbarb=self.getpara('Nbarb')
		Lbarb=self.getpara('Lbarb')
		U=self.getvar('U')
		V=self.getvar('V')
		x=self.getpara('NewLon')
		y=self.getpara('NewLat')
		X, Y = np.meshgrid(x,y)
		print("U shape"+str(U.shape))
		print("V shape"+str(V.shape))
		print("Y shape"+str(Y.shape))
		print("X shape"+str(X.shape))
		if X.shape != U.shape and Y.shape != V.shape:
			print('x * y does not equal to U or V')
		Up=U[::Nbarb,::Nbarb]
		Vp=V[::Nbarb,::Nbarb]
		Xp=X[::Nbarb,::Nbarb]
		Yp=Y[::Nbarb,::Nbarb]
		#plot=plt.barbs(Xp,Yp,Up,Vp,length=Lbarb, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))
		plot=plt.quiver(Xp,Yp,Up,Vp)
		return plot

class stations():
	# 	###################################
	# 	# Position of the Stations
	# 	###################################
	# 	StaPosFile="/home/thomas/PhD/obs-lcb/staClim/LatLonSta.csv"
	# 	StaPos={}
	# 	with open (StaPosFile) as StaPosF:
	# 		reader_IAC=csv.reader(StaPosF,delimiter=",")
	# 		header_IAC=reader_IAC.next()
	# 		for h in header_IAC:
	# 			StaPos[h]=[]
	# 		for row in reader_IAC:
	# 			for h,v in zip(header_IAC,row):
	# 				StaPos[h].append(v)
	# 
	# 	Lat=np.array(Lat)
	# 	Lon=np.array(Lon)
	# 	LatStaI=[]
	# 	LonStaI=[]
	# 	LatSta=[]
	# 	LonSta=[]
	# 	StaName=[]
	# 	for ista,sta in enumerate(StaPos['Posto']):
	# 		print('open station=> '+sta)
	# 		LatI=np.searchsorted(Lat,float(StaPos['Lat '][ista]), side="left")
	# 		LonI=np.searchsorted(Lon,float(StaPos['Lon'][ista]), side="left")
	# 		if LatI!=0 and LonI!=0:
	# 			LatSta=LatSta+[float(StaPos['Lat '][ista])]# Use in compareGFS_OBS.py
	# 			LonSta=LonSta+[float(StaPos['Lon'][ista])]#Use in compareGFS_OBS.py
	# 			LatStaI=LatStaI+[LatI]
	# 			LonStaI=LonStaI+[LonI]
	# 			StaName=StaName+[StaPos['Posto'][ista]]
	# 			print("In map => "+ StaPos['Posto'][ista] +" at "+ str(LatI) +" and " +str(LonI))
	pass



#------------------------------------------------------------------------------ 
#	Horizontal plot (variable, topography and wind vector)
#------------------------------------------------------------------------------ 
InPath="/dados1/sim/out300m_021114_V2/"
Files=glob.glob(InPath+"*")
Files.sort()
for Path in Files:
	print(Path)
	ARPS = arps()
	BASE = BaseVars(Path)
	SPEV = SpecVar()
	ARPS.load(BASE)
	ARPS.load(SPEV)
	FIG=ArpsFigures(ARPS)
	fig=plt.figure(figsize=(FIG.getpara('wfig'),FIG.getpara('hfig')))
	plt.suptitle(FIG.getpara('subtitle'),fontsize=20)
	FIG.setpara('Latmin',-22.90)
	FIG.setpara('Latmax',-22.80, )
	FIG.setpara('Lonmin',-46.30)
	FIG.setpara('Lonmax',-46.20)
	FIG.setpara('Altcross',0)
	FIG.setpara('nlevel',100)
	FIG.setpara('varmin',288)
	FIG.setpara('varmax',298)
	FIG.contourf('Tk')
	plt.colorbar()
	FIG.setpara('varmin',1000)
	FIG.setpara('varmax',2000)
	FIG.setpara('nlevel',200)
	CS=FIG.contour('ZP')
	CS.ax.grid(True, zorder=0)
	plt.clabel(CS, inline=10, fontsize=15,fmt='%4.f',)
	FIG.setpara('Nbarb',1)
	FIG.setpara('Altcross',0)
	FIG.windvector()
	plt.savefig('control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'))
	plt.close()


