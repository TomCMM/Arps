from netcdf_lib import *

#if __name__ == "__main__":
#===============================================================================
# Horizontal plot (variable, topography and wind vector)
#===============================================================================
InPath="/dados2/sim/out100m_V11_netcdf/out100m_V11_netcdf/"
Files=glob.glob(InPath+"*")
Files.sort()
Files=Files[0:2]# !!!!! control only one file

cphigh = ArpsFigures2.getparamset()

cplow = cphigh

for Path in Files:
	print(Path)
	ARPS = arps()
	BASE = BaseVars(Path)
	SPEV = SpecVar()
	ARPS.load(BASE)
	ARPS.load(SPEV)
	print(ARPS.getatt('THISDMP'))
	FIG=ArpsFigures(ARPS)
	fig=plt.figure(figsize=(FIG.getpara('wfig'),FIG.getpara('hfig')))
	plt.suptitle(FIG.getpara('subtitle'),fontsize=20)
	FIG.setpara('Latmin',-22.90)
	FIG.setpara('Latmax',-22.84, )
	FIG.setpara('Lonmin',-46.28)
	FIG.setpara('Lonmax',-46.22)
	FIG.setpara('Altcross',-400)
	FIG.setpara('nlevel',10)
	FIG.setpara('varmin',1)
	FIG.setpara('varmax',10)
	FIG.setpara('DPI',80)
	FIG.contourf('VEGTYP')
	plt.colorbar()
	FIG.setpara('varmin',800)
	FIG.setpara('varmax',1400)
	FIG.setpara('nlevel',20)
	CS=FIG.contour('ZP')
	CS.ax.grid(True, zorder=0)
	plt.clabel(CS, inline=10, fontsize=15,fmt='%4.f',)
# 	FIG.setpara('Nbarb',2)
# 	FIG.setpara('Lbarb',6)
# 	FIG.windvector()
	plt.savefig('control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'))
	plt.close()

#===============================================================================
#  Vertical plot
#===============================================================================
from netcdf_lib import *

InPath="/dados2/sim/out100m_V11_netcdf/out100m_V11_netcdf/"
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
	FIG.setpara('Latmax',-22.84)
	FIG.setpara('Lonmin',-46.27)
	FIG.setpara('Lonmax',-46.23)
	FIG.setpara('ATCDC_entireatmosphere_consideredasasinglelayerltmin',0)
	FIG.setpara('Altmax',8000, )
	FIG.setpara('nlevel',200)
	FIG.setpara('Latcross',-22.88)
	FIG.setpara('varmin',0)
	FIG.setpara('varmax',1)
	FIG.setpara('DPI',80)
	FIG.contourf('TKE')
	cbar=plt.colorbar()
	cbar.set_ticks(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
	cbar.set_ticklabels(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
	FIG.setpara('Nbarb',1)
	FIG.setpara('Lbarb',6)
	FIG.windvector()
	plt.axis([FIG.getpara('Lonmin'),FIG.getpara('Lonmax'),1000,2000])
	plt.savefig('control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'), transparent=False)
	plt.close()



#===============================================================================
# Get variable at a point
#===============================================================================
from netcdf_lib import *
import pandas as pd
import sns


InPath="/dados2/gfs/"

Files=glob.glob(InPath+"*nc")
Files.sort()

model='GFS_for'


Serie = netcdf_serie(Files,model)

U_gfs=Serie.get('UGRD_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]])# permit to avoid "too many file problem"
V_gfs=Serie.get('VGRD_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]])
#T_gfs=Serie.get('Tk',select=[[100000],[-22.86],[360-46.28,360-46.29]])['Tk']
CC_gfs=Serie.get('TCDC_entireatmosphere_consideredasasinglelayer_',select=[[0],[-22.86],[360-46.28,360-46.29]])
Serie.dataframe.index
CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'].columns=['TCC']

#------------------------------------------------------------------------------ 
# WIND histograme 
wind=np.sqrt(Serie.dataframe['UGRD_1000mb']**2+Serie.dataframe['VGRD_1000mb']**2)
TCC=CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_']
#------------------------------------------------------------------------------ 
# DISTRIBUTION WEATHER CONDITIONS
# g = sns.jointplot(wind,CC_gfs['TCC'], kind="kde", size=7, space=0)
#sns.jointplot(wind[wind.index.hour==15],CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'][wind.index.hour==15], color="#4CB391")



#===============================================================================
# Irradiance
#===============================================================================

InPath='/home/thomas/PhD/obs-lcb/LCBData/obs/Irradiance/RE07115.txt'
Irr=pd.read_csv(InPath,sep=',')
Irr.columns=['ID','Year','Day','Hour','Pira_397','Pira_369','Tlogger','LoggerV']

# creating index
newindex = [ ]
for i in Irr.index:
	hour=str(Irr['Hour'][i]).zfill(4)[0:2]
	if hour == '24':
		hour ='00'
	minute=str(Irr['Hour'][i]).zfill(4)[2:4]
	date=datetime.datetime(int(Irr['Year'][i]),1,1,int(hour) ,int(minute)) + datetime.timedelta(int(Irr['Day'][i])-1)
	newindex.append( date )

Irr['newindex']=newindex
Irr=Irr.set_index('newindex')

#------------------------------------------------------------------------------ 
# Rsun irradiance
InPath='/home/thomas/PhD/rsun/res/Sim_C05March2015/Irrdiance_20-02-2015.csv'
IRsun=pd.read_csv(InPath,sep=',',index_col=0)
IRsun.index=pd.to_datetime(IRsun.index)

#------------------------------------------------------------------------------ 

Irr_mean=Irr['Pira_397'].resample("1H",how='mean')
DT_SV_mean=DT_SV.resample("1H",how='mean')
ClearSkyIrr=IRsun['C05'][Irr_mean.index].groupby(lambda t: (t.hour)).mean() # clear sky irradiance


DI=pd.Series(index=Irr_mean.index)
for i in Irr_mean.index:
	DI[i]=(Irr_mean[i]/ClearSkyIrr[i.hour])*100


# DI=DI.between_time('07:00','09:00')
# DT_SV_mean=DT_SV_mean.between_time('06:00','08:00')

df=pd.concat([DT_SV_mean,DI],axis=1,join_axes=[Irr.index])
df.columns=['DT','Irr']

sns.set(style="darkgrid")
color = sns.color_palette()[2]
g = sns.jointplot("DT", "Irr", data=df, kind="reg", color=color, size=7)
plt.show()



#===============================================================================
# Heat map Irradiance
#===============================================================================

Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)

windsta9=station.getvar('Sm m/s').resample("1H",how='mean')

ClearSkyIrr=IRsun['C05'][Irr_mean.index].groupby(lambda t: (t.hour)).mean() # clear sky irradiance
# ClearSkyIrr=Irr['Pira_397'].groupby(pd.TimeGrouper(freq='10Min')).max() # clear sky irradiance
# ClearSkyIrr=ClearSkyIrr.groupby(lambda t: (t.hour,t.minute)).max()
Irr_mean=Irr['Pira_397'].resample("1H",how='mean')
DT_SV_mean=DT_SV.resample("1H",how='mean')

DI=pd.Series(index=Irr_mean.index)
for i in Irr_mean.index:
	DI[i]=(Irr_mean[i]/ClearSkyIrr[(i.hour)])*100


windsta9=windsta9.between_time('14:00','16:00')
DI=DI.between_time('14:00','16:00')
DT_SV_mean=DT_SV_mean.between_time('14:00','16:00')



df=pd.concat([(windsta9/10).round(1)*10,(DI/20).round()*20, DT_SV_mean],axis=1,join_axes=[DI.index])


df=df.drop_duplicates()
df.columns=['wind','DI','DT']
df_rect=pd.pivot_table(df,index=["DI"],values=['DT'],columns=['wind'],aggfunc=np.mean)

ax=sns.heatmap(df_rect)


# count 
count=pd.pivot_table(df,index=["DI"],values=['DT'],columns=['wind'],aggfunc=np.shape)


def HeatAnnotate(pivottable,ax):
	"""
	the columns and the index value dosent correspond to the xticks and yticks plotted
	Theirfor I get the true value of the axis to make the correct annotation of the plot
	"""
	columns =np.array(count.columns.labels)[1]
	index = count.index.values
	xticks=ax.get_xticks()
	yticks=ax.get_yticks()[::-1]
	for i,iy in zip(count.index,yticks) :
		for j,jx in zip(columns,xticks):
			print(i,j)
			plt.annotate(str(count.ix[i][j]), xy=(jx,iy))

HeatAnnotate(count,ax)

plt.gca().invert_yaxis()
plt.show()

#===============================================================================
# Heat map ILW
#===============================================================================

#------------------------------------------------------------------------------ 
# # calculate Longwave downard radiation
# Files=['/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C08clear_merge.TXT']
# station = LCB_station(Files[0])

def ILw(em , T):
	"""
	calculate the downward radiation in W m-2
	Brutsaert WH (1975) On a derivable formula for long-wave radiation from clear skies. Water Resour Res 11(5):742–744
	Clear skies conditions
	
	em: capor pressure hpa
	T: temperature degree
	
	"""
	stefan= 5.67051 * 10 **-8
	em = em * 10**2 # convert in PA
	T= T + 273.15# convert in Kelvin
	E=0.643*(em/T)**(1/7)
	L = E*stefan*T**4
	return L
# 
# ILw = ILw(station.getvar('Ev hpa'), station.getvar('Ta C'))
# 

Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)

# #------------------------------------------------------------------------------ 
# # 10min
# #------------------------------------------------------------------------------ 
windsta9=station.getvar('Sm m/s').resample("30min",how='median')
#net_mean=Ribeiraonet.Data.resample('30min',how='median')
#ILw_mean=ILw(net_mean['Ev hpa'],net_mean['Ta C'])
ILw_mean=ILw(station.getvar('Ev hpa'),station.getvar('Ta C')).resample("30min",how='median')
DT_SV_mean=DT_SV.resample("30min",how='median')

# # 
windsta9=windsta9["2014-09-10 00:00:00":"2015-04-10 00:00:00"]
ILw_mean=ILw_mean["2014-09-10 00:00:00":"2015-04-10 00:00:00"]
DT_SV_mean=DT_SV_mean["2014-09-10 00:00:00":"2015-04-10 00:00:00"]



#------------------------------------------------------------------------------  
# Desvio padrao %
#------------------------------------------------------------------------------ 

Lw_ClearSky=ILw_mean.groupby(pd.TimeGrouper(freq='30min')).median() # clear sky irradiance
Lw_ClearSky=Lw_ClearSky.groupby(lambda t: (t.hour,t.minute)).median()


DI=pd.Series(index=ILw_mean.index)
for i in ILw_mean.index:
	DI[i]=((ILw_mean[i] - Lw_ClearSky[(i.hour,i.minute)]) / Lw_ClearSky[(i.hour,i.minute)]) * 100


# #------------------------------------------------------------------------------ 
# # 1H
# #------------------------------------------------------------------------------ 
# Lw_ClearSky=ILw_mean.groupby(pd.TimeGrouper(freq='3H')).mean() # clear sky irradiance
# Lw_ClearSky=Lw_ClearSky.groupby(lambda t: (t.hour)).mean()
# 
# 
# DI=pd.Series(index=ILw_mean.index)
# for i in ILw_mean.index:
# 	DI[i]=((ILw_mean[i] - Lw_ClearSky[(i.hour)]) / Lw_ClearSky[(i.hour)]) * 100
# ILw_mean=ILw(station.getvar('Ev hpa'),station.getvar('Ta C')).resample("10min",how='median')
#------------------------------------------------------------------------------ 


windsta9=windsta9.between_time('04:00','06:00')
DI=DI.between_time('04:00','06:00')
DT_SV_mean=DT_SV_mean.between_time('04:00','06:00')
# 


df=pd.concat([(windsta9/10).round(1)*10,(DI/2).round()*2, DT_SV_mean],axis=1,join_axes=[DI.index])


df=df.drop_duplicates()
df.columns=['wind','DI','DT']
df_rect=pd.pivot_table(df,index=["DI"],values=['DT'],columns=['wind'],aggfunc=np.median)

ax=sns.heatmap(df_rect, fmt="d")
plt.clim(-4,4)

# count 
count=pd.pivot_table(df,index=["DI"],values=['DT'],columns=['wind'],aggfunc=np.shape)


def HeatAnnotate(pivottable,ax):
	"""
	the columns and the index value dosent correspond to the xticks and yticks plotted
	Theirfor I get the true value of the axis to make the correct annotation of the plot
	"""
	columns =np.array(count.columns.labels)[1]
	index = count.index.values
	xticks=ax.get_xticks()
	yticks=ax.get_yticks()[::-1]
	for i,iy in zip(count.index,yticks) :
		for j,jx in zip(columns,xticks):
			print(i,j)
			plt.annotate(str(count.ix[i][j]), xy=(jx,iy))

HeatAnnotate(count,ax)

plt.gca().invert_yaxis()
plt.show()

#===============================================================================
# plot DT vs time for different wind and ratio irradiance condition
#===============================================================================


InPath='/home/thomas/PhD/obs-lcb/LCBData/obs/Irradiance/RE07115.txt'
Irr=pd.read_csv(InPath,sep=',')
Irr.columns=['ID','Year','Day','Hour','Pira_397','Pira_369','Tlogger','LoggerV']

# creating index
newindex = [ ]
for i in Irr.index:
	hour=str(Irr['Hour'][i]).zfill(4)[0:2]
	if hour == '24':
		hour ='00'
	minute=str(Irr['Hour'][i]).zfill(4)[2:4]
	date=datetime.datetime(int(Irr['Year'][i]),1,1,int(hour) ,int(minute)) + datetime.timedelta(int(Irr['Day'][i])-1)
	newindex.append( date )

Irr['newindex']=newindex
Irr=Irr.set_index('newindex')



Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)

#------------------------------------------------------------------------------ 
# 10min
#------------------------------------------------------------------------------ 
windsta9=station.getvar('Sm m/s').resample("10min",how='mean')
IRsun.columns=['C05']
ClearSkyIrr_obs=Irr['Pira_397'].groupby(pd.TimeGrouper(freq='10Min')).max() # clear sky irradiance
ClearSkyIrr_obs=ClearSkyIrr_obs.groupby(lambda t: (t.hour,t.minute)).max()
ClearSkyIrr=IRsun['C05'][Irr_mean.index].groupby(lambda t: (t.hour,t.minute)).mean() # clear sky irradiance
Irr_mean=Irr['Pira_397'].resample("10min",how='mean')
DT_SV_mean=DT_SV.resample("10min",how='mean')

# rng = pd.date_range('1/1/2011', periods=144, freq='10min')
# Irr_mean=Irr_mean.groupby(lambda t: (t.hour,t.minute)).mean()
#  
# plt.plot(rng,ClearSkyIrr,label='Rsun')
# plt.plot(rng,Irr_mean,label='mean_obs')
#  
#  
# plt.legend()
# plt.show()

#for day in Irr_mean.index.day:




DI=pd.Series(index=Irr_mean.index)
for i in Irr_mean.index:
	DI[i]=(Irr_mean[i]/ClearSkyIrr[(i.hour,i.minute)])*100



windlabels=['0_5']
DIlabels=['0_30','30_70','70_100']
windcut=pd.Series(pd.cut(windsta9,bins=[0,5],labels=windlabels),index=windsta9.index)
DIcut=pd.Series(pd.cut(DI,bins=[0,30,70,100],labels=DIlabels),index=DI.index)


df=pd.concat([windcut,DIcut, DT_SV_mean],axis=1,join_axes=[DIcut.index])
df.columns=['wind','DI','DT']
df['wind'].value_counts()

#------------------------------------------------------------------------------ 
fig = plt.figure()
linestyles = ['-', '--', ':']
colors=list()
for i in np.arange(1,0,-0.3):
	print(plt.cm.jet(i))
	print(colors)
	colors.append(plt.cm.Greys(i))


for i,windbin in enumerate(windlabels):
	for j,DIbin in enumerate(DIlabels):
		col=colors[i]
		line=linestyles[j]
		select=df['DT'][(df['wind'] == windbin) & (df['DI'] == DIbin)]
		select=select.groupby(lambda t: (t.hour)).mean()
		print select
		plt.plot(select.index,select,label=str('U '+windbin+'  DI '+DIbin),linestyle=line,color=col)


plt.axhline(y=0,color='k') # horizontal line at 0

plt.annotate(str('Valley Colder'), xy=(12,-0.2),color='blue')
plt.annotate(str('Valley warmer'), xy=(12,0.2),color='red')

plt.legend()
fig.suptitle('Temperature difference between slope and valley stations for different condition of wind at the ridge and ratio of maximum radiation',fontsize=16)
plt.xlabel('Time (h)',fontsize=16)
plt.ylabel('Temperature difference between Slope and Valley stations(C)',fontsize=16)
plt.show()

#===============================================================================
# Calculation doward longwave radiation
#===============================================================================
from __future__ import division
import os
import glob
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fnmatch
import copy
from LCBnet_lib import *
from scipy import interpolate
from clear import clear
import seaborn as sns


#------------------------------------------------------------------------------ 
# # calculate Longwave downard radiation
# Files=['/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C08clear_merge.TXT']
# station = LCB_station(Files[0])

def ILw(em , T):
	"""
	calculate the downward radiation in W m-2
	Brutsaert WH (1975) On a derivable formula for long-wave radiation from clear skies. Water Resour Res 11(5):742–744
	Clear skies conditions
	
	em: capor pressure hpa
	T: temperature degree
	
	"""
	stefan= 5.67051 * 10 **-8
	em = em * 10**2 # convert in PA
	T= T + 273.15# convert in Kelvin
	E=0.643*(em/T)**(1/7)
	L = E*stefan*T**4
	return L
# 
# ILw = ILw(station.getvar('Ev hpa'), station.getvar('Ta C'))
# 

Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)

# #------------------------------------------------------------------------------ 
# # 10min
# #------------------------------------------------------------------------------ 
#windsta9=station.getvar('Sm m/s').resample("30min",how='mean')
net_mean=Ribeiraonet.Data.resample('30min',how='mean')
ILw_mean=ILw(net_mean['Ev hpa'],net_mean['Ta C'])
#ILw_mean=ILw(station.getvar('Ev hpa'),station.getvar('Ta C')).resample("30min",how='mean')
DT_SV_mean=DT_SV.resample("30min",how='mean')

#------------------------------------------------------------------------------  
# Desvio padrao %
#------------------------------------------------------------------------------ 

Lw_ClearSky=ILw_mean.groupby(pd.TimeGrouper(freq='30Min')).mean() # clear sky irradiance
Lw_ClearSky=Lw_ClearSky.groupby(lambda t: (t.hour,t.minute)).mean()


DI=pd.Series(index=ILw_mean.index)
for i in ILw_mean.index:
	DI[i]=((ILw_mean[i] - Lw_ClearSky[(i.hour,i.minute)]) / Lw_ClearSky[(i.hour,i.minute)]) * 100

ILw_mean=DI
# #------------------------------------------------------------------------------ 
# # 1H
# #------------------------------------------------------------------------------ 
# windsta9=station.getvar('Sm m/s').resample("1H",how='mean')
# #net_mean=Ribeiraonet.Data.resample('10min',how='mean')
# #ILw_mean=ILw(net_mean['Ev hpa'],net_mean['Ta C'])
# ILw_mean=ILw(station.getvar('Ev hpa'),station.getvar('Ta C')).resample("1H",how='mean')
# DT_SV_mean=DT_SV.resample("1H",how='mean')
# 
# #------------------------------------------------------------------------------ 
# # Desvio padrao % 1H
# #------------------------------------------------------------------------------ 
# 
# Lw_ClearSky=ILw_mean.groupby(pd.TimeGrouper(freq='1H')).mean() # clear sky irradiance
# Lw_ClearSky=Lw_ClearSky.groupby(lambda t: (t.hour)).mean()
# 
# 
# DI=pd.Series(index=ILw_mean.index)
# for i in ILw_mean.index:
# 	DI[i]=((ILw_mean[i] - Lw_ClearSky[(i.hour)]) / Lw_ClearSky[(i.hour)]) * 100
# 




#------------------------------------------------------------------------------ 
#	Histogram Ivs U
#------------------------------------------------------------------------------ 

df=pd.concat([windsta9,ILw_mean, DT_SV_mean],axis=1,join_axes=[DT_SV_mean.index])
df.columns=['wind','ILw','DT']

sns.set(style="darkgrid")
color = sns.color_palette()[2]

g = sns.jointplot("ILw", "wind", data=df)
plt.show()



windlabels=['0_5']
DIlabels=['-10_-2.5','-2.5_2.5','2.5_10']
windcut=pd.Series(pd.cut(windsta9,bins=[0,5],labels=windlabels),index=windsta9.index)
DIcut=pd.Series(pd.cut(ILw_mean,bins=[-10,-2.5,2.5,10],labels=DIlabels),index=ILw_mean.index)

# exclusion classes
# windcut=windcut[ windcut != '4_6' ]
# #DIcut=DIcut[ DIcut != '-2.5_2.5']
# windlabels.remove( '4_6')
# DIlabels.remove('-2.5_2.5')

df=pd.concat([windcut,DIcut, DT_SV_mean],axis=1,join_axes=[DT_SV_mean.index])
df.columns=['wind','ILw','DT']
df['wind'].value_counts()

#------------------------------------------------------------------------------ 
fig = plt.figure()
linestyles = ['-', '--', ':']
colors=list()
for i in np.arange(1,0,-0.3):
	print(plt.cm.jet(i))
	print(colors)
	colors.append(plt.cm.Greys(i))

for i,windbin in enumerate(windlabels):
#	col=colors[i]
	for j,DIbin in enumerate(DIlabels):
		col=colors[i]
		line=linestyles[j]
#		line=linestyles[j]
		select=df['DT'][(df['wind'] == windbin) & (df['ILw'] == DIbin)]
		select=select.groupby(lambda t: (t.hour)).mean()
		print select
		ax=plt.plot(select.index,select,label=str('U '+windbin+'  ILw '+DIbin),linestyle=line,color=col)


plt.axhline(y=0,color='k') # horizontal line at 0

plt.annotate(str('Valley Colder'), xy=(12,-0.2),color='blue')
plt.annotate(str('Valley warmer'), xy=(12,0.2),color='red')

plt.legend()
fig.suptitle('Temperature difference between slope and valley stations for different condition of wind at the ridge and Incoming longwave radiation. Estimated by Brutsaert equation for clear sky',fontsize=16)
plt.xlabel('Time (h)',fontsize=16)
plt.ylabel('Temperature difference between Slope and Valley stations(C)',fontsize=16)
plt.show()





#===============================================================================
# scatter plot: DT vs wind sta9
#===============================================================================
import seaborn as sns

Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)

windsta9=station.getvar('Sm m/s').resample("1H",how='mean')
dirsta9=station.getvar('Dm G').resample("1H",how='mean')
#STD_windsta9=station.getvar('Sm m/s').resample("3H",how='std')


windsta9=windsta9[AccDailyRain < 0.1]#rainfilter
#windsta9=windsta9[STD_dirsta9 > 10]# select direction
#windsta9=windsta9[windsta9 < 10]# wind speed filter
#windsta9=windsta9[STD_windsta9 < 1.6]# wind speed filter

DT_SV_mean=DT_SV.resample("1H",how='mean')


# DT_SV_mean=DT_SV_mean[(dirsta9 < 180) & (dirsta9 > 135) ]
# windsta9=windsta9[(dirsta9 < 180) & (dirsta9 > 135) ]

windsta9=windsta9.between_time('03:00','19:00')
DT_SV_mean=DT_SV_mean.between_time('03:00','19:00')

windsta9=windsta9[DI[DI<30].index]
DT_SV_mean=DT_SV_mean[DI[DI<30].index]

df=pd.concat([DT_SV_mean,windsta9],axis=1,join_axes=[windsta9.index])
df.columns=['DT','windsta9']

sns.set(style="darkgrid")
color = sns.color_palette()[2]

g = sns.jointplot("DT", "windsta9", data=df, kind="reg", color=color, size=7)
plt.show()

#===============================================================================
# scatter plot: DT vs wind in the valley
#===============================================================================
import seaborn as sns

Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)

windsta9=station.getvar('Sm m/s').resample("1H",how='mean')
valleywind=Valleynet.Data['Sm m/s'].resample("1H",how='mean')
valleywind=valleywind.resample("1H",how='mean')
DT_SV_mean=DT_SV.resample("1H",how='mean')

valleywind=valleywind[windsta9[windsta9 < 4].index]
DT_SV_mean=DT_SV_mean[windsta9 < 4]

# 
# valleywind=valleywind.between_time('04:00','06:00')
# DT_SV_mean=DT_SV_mean.between_time('04:00','06:00')

df=pd.concat([DT_SV_mean,valleywind],axis=1,join_axes=[windsta9.index])
df.columns=['DT','valleywind']

sns.set(style="darkgrid")
color = sns.color_palette()[2]

g = sns.jointplot("DT", "valleywind", data=df, kind="reg", color=color, size=7)
plt.show()


#===============================================================================
# Channeling
#===============================================================================


from __future__ import division
import os
import glob
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fnmatch
import copy
from LCBnet_lib import *
from scipy import interpolate
from clear import clear
import seaborn as sns
#===============================================================================
InPath='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/'

# Find all the clima and Hydro
Files=glob.glob(InPath+"*")
net=LCB_net()


for i in Files:
	print(i)
	net.add(LCB_station(i))



#Files=reversed(Files)
position=[]
staname=[]
stationsnames=att_sta().stations(['Head'])
stations=att_sta().sortsta(stationsnames,'Lon')

position=stations['position']
staname=stations['staname']



Norm=np.array([])
Theta=np.array([])

Degree=range(0,380,20)
IniDeg=range(0,360,20)
EndDeg=range(20,380,20)
X,Y = np.meshgrid(position,Degree)

Ini='17:00'
End='19:00'

IniPeriod="2014-09-10 00:00:00"
EndPeriod="2015-04-10 00:00:00"

dirsta9= net.getsta('C09').getvar('Dm G').resample("10min",how='mean')
speedsta9= net.getsta('C09').getvar('Sm m/s').resample("10min",how='mean')
speedsta9=speedsta9.between_time(Ini,End)[IniPeriod:EndPeriod]
dirsta9=dirsta9.between_time(Ini,End)[IniPeriod:EndPeriod]

for inideg,enddeg in zip(IniDeg,EndDeg):
	for sta in staname:
		print(sta)
		print(str(inideg))
		print(str(enddeg))
		dir=net.getsta(sta).getvar('Dm G').resample("10min",how='mean')
		speed=net.getsta(sta).getvar('Sm m/s').resample("10min",how='mean')
		speed=speed.between_time(Ini,End)[IniPeriod:EndPeriod]
		dir=dir.between_time(Ini,End)[IniPeriod:EndPeriod]
		index=dirsta9[(dirsta9 > inideg) & (dirsta9 < enddeg)].index
		speed=speed[index].mean()
		dir=dir[index].mean()
		Norm=np.append(Norm,speed)
		Theta=np.append(Theta,dir)


V=np.cos(map(math.radians,Theta+180))*Norm
U=np.sin(map(math.radians,Theta+180))*Norm


U=U.reshape(len(IniDeg),len(staname))
V=V.reshape(len(IniDeg),len(staname))

# U=U.transpose()
# V=V.transpose()


a=plt.quiver(X,Y,U,V,scale=35)

l,r,b,t = plt.axis()
dx, dy = r-l, t-b
plt.axis([l-0.2*dx, r+0.2*dx, b-0.1*dy, t+0.1*dy])


plt.show()



plt.savefig('hovermoler.png')
plt.close()


#===============================================================================
# Channeling + cold pool strength
#===============================================================================


from __future__ import division
import os
import glob
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fnmatch
import copy
from LCBnet_lib import *
from scipy import interpolate
from clear import clear
import seaborn as sns
#===============================================================================
InPath='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/'

# Find all the clima and Hydro
Files=glob.glob(InPath+"*")
net=LCB_net()


for i in Files:
	print(i)
	net.add(LCB_station(i))



#Files=reversed(Files)
position=[]
staname=[]
stationsnames=att_sta().stations(['Head'])
stations=att_sta().sortsta(stationsnames,'Lon')

position=stations['position']
staname=stations['staname']



Norm=np.array([])
Theta=np.array([])

Degree=np.arange(-6,3,0.5)
IniDeg=np.arange(-6,2.5,0.5)
EndDeg=np.arange(-5.5,4,0.5)
X,Y = np.meshgrid(position,Degree)

Ini='00:00'
End='06:00'

IniPeriod="2014-10-10 00:00:00"
EndPeriod="2015-04-10 00:00:00"

DT_SV_mean=DT_SV.resample("10min",how='mean')
DT_SV_mean=DT_SV_mean.between_time(Ini,End)[IniPeriod:EndPeriod]


dirsta9= net.getsta('C09').getvar('Dm G').resample("10min",how='mean')
speedsta9= net.getsta('C09').getvar('Sm m/s').resample("10min",how='mean')

Tsta9= net.getsta('C09').getvar('Ta C').resample("10min",how='mean')
Tvalley=Valleynet.Data['Ta C'].resample("10min",how='mean').between_time(Ini,End)[IniPeriod:EndPeriod]
DT_SV_mean=Tvalley-Tsta9


speedsta9=speedsta9.between_time(Ini,End)[IniPeriod:EndPeriod]
dirsta9=dirsta9.between_time(Ini,End)[IniPeriod:EndPeriod]

for inideg,enddeg in zip(IniDeg,EndDeg):
	for sta in staname:
		print(sta)
		print(str(inideg))
		print(str(enddeg))
		dir=net.getsta(sta).getvar('Dm G').resample("10min",how='mean')
		speed=net.getsta(sta).getvar('Sm m/s').resample("10min",how='mean')
		speed=speed.between_time(Ini,End)[IniPeriod:EndPeriod]
		dir=dir.between_time(Ini,End)[IniPeriod:EndPeriod]
		index=DT_SV_mean[(DT_SV_mean > inideg) & (DT_SV_mean < enddeg) & (dirsta9 <60) & (dirsta9 >0) & (speedsta9 <5)].index
		speed=speed[index].mean()
		dir=dir[index].mean()
		Norm=np.append(Norm,speed)
		Theta=np.append(Theta,dir)


V=np.cos(map(math.radians,Theta+180))*Norm
U=np.sin(map(math.radians,Theta+180))*Norm


U=U.reshape(len(IniDeg),len(staname))
V=V.reshape(len(IniDeg),len(staname))

# U=U.transpose()
# V=V.transpose()


a=plt.quiver(X,Y,U,V,scale=35)

l,r,b,t = plt.axis()
dx, dy = r-l, t-b
plt.axis([l-0.2*dx, r+0.2*dx, b-0.1*dy, t+0.1*dy])


plt.show()



plt.savefig('hovermoler.png')
plt.close()

#===============================================================================
# Thermal MACHINE
#===============================================================================
Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)


windsta9=station.getvar('Sm m/s').resample("1H",how='median')

def PolarToCartesian(norm,theta):
	"""
	Transform polar to Cartesian where 0 = North, East =90 ....
	"""
	U=norm*np.cos(map(math.radians,-theta+270))
	V=norm*np.sin(map(math.radians,-theta+270))
	return U,V

normwest=Westnet.Data['Sm m/s']
thetawest=Westnet.Data['Dm G']
Uwest,Vwest=PolarToCartesian(normwest,thetawest)

normeast=Eastnet.Data['Sm m/s']
thetaeast=Eastnet.Data['Dm G']
Ueast,Veast=PolarToCartesian(normeast,thetaeast)

Div= Ueast -Uwest
Div=Div.resample("1H",how='mean')

DT_SV_mean=DT_SV.resample("1H",how='median')

# 
# DT_SV_mean=DT_SV_mean[windsta9<5]
# Div=Div[windsta9[windsta9<5].index]
# DI=DI.between_time('11:00','14:00')
DT_SV_mean=DT_SV_mean.between_time('12:00','14:00')
Div=Div.between_time('12:00','14:00')
# windsta9=windsta9.between_time('11:00','14:00')



# 
# DIV=DIV.between_time('11:00','14:00')
# DT_SV_mean=DT_SV_mean.between_time('11:00','14:00')


df=pd.concat([DT_SV_mean,Div],axis=1,join_axes=[Div.index])
df.columns=['DT','Div']

sns.set(style="darkgrid")
color = sns.color_palette()[2]

g = sns.jointplot("DT", "Div", data=df, kind="reg", color=color, size=7)
plt.show()




#===============================================================================
# Heat map 
#===============================================================================


wind=np.sqrt(Serie.dataframe['UGRD_1000mb']**2+Serie.dataframe['VGRD_1000mb']**2)
TCC=CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_']
Hour=3
wind=wind[wind.index.hour==Hour]
TCC=TCC[TCC.index.hour==Hour]


DT_SV_mean=abs(DT_SV.resample("H",how='mean'))
DT_SV_mean=DT_SV_mean[DT_SV_mean.index.hour ==Hour]

# Qwind=pd.Series(pd.qcut(wind,[0,0.25,0.5,0.75,1],labels=wind.quantile([0.25,0.5,0.75,1]).values),index=wind.index)
# QTTC=pd.Series(pd.qcut(TCC,[0,0.25,0.5,0.75,1],
# 					labels=TCC.quantile([0.25,0.5,0.75,1]).values),
# 					index=TCC.index)
# 
# df=pd.concat([Qwind,QTTC, DT_SV_mean],axis=1,join_axes=[wind.index])

df=pd.concat([(wind/5).round(1)*5,(TCC/20).round()*20, DT_SV_mean],axis=1,join_axes=[wind.index])


df=df.drop_duplicates()
df.columns=['wind','TCC','DT']
df_rect=pd.pivot_table(df,index=["TCC"],values=['DT'],columns=['wind'],aggfunc=np.mean)
sns.heatmap(df_rect)
plt.gca().invert_yaxis()
plt.show()

plt.close()


#===============================================================================
# Div by class of Irradiation  
#===============================================================================

Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)


windsta9=station.getvar('Sm m/s').resample("1H",how='mean')

def PolarToCartesian(norm,theta):
	"""
	Transform polar to Cartesian where 0 = North, East =90 ....
	"""
	U=norm*np.cos(map(math.radians,-theta+270))
	V=norm*np.sin(map(math.radians,-theta+270))
	return U,V

normwest=HeadValleyWestnet.Data['Sm m/s']
thetawest=HeadValleyWestnet.Data['Dm G']
Uwest,Vwest=PolarToCartesian(normwest,thetawest)

normeast=HeadValleyEastnet.Data['Sm m/s']
thetaeast=HeadValleyEastnet.Data['Dm G']
Ueast,Veast=PolarToCartesian(normeast,thetaeast)

Div= Ueast -Uwest

# Div=Div[windsta9[windsta9<7].index]

IRsun.columns=['C05']
ClearSkyIrr=IRsun['C05'][Irr_mean.index].groupby(lambda t: (t.hour)).mean() # clear sky irradiance
Irr_mean=Irr['Pira_397'].resample("1H",how='mean')
DT_SV_mean=DT_SV.resample("1H",how='mean')

DI=pd.Series(index=Irr_mean.index)
for i in Irr_mean.index:
	DI[i]=(Irr_mean[i]/ClearSkyIrr[(i.hour)])*100




#DI=DI[AccDailyRain[AccDailyRain < 0.1].index]

# DI=DI[np.isfinite(DI)]
# Div=Div[np.isfinite(Div)]
Div_Irr=Div[DI.index]


#plt.plot(Div_Irr[DI[DI < 30].index].groupby(lambda t: (t.hour)).mean(),label='DI_0_30')
Y=Div_Irr[DI[(DI > 0) & (DI < 50)].index].groupby(lambda t: (t.hour)).mean()
X=Y.index
plt.plot(X,Y,label='DI_0_50')

Y=Div_Irr[DI[(DI > 50) & (DI < 100)].index].groupby(lambda t: (t.hour)).mean()
X=Y.index
plt.plot(X,Y,label='DI_50_100')

plt.legend()
plt.show()

#===============================================================================
# Heat map Div 
#===============================================================================
Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)
windsta9=station.getvar('Sm m/s')


# ClearSkyIrr=Irr['Pira_397'].groupby(pd.TimeGrouper(freq='30Min')).max() # clear sky irradiance
# ClearSkyIrr=ClearSkyIrr.groupby(lambda t: (t.hour,t.minute)).max()
ClearSkyIrr=IRsun['C05'][Irr_mean.index].groupby(lambda t: (t.hour)).mean() # clear sky irradiance
Irr_mean=Irr['Pira_397'].resample("1H",how='mean')
DT_SV_mean=DT_SV.resample("1H",how='mean')
windsta9=windsta9.resample("1H",how='mean')

DI=pd.Series(index=Irr_mean.index)
for i in Irr_mean.index:
	DI[i]=(Irr_mean[i]/ClearSkyIrr[(i.hour)])*100

def PolarToCartesian(norm,theta):
	"""
	Transform polar to Cartesian where 0 = North, East =90 ....
	"""
	U=norm*np.cos(map(math.radians,-theta+270))
	V=norm*np.sin(map(math.radians,-theta+270))
	return U,V

normwest=HeadValleyWestnet.Data['Sm m/s']
thetawest=HeadValleyWestnet.Data['Dm G']
#Uwest=np.cos(map(math.radians,thetawest+180))*normwest # wrong
Uwest,Vwest=PolarToCartesian(normwest,thetawest)

normeast=HeadValleyEastnet.Data['Sm m/s']
thetaeast=HeadValleyEastnet.Data['Dm G']
#Ueast=np.cos(map(math.radians,thetaeast+180))*normeast # wrong
Ueast,Veast=PolarToCartesian(normeast,thetaeast)

Div= Ueast - Uwest
Div=Div.resample("30min",how='mean')


DI=DI.between_time('11:00','14:00')
DT_SV_mean=DT_SV_mean.between_time('11:00','14:00')
Div=Div.between_time('11:00','14:00')
windsta9=windsta9.between_time('11:00','14:00')

#------------------------------------------------------------------------------ 
# wind filter
# DI=DI[windsta9 < 5]
# Div=Div[windsta9 < 5]
# DT_SV_mean=DT_SV_mean[windsta9 < 5]


df=pd.concat([(DI/5).round(1)*5,(Div/2).round()*2, DT_SV_mean,windsta9],axis=1,join_axes=[DI.index])


df=df.drop_duplicates()
df.columns=['DI','Div','DT','windsta9']
# df=df[df['windsta9'] < 5]
df_rect=pd.pivot_table(df,index=["DI"],values=['DT'],columns=['Div'],aggfunc=np.mean)
sns.heatmap(df_rect)


plt.gca().invert_yaxis()
plt.show()



#===============================================================================
# Grouped box plot
#===============================================================================
df=pd.concat([wind, CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'], abs(DT_SV)],axis=1,join_axes=[wind.index])
df.columns=['wind','TCC','DT']
df['WindLabel']=pd.qcut(wind,[0,0.25,0.5,0.75,1],labels=['windIq1','windIq2','windIq3','windIq4'])
df['CCLabel']=pd.qcut(CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'],[0,0.25,0.5,0.75,1],labels=['TCCIq1','TCCIq2','TCCIq3','TCCIq4'])
df['Label']=df['WindLabel']+'_'+df['CCLabel']
df['hour']=df.index.hour

f, (ax1, ax2) =plt.subplots(2, 1)
hours=[3,9,15,21]
boxplot = sns.factorplot("hour", "DT", "Label", df, kind="box",palette="PRGn", aspect=1.25, x_order=hours)
boxplot.despine(offset=10, trim=True)
boxplot.set_axis_labels("Hours", "Difference of temperature between valley center and Slope stations")

boxplot = sns.factorplot("hour", "DT", "Label", df, kind="box",palette="PRGn", aspect=1.25, x_order=hours)
boxplot.despine(offset=10, trim=True)
boxplot.set_axis_labels("Hours", "Difference of temperature between valley center and Slope stations")


#===============================================================================
# Scatter plot wind GFS + station9
#===============================================================================
import seaborn as sns

windgfs=np.sqrt(Serie.dataframe['UGRD_1000mb']**2+Serie.dataframe['VGRD_1000mb']**2)

Path='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/C09clear_merge.TXT'
station = LCB_station(Path)

windsta9=station.getvar('Sm m/s').resample("H",how='mean')

df=pd.concat([windgfs,windsta9],axis=1,join_axes=[wind.index])
df.columns=['windgfs','windsta9']

sns.set(style="darkgrid")
color = sns.color_palette()[2]

g = sns.jointplot("windgfs", "windsta9", data=df, kind="reg", color=color, size=7)


#===============================================================================
# Polar plot distribution
#===============================================================================
#------------------------------------------------------------------------------ 
# station
InPath='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/'
out='/home/thomas/'

Hour=21
# Find all the clima and Hydro
Files=glob.glob(InPath+"*")

for File in sorted(Files):
	print(File)
	station=LCB_station(File)
	windsta9=station.getvar('Sm m/s').resample("H",how='mean')
	dirwindsta9=station.getvar('Dm G').resample("H",how='mean')
# 	windsta9=windsta9[windsta9.index.hour==Hour]
# 	dirwindsta9=dirwindsta9[dirwindsta9.index.hour==Hour]
	hist, bin_edges = np.histogram(np.array(dirwindsta9),bins=np.arange(0,380,20))
	hist_norm=(hist/hist.sum())*100
	width=repeat(20*np.pi/180,len(hist_norm))
	bin_rad=(bin_edges[:-1]+10)*(np.pi/180)
	ax = plt.subplot(111, polar=True)
	ax.set_theta_zero_location("N")
	ax.set_theta_direction(-1)  
	bars = ax.bar(bin_rad,hist_norm, width=width, bottom=0.0)
	plt.savefig(station.getpara('staname')+'__'+'-polarplot.png',bbox_inches='tight') # reduire l'espace entre les grafiques
	plt.close()

#------------------------------------------------------------------------------ 
# GFS

Hour=21
def PolarToCartwind(U,V):
	wind_speed=np.sqrt(U**2+V**2)
	theta_deg=np.arctan2(U, V)*(180/np.pi)+180
	return theta_deg,wind_speed

dirgfs,speedgfs=PolarToCartwind(Serie.dataframe['UGRD_1000mb'], Serie.dataframe['VGRD_1000mb'])
dirgfs=dirgfs[dirgfs.index.hour==Hour]


hist, bin_edges = np.histogram(np.array(dirgfs),bins=np.arange(0,380,20))
hist_norm=(hist/hist.sum())*100

width=repeat(20*np.pi/180,len(hist_norm))
bin_rad=(bin_edges[:-1]+10)*(np.pi/180)
ax = plt.subplot(111, polar=True)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)  
bars = ax.bar(bin_rad,hist_norm, width=width, bottom=0.0)
plt.savefig("GFS"+'__'+str(Hour)+'-polarplot.png',bbox_inches='tight') # reduire l'espace entre les grafiques
plt.close()


#===============================================================================
# Hodograph distribution
#===============================================================================

# station
InPath='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/'
out='/home/thomas/'

Hour=21
# Find all the clima and Hydro
Files=glob.glob(InPath+"*")

for File in sorted(Files):
	print(File)
	station=LCB_station(File)
	Dir_deg=station.daily_h()['Dm G']
	Dir=Dir_deg*(np.pi/180)
	speed=station.daily_h()['Sm m/s']
	ax1 = plt.subplot(111,polar = True)
	ax1.set_theta_direction(-1)
	ax1.set_theta_zero_location("N")
	ax1.plot(Dir,speed,'bo-')
	for D,s,i in zip(Dir,speed,speed.index):
		ax1.annotate(str(i), xy=(D,s))
	plt.savefig(station.getpara('staname')+'-hodograph.png',bbox_inches='tight') # reduire l'espace entre les grafiques
	plt.close()



#------------------------------------------------------------------------------ 
# GFS
U=Serie.dataframe['UGRD_1000mb'].groupby(lambda t: (t.hour,t.minute)).mean()
V=Serie.dataframe['VGRD_1000mb'].groupby(lambda t: (t.hour,t.minute)).mean()
dirgfs_deg,speedgfs=PolarToCartwind(U,V)
dirgfs=dirgfs_deg*(np.pi/180)

ax1 = plt.subplot(111,polar = True)
ax1.set_theta_direction(-1)
ax1.set_theta_zero_location("N")

ax1.plot(dirgfs,speedgfs,'ro-')

for Dir,speed,idx in zip(dirgfs,speedgfs,speedgfs.index):
	ax1.annotate(str(idx[0]), xy=(Dir,speed))
	
plt.savefig('GFS_hodograph.png',bbox_inches='tight') # reduire l'espace entre les grafiques
plt.close()

#===============================================================================
# Hodograph distribution + TCC filter
#===============================================================================


TCC=CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_']
TCC=(TCC/25).round()*25


# station
InPath='/home/thomas/PhD/obs-lcb/LCBData/obs/Merge/'
out='/home/thomas/'

Hour=21
# Find all the clima and Hydro
Files=glob.glob(InPath+"*")
ClassTCC=range(25,125,25)

for File in sorted(Files):
	print(File)
	station=LCB_station(File)
	wind=station.getvar('Sm m/s').resample("H",how='mean')
	dirwind_deg=station.getvar('Dm G').resample("H",how='mean')
	dirwind=dirwind_deg*(np.pi/180)
	df=pd.concat([TCC,wind,dirwind],axis=1,join_axes=[TCC.index])
	df.columns=['TCC','wind','dirwind']
	plt.figure(figsize=(21,12))
	ax1 = plt.subplot(111,polar = True)
	ax1.set_theta_direction(-1)
	ax1.set_theta_zero_location("N")
	for c in ClassTCC:
		windclass=df[df['TCC'] == c]['wind']
		dirclass=df[df['TCC'] == c]['dirwind']
		windclass=windclass.groupby(lambda t: (t.hour,t.minute)).mean()		
		dirclass=dirclass.groupby(lambda t: (t.hour,t.minute)).mean()
		ax1.plot(dirclass,windclass,label=str(c))
		handles, labels = ax1.get_legend_handles_labels()
		ax1.legend(handles, labels)
		for D,s,i in zip(dirclass,windclass,windclass.index):
			ax1.annotate(str(i[0]), xy=(D,s))
	plt.savefig(station.getpara('staname')+'-hodograph-synopticcondition.png',bbox_inches='tight') # reduire l'espace entre les grafiques
	plt.close()



