#       DESCRIPTION


#               Import the different station from IAC, INMET and Sinda and write as an input for ADAS

#	VERSION	3
#		
#			Spatio/temporal graph of the difference between gfs and Obs
# 	IMPORTANT
#		INMET 
#			!!! In the data file the direction and the velocity of the wind are switched !!
#			This program take into account this program		
#		Sinda
#	 		-> Les informations des station sinda doivent etre mise manuelement a la ligne!!!
#		IAC
#			Still need to check the position of the IAC station As well as the Altitude
#	
#	Information about
#		Radiation
#			Due to strange value the data of radiation are not included both for INMET and SINDA
#		INMET
#			Radiacion was in cal/(s.mm2)*2.4=w/m2

#=====================================================================================================
#=====================
#===== Library
#=====================
import csv
import numpy as np
from __future__ import division
import os
import datetime
import re # To find character in a string
import matplotlib.pyplot as plt
import pandas as pd
from scipy.io import netcdf
from colour import Color
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

#=====================
#===== User Imput
#=====================

#-----Input Path 
IP_INMET="/home/thomas/PhD/obs-lcb/staClim/INMET/"# INMET 
IP_sinda="/home/thomas/PhD/obs-lcb/staClim/sinda/"# SINDA
IP_IAC="/home/thomas/PhD/obs-lcb/staClim/IAC/data/"# IAC
IP_IAC_stainfo="/home/thomas/PhD/obs-lcb/staClim/IAC/stainfo_V2.csv"#IAC station metadata

#-----Simulation date
hour='12'# obs hour
dateNeed='14/02/2014'# obs date

#----- Output
OutFilename='surface'#outfile name 
OutDirPath='/home/thomas/PhD/arps/obs/AdasInput/'# Out file path 
infosta='stainfo'# file name of the station information

#=====================
#===== IMPORT DATA
#=====================

# Goes through the files and put the variable in a dictionary [station]>[Month]>[variable]
#----- INMET STATION NETWORK
data_INMET = {}
for dirname  in os.walk(IP_INMET).next()[1]:
        data_INMET[dirname]={}
        for subdirname in os.walk(IP_INMET+dirname).next()[1]:
                data_INMEplt.plot(y_new,x_new)T[dirname][subdirname]={}
		data_INMET[dirname][os.walk(IP_INMET+dirname).next()[2][0]]={}#get info from the station
		#data_INMET[dirname][os.walk(IP_INMET+dirname).next()[2][1]]
		with open (IP_INMET+dirname+"/"+os.walk(IP_INMET+dirname).next()[2][0]) as readinfo:
			readerinfo=csv.reader(readinfo,delimiter=":")
			for row in readerinfo:
				if row[0]=='Latitude':data_INMET[dirname][os.walk(IP_INMET+dirname).next()[2][0]]["Latitude"]=row[1][1:8]
				if row[0]=='Longitude':data_INMET[dirname][os.walk(IP_INMET+dirname).next()[2][0]]["Longitude"]=row[1][1:8]
				if row[0]=='Altitude':data_INMET[dirname][os.walk(IP_INMET+dirname).next()[2][0]]["Altitude"]=row[1][1:-7]	
                for filename in os.walk(IP_INMET+dirname+"/"+subdirname).next()[2]:
                        if filename.find("~")==-1:#avoid backup file from gedit
				data_INMET[dirname][subdirname][filename]={}
                        	with open(IP_INMET+dirname+"/"+subdirname+"/"+filename, 'r') as csvfile_INMET:
                                	reader_INMET=csv.reader(csvfile_INMET)
                                	header_INMET=reader_INMET.next()
                                	for h in header_INMET:
                                        	data_INMET[dirname][subdirname][filename][h]=[]
           	               	      	for row in reader_INMET:
                	                        for h,v in zip(header_INMET,row):
                        	                        data_INMET[dirname][subdirname][filename][h].append(v)

#----- SINDA STATION  NETWORK
data_sinda={}
for dirname  in os.walk(IP_sinda).next()[1]:
	data_sinda[dirname]={}
	for subdirname in os.walk(IP_sinda+dirname).next()[1]:
		data_sinda[dirname][subdirname]={}
		data_sinda[dirname][os.walk(IP_sinda+dirname).next()[2][0]]={}
		with open (IP_sinda+dirname+"/"+os.walk(IP_sinda+dirname).next()[2][0]) as readinfo:
			readerinfo=csv.reader(readinfo,delimiter=":")
			for row in readerinfo:
				 if row[0]=='Latitude':data_sinda[dirname][os.walk(IP_sinda+dirname).next()[2][0]]["Latitude"]=row[1][1:7]
				 if row[0]=='Longitude':data_sinda[dirname][os.walk(IP_sinda+dirname).next()[2][0]]["Longitude"]=row[1][1:7]
				 if row[0]=='Altitude':data_sinda[dirname][os.walk(IP_sinda+dirname).next()[2][0]]["Altitude"]=row[1][1:-3]
		for filename in os.walk(IP_sinda+dirname+"/"+subdirname).next()[2]:
			if filename.find("~")==-1:#avoid backup file from gedit
				data_sinda[dirname][subdirname][filename]={}
				with open(IP_sinda+dirname+"/"+subdirname+"/"+filename, 'r') as csvfile_sinda:
					reader_sinda=csv.reader(csvfile_sinda,delimiter="\t")
					header_sinda=reader_sinda.next()
					for h in header_sinda:					
						data_sinda[dirname][subdirname][filename][h]=[]
					for row in reader_sinda:
						for h,v in zip(header_sinda,row):
							data_sinda[dirname][subdirname][filename][h].append(v)


#----- IAC STATION NETWORK
#The structure of the IAC network is modify to correspond to the structure of the INMET and Sinda network
#Read Stainfo
stainfo={}
with open (IP_IAC_stainfo) as stainfo_IAC:
	reader_IAC=csv.reader(stainfo_IAC,delimiter=",")
	header_IAC=reader_IAC.next()
	for h in header_IAC:
		stainfo[h]=[]
	for row in reader_IAC:
		for h,v in zip(header_IAC,row):
			stainfo[h].append(v)

#Read IAC data
data_IAC={}
for filename in os.walk(IP_IAC).next()[2]:
	data_IAC[filename]={'data':{'data':{}}}#To follow the structure of the INMET AND SINDA where there is a file for "each" month
	with open (IP_IAC+filename) as csvfile_IAC:
		print('open--->'+filename)
		reader_IAC=csv.reader(csvfile_IAC,delimiter=",")
		header_IAC=reader_IAC.next()
		index=stainfo['id'].index(re.findall('\d+', filename)[0])
		data_IAC[filename]['stainfo']={'ID':re.findall('\d+', filename),'Latitude':stainfo['Lat '][index],'Longitude':stainfo['Lon'][index],'Name':stainfo['Posto'][index],'Altitude':stainfo['Alt'][index]}
		for h in header_IAC:
			data_IAC[filename]['data']['data'][h]=[]
			print(h)
		for row in reader_IAC:
			for h,v in zip(header_IAC,row):
				data_IAC[filename]['data']['data'][h].append(v)
		


##########################################################################################################################################
##########################################################################################################################################


#===== Temperature of February Sinda
data={'data_INMET':data_INMET,'data_sinda':data_sinda,'data_IAC':data_IAC}
#data={'data_sinda':data_sinda}
#data={'data_INMET':data_INMET}
#data={'data_IAC':data_IAC}


Date = pd.date_range('2014-02-01-03', '2014-02-28', freq='1H')

UTC=3
LonLim=[-47.35,-45.06]
LatLim=[-23.5,-21.21]
DATA=pd.DataFrame(index=Date)
PosSta={}
for Net in data:
	for idx,sta in enumerate(data[Net]):
		print(sta)
		for month in data[Net][sta]:
			if month != infosta:
				print(month)
				File=data[Net][sta][month].keys()[0]
				
				dateIndex=pd.to_datetime([datetime.datetime.strptime(data[Net][sta][month][File][varname[Net]['date']][x]+FormatDate2(Net,x), FormatDateNet[Net]) for x in range(len(data[Net][sta][month][File][varname[Net]['date']])) ])
				if set(Date).intersection(dateIndex) != set([]):
					if LatLim[0] < float(data[Net][sta]['stainfo'][varname[Net]['Latitude']]) < LatLim[1] and LonLim[0] < float(data[Net][sta]['stainfo'][varname[Net]['Longitude']]) < LonLim[1]:
						DATA=DATA.join(pd.DataFrame(data[Net][sta][month][File][varname[Net]['T']],index=dateIndex,columns=[sta+month]))
						PosSta[sta+month]={'Lat':data[Net][sta]['stainfo'][varname[Net]['Latitude']],'Lon':data[Net][sta]['stainfo'][varname[Net]['Longitude']],'Alt':conv[Net]['elev'](data[Net][sta]['stainfo'][varname[Net]['Altitude']]),'Net':Net}
				

#Drop duplicates
DATA['Date']=DATA.index
DATA=DATA.drop_duplicates(cols='Date')
del DATA['Date']


FormatDateNet={'data_INMET':'%d/%m/%Y%H','data_sinda':'%Y-%m-%d %H:%M:%S.0','data_IAC':'%Y-%m-%d %H:%M:%S'}

def FormatDate2(var,var2):
	hour=''
	if var=='data_INMET':
		hour=data[Net][sta][month][File]['hora'][var2]
	return hour



def difference(a, b):
    return list(set(b).difference(set(a))) 

#############################################################################################
########## READ GFS NETCDF###################################################################

InputDirPath='/home/thomas/PhD/obs-lcb/gfs/140214/netcdf/'
from os import listdir
from os.path import isfile, join
import scipy.interpolate
files = sorted([ f for f in listdir(InputDirPath) if isfile(join(InputDirPath,f)) ])

GFS_DATA=pd.DataFrame(index=Date)
GFS_Snd=pd.DataFrame()

for idxf,File in enumerate(files):
	GFS_T=pd.DataFrame()
	f = netcdf.netcdf_file(InputDirPath+File, 'r')
	#print(InputDirPath+File)
	Date_Gfs=pd.to_datetime(datetime.datetime.strptime(File,'fnl_%Y%m%d_%H_%M_c.nc')- datetime.timedelta(hours=UTC))
	print(Date_Gfs)
	Lat_Gfs=f.variables['lat_3'].data
	Lon_Gfs=f.variables['lon_3'].data
	TMP_Gfs=f.variables['TMP_3_HTGL'].data# Temperature a 2m 
	HGT_Gfs=f.variables['HGT_3_ISBL'].data# Height above the fround each pressure level
	TMP_Gfs_P=f.variables['TMP_3_ISBL'].data# Height each temperature level
	HGT_Gfs_SUP=f.variables['HGT_3_SFC'].data #Elevation topography
	Lat_GFS=f.variables['lat_3'].data#Vector latitude
	Lon_GFS=f.variables['lon_3'].data
	for sta in PosSta:
		IdxLatGfs=next(idx for idx,val in enumerate(Lat_Gfs+0.5) if val < float(PosSta[sta]['Lat']))-1
		IdxLonGfs=next(idx for idx,val in enumerate(Lon_Gfs+0.5) if val > 360+float(PosSta[sta]['Lon']))
		y_interp=scipy.interpolate.interp1d([i for i in reversed(HGT_Gfs[:,IdxLatGfs,IdxLonGfs])],[i for i in reversed(TMP_Gfs_P[:,IdxLatGfs,IdxLonGfs])],bounds_error=False,fill_value=TMP_Gfs_P[-1,IdxLatGfs,IdxLonGfs])	
		if idxf==0:
			GFS_DATA=GFS_DATA.join(pd.DataFrame([y_interp(float(PosSta[sta]['Alt']))],index=[Date_Gfs],columns=[sta]))	
		else:
			GFS_DATA[sta][Date_Gfs]=y_interp(float(PosSta[sta]['Alt']))
	IdxLatGfs=next(idx for idx,val in enumerate(Lat_Gfs+0.5) if val < float(-29.72))-1
	IdxLonGfs=next(idx for idx,val in enumerate(Lon_Gfs+0.5) if val > 360+float(-53.70))
	GFS_T['TEMP']=pd.Series(TMP_Gfs_P[:,IdxLatGfs,IdxLonGfs],index=[Date_Gfs]*len(TMP_Gfs_P[:,IdxLatGfs,IdxLonGfs]))
	GFS_T['Level']=pd.Series(range(0,len(TMP_Gfs_P[:,IdxLatGfs,IdxLonGfs])),index=[Date_Gfs]*len(TMP_Gfs_P[:,IdxLatGfs,IdxLonGfs]))
	GFS_T['HGHT']=pd.Series(HGT_Gfs[:,IdxLatGfs,IdxLonGfs],index=[Date_Gfs]*len(TMP_Gfs_P[:,IdxLatGfs,IdxLonGfs]))
	GFS_Snd=GFS_Snd.append(GFS_T)



#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
########################## Contour plot
#Do a contour plot every 6 hours for a week
start='20140214 12'
end='20140214 12'
DPI=96
Diff_gfs_obs=DATA[start:end]#+273.15 - GFS_DATA[start:end]

#!!!!!!!!!!!!!!!!!!!!!!!!!! NEED TO RUN NETCDF_V2.py to make this graph

for idate,date in enumerate(Diff_gfs_obs.index):
	wFig=screen_width/DPI #size in inches 
	hFig=screen_height/DPI#
	fig=plt.figure(figsize=(wFig,hFig))
	filename=date.strftime('%Y-%m-%d %H:%M:%S')
	title=('BIAS between Obs - GFS'+'   '+filename)

	plt.title(title)
	print(title)
	# contour land
	CT1=plt.contourf(X,Y,Hgt,levels=range(1,2200,50),cmap=get_cmap('gray'))
	# Set the ticks label
	CT1.ax.set_xticks( x_stag[1::Nticks])
	CT1.ax.set_xticklabels(Ticks_Lon) 
	CT1.ax.set_yticks( y_stag[1::Nticks])
	CT1.ax.set_yticklabels(Ticks_Lat)
	#Grid
	CT1.ax.grid(True, zorder=0)
	CT1.ax.grid(True, zorder=0)
	scatter(np.array(LonStaI)*Dx,np.array(LatStaI)*Dy,marker='o',c='r',s=20)
	#===== Plot station Position
	for i,txt in enumerate(StaName):
		annotate(txt,(np.array(LonStaI[i]+5)*Dx,np.array(LatStaI[i]-5)*Dy),fontsize=14)
	# Trouver la position dans le contour plot en saidant du code netcdf
	LatSta=[round(x,2)for x in LatSta]
	stalat=[round(float(PosSta[i]['Lat']),2) for i in PosSta]
	Pos=[LatSta.index(p) for p in stalat]
	LATPOSSTAI=[LatStaI[r] for r in Pos]
	LONPOSSTAI=[LonStaI[r] for r in Pos]
	Min = Diff_gfs_obs.min().mean()
	Max= Diff_gfs_obs.max().mean()
	for o,txt in enumerate(PosSta):
		col=(round(Diff_gfs_obs[txt][date],2)+abs(Min))/(abs(Max)+abs(Min))
		print(str(round(Diff_gfs_obs[txt][date],2))+'---->'+str(col))
		annotate(round(Diff_gfs_obs[txt][date],2),(np.array(LONPOSSTAI[o]-10)*Dx,np.array(LATPOSSTAI[o]+10)*Dy),fontsize=20, color=plt.cm.RdYlBu(col))
	# Axis limits
	plt.xlim(x_stag[1:].min(),x_stag[1:].max())
	plt.ylim(y_stag[1:].min(),y_stag[1:].max())
	OutDirPath='/home/thomas/PhD/arps/res/fig_14-02-14/'
	filename=date.strftime('%Y-%m-%d %H:%M:%S')
	# Save grafics
	plt.savefig(OutDirPath+filename+'.png',dpi=DPI)
	print('Saving:'+OutDirPath+filename+'.png \n -----------------------\n')




#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
################################PLOT + Analyis #################################################

#===== Hourly mean over a week
DATA=DATA.convert_objects(convert_numeric=True)#Convert the data frame in numeric
DATA_mean_Day = DATA.groupby(lambda x: (x.year, x.hour)).mean().mean(axis=1)+273.15
DATA_GFS_mean_Day = GFS_DATA.groupby(lambda x: (x.year, x.hour)).mean().mean(axis=1)

hour=[x[1] for x in  DATA_mean_Day.index]
p1=plt.plot(hour,DATA_mean_Day,'-ro',label='"Mean 48 Climatic stations in domain"')
p2=plt.plot(hour,DATA_GFS_mean_Day,'-bo',label='"Mean Gfs at the position of the station"')
plt.ylabel('Temperature in (K)')
plt.xlabel('Time (h)')
plt.legend(loc=4)
plt.grid(True)
plt.show()




####################### DIFFERENCE BETWEEN GFS AND OBS HOURLY TIME SERIE
DIFF_GFS_OBS=DATA[start:end].groupby(lambda x: (x.year, x.hour)).mean()+273.15 - GFS_DATA[start:end].groupby(lambda x: (x.year, x.hour)).mean()

DIFF_GFS_OBS.T.boxplot()
plt.xticks(rotation=90)# Rotate x axis 
##############################


#OOOOOOOOOOOOOOOOOOOOOOOOOO Box plot 
DATA=DATA.convert_objects(convert_numeric=True)
GFS_DATA=GFS_DATA.convert_objects(convert_numeric=True)



plt.plot(y_new,x_new)
#====== BOxplot difference between GFS and observations + color redes + sorted by altitude

StaAlt=[float(PosSta[i]['Alt']) for i in PosSta]
StaName=[ i for i in PosSta]
list1, list2 = (list(t) for t in zip(*sorted(zip(StaAlt, StaName))))

DATA_By_Alt=pd.DataFrame(index=Date)
DIFF_OBS_GFS = (DATA[start:end]+273.15) - GFS_DATA[start:end]
colorplot=[]
colorNet={'data_sinda':'pink', 'data_INMET':'lightblue', 'data_IAC':'lightgreen'}

for i in list2:
	DATA_By_Alt[i]=DIFF_OBS_GFS[i]
	colorplot.append(colorNet[PosSta[i]['Net']])


#=====================================
#===== CREATE Station
StaAlt=[float(PosSta[i]['Alt']) for i in PosSta]
StaName=[ i for i in PosSta]
list1, list2 = (list(t) for t in zip(*sorted(zip(StaAlt, StaName))))

DATA.loc['20140214 12']
plt.plot(map(float,DATA.loc['20140214 12'][list2]),list1)

#altitude
ALTT=[20.0, 539.0, 555.0, 571.0, 574.0, 595.0, 633.0, 662.0, 667.0, 702.0, 705.0, 725.0, 761.0, 763.0, 770.0, 771.0, 771.0, 776.0, 782.0, 789.0, 801.0, 812.0, 828.0, 874.0, 881.0, 897.0, 899.0, 900.0, 902.0, 933.0, 1002.0, 1050.0, 1105.0, 1144.0, 1150.0, 1276.0, 1434.0, 1461.0, 1500.0, 1590.0, 1642.0]

#temperature
TT=[31.44, 30.0, 26.67, 26.9, 29.26, 28.08, 24.4, 28.82, 27.79, 27.16, 30.5, 27.15, 28.62, 28.5, 29.4, 27.86, 27.86, 27.84, 28.78, 27.32, 27.2, 26.91, 26.58, 29.13, 27.88, 27.28, 29.5, 26.82, 27.88, 28.21, 28.02, 27.56, 26.25, 25.5, 24.4, 24.8, 20.0, 18.5, 20.2, 23.5, 24.4]




z = np.polyfit(ALTT,TT, 3)
f = np.poly1d(z)
x_new = np.linspace(100, 3000, 50)
y_new = f(x_new)
plt.plot(y_new,x_new)
plt.plot(TT,ALTT)
plt.show()



#++++++++++++++++++++++++++++++++++++++++++









box=DATA_By_Alt.boxplot(patch_artist=True)
plt.xticks(rotation=90)# Rotate x axis 
for patch, color in zip(box['boxes'], colorplot):
    patch.set_facecolor(color)

plt.show()



########### PLOT TIME SERIE TEMPERATURE 
# pour voir les eventuelle probleme

plt.figure()
statoplot=['STRdoSapucai-MGfev14','flonaLorena-SPfev14','Guaratingueta-SPfev14','Itu-SPFev-14','Taubate-SPfev14','CamposdoJordao-Met-SPfev14']

for i in statoplot:
	DATA[i].plot()

plt.legend()
plt.show()



# LAG PHASE
GFS_DATA['Taubate-SPfev14'].plot()
(DATA['Taubate-SPfev14']+273.15).plot()
plt.legend()
plt.show()

GFS_DATA['IAC_Weather_23_Extrema.datdata'].plot()
(DATA['IAC_Weather_23_Extrema.datdata']+273.15).plot()
plt.show()


GFS_DATA['IAC_Weather_123_Cassia_dos_Coqueiros.datdata'].plot()
(DATA['IAC_Weather_123_Cassia_dos_Coqueiros.datdata']+273.15).plot()
plt.show()


GFS_DATA['INB-PC01-MGfev14'].plot()
(DATA['INB-PC01-MGfev14']+273.15).plot()
plt.show()


GFS_DATA['flonaLorena-SPfev14'].plot()
(DATA['flonaLorena-SPfev14']+273.15).plot()
plt.show()


GFS_DATA['STRdoSapucai-MGfev14'].plot()
(DATA['STRdoSapucai-MGfev14']+273.15).plot()
plt.show()

GFS_DATA['Guaratingueta-SPfev14'].plot()
(DATA['Guaratingueta-SPfev14']+273.15).plot()
plt.show()



GFS_DATA['IAC_Weather_22_Espirito Santo do Pinhal.datdata'].plot()
(DATA['IAC_Weather_22_Espirito Santo do Pinhal.datdata']+273.15).plot()
plt.show()

GFS_DATA['IAC_Weather_3_Campinas.datdata'].plot()
(DATA['IAC_Weather_3_Campinas.datdata']+273.15).plot()
plt.show()
############################################################  ############################## ############################## 
############################## Soundings
IP_Snd="/home/thomas/PhD/obs-lcb/soundings/140214/"
fn_Snd="FEB_MARTE"
year='2014'
month='02'


data_Snd = pd.read_csv(IP_Snd+fn_Snd, index_col=False, header=0,delim_whitespace=True)

di=np.where(data_Snd['HGHT'][1:] < data_Snd['HGHT'][:-1]) # NUMBER OF SOUNDING IN THE MONTH in FILE !!!
di=di[0]+1
di=np.insert(di,0,0)
di=np.append(di,data_Snd.index[-1]+1)
di=di[1:]-di[:-1]

Date_SND=pd.to_datetime([])
Date_SND_final=pd.to_datetime([])
Date_Snd_REAL= pd.date_range('2014-02-01-00','2014-02-28-00',freq='12H')# REAL TIME SERIE EVERY 12Z
CORRDATE=pd.to_datetime(['2014-02-10-00','2014-02-12-12','2014-02-15-00','2014-02-17-12','2014-02-21-12'])

Match=sorted(list(set(Date_Snd_REAL) - set(CORRDATE)))

level=[]
Date_Snd=pd.to_datetime(Match)
for i,v in enumerate(di):
	Date_SND_final=Date_SND_final.append(pd.to_datetime([Date_Snd[i].strftime('%Y-%m-%d %H:%M:%S')]*v))
	level.extend(range(1,v+1))### SO POWERFULL


#Date_SND=[pd.to_datetime(datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S')) for i in Date_SND]
data_Snd['Date']=Date_SND_final
data_Snd=data_Snd.set_index('Date')
data_Snd['Level']=level







data_Snd_mean=data_Snd.groupby('Level',).mean()


data_Snd['hour']=data_Snd.index.hour

data_Snd.groupby([data_Snd['hour'],data_Snd['Level']]).mean()

GFS_Snd_09pm=GFS_Snd[GFS_Snd.index.hour==21]
GFS_Snd_09am=GFS_Snd[GFS_Snd.index.hour==9]


data_Snd_09pm=data_Snd[data_Snd['hour']==0]
data_Snd_09am=data_Snd[data_Snd['hour']==12]

data_Snd_09pm_mean=data_Snd_09pm.groupby('Level',).mean()
data_Snd_09am_mean=data_Snd_09am.groupby('Level',).mean()

GFS_Snd_09pm_mean=GFS_Snd_09pm.groupby('Level',).mean()
GFS_Snd_09am_mean=GFS_Snd_09am.groupby('Level',).mean()

#pot all soundings
start=0
for i,v in enumerate(di):
	end=start+di[i]
	fig = plt.figure()
	plt.plot(data_Snd['TEMP'][start:end],data_Snd['HGHT'][start:end],'-ro',label='Mean Temperature (C)')
	fig.suptitle(str(data_Snd.index[start]), fontsize=20)
	#plt.xlabel('Temperature', fontsize=18)
	plt.ylabel('Height (m)', fontsize=16)
	start=end
	plt.show()

#plot mean at 12 and 00
p1=plt.plot(data_Snd_09pm_mean['TEMP']+273.15,data_Snd_09pm_mean['HGHT'],'-bo',label='Mean Temperature at 00h(C)')
plt.plot(data_Snd_09am_mean['TEMP']+273.15,data_Snd_09am_mean['HGHT'],'-b+',label='Mean Temperature at 12h(C)')
plt.plot(GFS_Snd_09pm_mean['TEMP'],GFS_Snd_09pm_mean['HGHT'],'-go',label='Mean GFS Temperature at 00h(C)')
plt.plot(GFS_Snd_09am_mean['TEMP'],GFS_Snd_09am_mean['HGHT'],'-g+',label='Mean GFS Temperature at 12h(C)')
plt.axis([260, 300, 0, 5000])
plt.grid(True)
plt.legend(loc=2)
plt.show()
#PLot mean
p1=plt.plot(data_Snd_mean['TEMP'],data_Snd_mean['HGHT'],'-ro',label='Mean Temperature (C)')
plt.legend(loc=2)



########################## SOUNDING GFS

#hautedata_Snd.indexur superficie: 'HGT_3_SFC'
# Lat Lat_3
#Long Lon_3
#Temperature above ground level: TMP_3_HTGL


for x in f.variables:
	print('====================================')
	print(x)
	print(f.variables[x].long_name)
	print(f.variables[x].units)
	print(f.variables[x].shape)
	print('====================================')

#for x in f.variables:
#	print(x)

c=['TMP_3_GPML','TMP_3_DBLY','TMP_3_SIGL','TMP_3_ISBL','TMP_3_TRO','TMP_3_GPML','TMP_3_MCTL_ave','TMP_3_MWSL','TMP_3_LCTL_ave','TMP_3_HTGL','TMP_3_SFC','TMP_3_HCTL_ave','TMP_3_SPDY']

for x in c:
	print(x)
	print(f.variables[x].level_indicator)


HGT_3_HTFL HGT_3_TRO HGT_3_PVL

#############################################################################################
############################################################################################

#=====================	
#===== WRITE Obs in ADAS
#=====================


# Merge Data
data={'data_INMET':data_INMET,'data_sinda':data_sinda,'data_IAC':data_IAC}
#create a dictionnary for the specific name of the variables which depend of the network
var_INMET={'hour':'hora','date':'data','Altitude':'Altitude','Longitude':'Longitude','Latitude':'Latitude','T':'temp_inst','Td':'pto_orvalho_inst','Vvel':'vento_direcao','Vdir':'vento_vel','P':'pressao','I':'radiacao'}#Vvel adn Vdir are inversed to solve data problem
var_sinda={'hour':'DataHora','date':'DataHora','Altitude':'Altitude','Longitude':'Longitude','Latitude':'Latitude','T':'TempAr','Td':'UmidRel','Vvel':'VelVento10m','Vdir':'DirVento','P':'PressaoAtm','I':'RadSolAcum'}
var_IAC={'hour':'date','date':'date','Altitude':'Altitude','Longitude':'Longitude','Latitude':'Latitude','T':'Temp','Td':'Umidade'}

varname={'data_INMET':var_INMET,'data_sinda':var_sinda,'data_IAC':var_IAC}


#====== Function to convert the format
#As the format of the data are different between the network, the following function permit to transform this 
def same(var):
	var=[var]
	return(var)

def same2(var,*arg):
	return var

def Date(var):
	sp=var.split()[0]
	sp=datetime.datetime.strptime(sp,'%Y-%m-%d').strftime('%d/%m/%Y')
	return [sp]

def Hora(var):
	sp=var.split()[1]
	sp=sp[0:2]
	return [sp]

def INMETAlt(var):
	if ',' in var:
		var=float(var.replace(',','.'))*1000
	return var

# if no obs > -99.9
def NoObs(var,trans,trans2):
	try:
		eval(var)
	except KeyError:
		return -99.9
	else:
		if eval(var)=='' or eval(var)=='/////':
			return -99.9
		else:#===== Read INMET station


with open(IP_INMET+fn_INMET, 'r') as csvfile_INMET:
        reader_INMET=csv.reader(csvfile_INMET)
        header_INMET=reader_INMET.next()
        data_INMET = {}
        for h in header_INMET:
                data_INMET[h]=[]
        for row in reader:
                for h,v in zip(header_INMET,row):
                        data_INMET[h].append(v)

			return eval(eval(var)+trans+trans2)

#convert T and RH in TD for Sinda
def Td(Rh,T):
	EsT=6.112*np.exp((17.67*float(T))/(float(T)+243.5))#Vapor at saturation in mb
	EsTd=(float(Rh)*EsT)/100
	Td=(np.log(EsTd/6.112)*243.5)/(17.67-np.log(EsTd/6.112))
	Td=float(Td)
	return Td

#----- Dictionnary with conversion
conv_sinda={'hour':Hora,'date':Date,'elev':same2,'Td':Td}
conv_INMET={'hour':same,'date':same,'elev':INMETAlt,'Td':same2}
conv_IAC={'hour':Hora,'date':Date,'elev':same2,'Td':Td}
conv={'data_INMET':conv_INMET,'data_sinda':conv_sinda,'data_IAC':conv_IAC}


