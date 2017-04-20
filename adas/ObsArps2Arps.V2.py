#!/usr/bin/python
# Thomas Martin 18/12/13
#	VERSION V2
#		CREATE A MAP OF TEMPERATURE BASE ON A FIT FOUND ON CompareGFS
#		
# This python code permit to export a variable taken from a file output of the ARPS model (.nc)
# and write it in the format readable by ADAS

#  make preliminary test of the effect of the assimilation of better 
# better spatially distributed initial field of surface climatic variables

# For further information about the file format readable by ADAS
# read the user manual
# A short description is written at the end of this program
# Or check the function export2ARPS.py (Thomas Martin)

# USER INPUT:
#-> filename 	name of the ARPS output to use (.nc)
#-> InputdirPath	Path of the file to be inputed
#-> OutDirPath		Path of the folder for the output of the program
#-> Outfilename		Name of the file output
#-> varname		variable to be exported in ADAS
#[To see the full list of variables disponible on the netcdf file: f.variables.keys()]

#===== Module
import numpy as np
from scipy.io import netcdf
import datetime 
from __future__ import division

#======  User input
filename='r300m.net000000'
InputDirPath='/home/thomas/PhD/arps/sim/140214/out300m_control_netcdf/'
OutFilename='surface'
OutDirPath='/home/thomas/PhD/arps/obs/AdasInput/'
varname='PT'
sep=7

#===== Read ARPS file
f = netcdf.netcdf_file(InputDirPath+filename, 'r')
var=f.variables[varname][0,1,:,:]-273.15 # Surface temperature in degree Celsus 
var=np.array(var,dtype=np.float64)# ! to be able to round at 2 decimal
elev=f.variables['ZP'][1,:,:]#elevation
elev=elev[::10,::10]#reduce the number of point

date=datetime.datetime.strptime(f.INITIAL_TIME[0:10], '%Y-%m-%d')# date of the file
hour=datetime.datetime.strptime(f.INITIAL_TIME[11:], '%H:%M:%S')# hour of the file
x_stag=f.variables['x_stag']# coordinate X
y_stag=f.variables['y_stag']# coordinate Y
X, Y = np.meshgrid(x_stag[1:]-(x_stag[:].max())/2, y_stag[1:]-(y_stag[:].max())/2)# make matrice of coordinate
X=X[::10,::10]
Y=Y[::10,::10]

from pyproj import Proj
pnyc = Proj(proj='lcc',datum='WGS84',lat_1=f.TRUELAT1,lat_2=f.TRUELAT2,lat_0=f.CTRLAT,lon_0=f.CTRLON)
lon,lat= pnyc(X,Y, inverse=True)

#========== TRANSFORM THE TEMPERATURE V2


ALTT=[20.0, 539.0, 555.0, 571.0, 574.0, 595.0, 633.0, 662.0, 667.0, 702.0, 705.0, 725.0, 761.0, 763.0, 770.0, 771.0, 771.0, 776.0, 782.0, 789.0, 801.0, 812.0, 828.0, 874.0, 881.0, 897.0, 899.0, 900.0, 902.0, 933.0, 1002.0, 1050.0, 1105.0, 1144.0, 1150.0, 1276.0, 1434.0, 1461.0, 1500.0, 1590.0, 1642.0]


TT=[31.44, 30.0, 26.67, 26.9, 29.26, 28.08, 24.4, 28.82, 27.79, 27.16, 30.5, 27.15, 28.62, 28.5, 29.4, 27.86, 27.86, 27.84, 28.78, 27.32, 27.2, 26.91, 26.58, 29.13, 27.88, 27.28, 29.5, 26.82, 27.88, 28.21, 28.02, 27.56, 26.25, 25.5, 24.4, 24.8, 20.0, 18.5, 20.2, 23.5, 24.4]

zz = np.polyfit(ALTT,TT, 3)
ff = np.poly1d(zz)

NewVar=ff(elev)
NewVar=(NewVar*(9/5))+32


#================

#lon,lat=P_lcc(X,Y,f.TRUELAT1,f.TRUELAT2,f.CTRLAT,f.CTRLON,True)# convertmatrix of coordinate into Lat/lon matrix
nobs=NewVar.shape[0]*NewVar.shape[1]

#======= Write file 
f_out=open(OutFilename+'.lso', 'w')

#file header
f_out.write(" "+"{} {} {} {}{} {}\n".format(date.strftime('%d-%b-%Y'),hour.strftime('%H:%M:%S')+'.00',str(0).rjust(5),str(0).rjust(4),str(nobs).rjust(sep)*7,9999))

for i in range(NewVar.shape[0]):
        for j in range(NewVar.shape[1]):
                #station header
                f_out.write("{} {} {} {} {} {} {}\n".format(str(varname).rjust(5),np.around(lat[i][j],decimals=2),str(np.around(lon[i][j],decimals=2)).rjust(sep),str(str(int(elev[i][j]))+'.').ljust(5,'0'),str("SA").rjust(2),str(hour.strftime('%H%M')).rjust(10), "".rjust(8) ))
                #Data variable:line1
                f_out.write(" {} {} {} {} {} {} {} {} {}\n".format(str(np.round(NewVar[i][j],decimals=1)).rjust(9),str(-99.9).rjust(6),str(-99.9).rjust(5),str(-99.9).rjust(5),str(-99.9).rjust(5),str(-99.9).rjust(5),str(-99.9).rjust(6),str(-99.9).rjust(6),str(-99.9).rjust(6)))
                #Data variable:line2
                f_out.write("{} {} {} {} {} {} {}\n".format(str(0).rjust(6),str(-99.9).rjust(7),str(-99.9).rjust(7),str(-99.9).rjust(5),str("-99.900").rjust(7),str(-99.9).rjust(6),str(-99).rjust(4)))

#close the file
f_out.close()

print("################################################################")
print("name of the input file: " + filename)
print("name of the output file: "+ OutFilename)
print("Variable: "+ varname)
print("domain-> Lon(" + str(lon.min())+" to "+str(lon.max())+") Lat("+str(lat.min())+" to "+str(lat.max())+")")
print("Creating a map of "+f.variables[varname].long_name+' in '+f.variables[varname].units+ '\n (Temperature is set in  degree)')
print("Date:"+ str(date) + str(hour))
print("################################################################")
print("Sucessful!!")
print("################################################################")
#====== ADAS FILE DESCITPION
#===== File Header
#Date (DD-MMM-YYY format)
#UTC Time (HH:MM:SS.SS format)
#Number of mesonet stations
#Number of mesonet stations possible
#Number of SAOs in analysis grid
#Number of SAO possible
#Total number of surface stations in analysis grid
#Total number of surface stations in .lso file
#Total number of surface stations possible
#----exemple
#5-MAY-1995 18:00:00.00 83 0 54 176 176 176 137 176 259 400
# Notes -> only the Total number of surface stations in .lso file is used !!! (see ADAS documentation)

#=====Station Header Variables
#Station Name (can be fabricated for special sites)
#Latitude (North)
#Longitude (East)
#Station Elevation (m)
#Data Type Designator
#Data Time UTC (HHMM)
#Weather (Using SAO or METAR weather format)
#-----exemple
#DFW 32.90-97.03 182. SA 1200

#======Data Variables and Units:
#Line One:
#Temperature (F)
#Dew Point Temperature (F)
#Wind Direction (degrees from true north)
#Wind Speed (kts)
#Gust Direction (degrees from true north)
#Gust Speed (kts)
#Station Pressure (mb)
#Mean Sea-Level Pressure (mb)
#Altimeter Setting (mb)

#Line Two:
#Number of Cloud Layer Data lines (CLR is one cloud layer line)
#Ceiling Hgt (m)
#Lowest Cloud (m)
#Total Cloud Cover (fraction 0.0-1.0)
#Visibility (mi)
#Solar Radiation (W/m2)
#3-hr coded pressure change (example: 608)
#Missing Data are indicated by -99

#Cloud data Lines:
#Cloud stuf(see the description file of ADAS)
#Cloud Height (m)

#-----Exemple
#60.0 54.0 50. 7. -100. -100. -99.9 1020.0 1020.7
#       2  2286.0 1371.6 1.0 20.000 -99.9 -99
#               SCT 1371.6
#               OVC 2286.0






