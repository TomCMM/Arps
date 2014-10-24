#!/usr/bin/python
# Thomas Martin 18/12/13

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
from projpytom import P_lcc

#======  User input
filename='r3km.net021600'
InputDirPath='/data1/arps/testtom3/realexp/run/out3km_netcdf/'
OutFilename='surface'
OutDirPath='/home/thomas/PhD/arps/res/AdasInput/'
varname='PT'
sep=7
#===== Read ARPS file
f = netcdf.netcdf_file(InputDirPath+filename, 'r')
var=f.variables[varname][0,1,:,:]-273.15 # Surface temperature in degree Celsus 
var=np.array(var,dtype=np.float64)# ! to be able to round at 2 decimal
elev=f.variables['ZP'][1,:,:]#elevation
date=datetime.datetime.strptime(f.INITIAL_TIME[0:10], '%Y-%m-%d')# date of the file
hour=datetime.datetime.strptime(f.INITIAL_TIME[11:], '%H:%M:%S')# hour of the file
x_stag=f.variables['x_stag']# coordinate X
y_stag=f.variables['y_stag']# coordinate Y
X, Y = np.meshgrid(x_stag[1:]-(x_stag[:].max())/2, y_stag[1:]-(y_stag[:].max())/2)# make matrice of coordinate
lon,lat=P_lcc(X,Y,f.TRUELAT1,f.TRUELAT2,f.CTRLAT,f.CTRLON,True)# convertmatrix of coordinate into Lat/lon matrix
nobs=var.shape[0]*var.shape[1]

#======= Write file 
f_out=open(OutFilename+'.lso', 'w')

#file header
f_out.write(" "+"{} {} {} {}{} {}\n".format(date.strftime('%d-%b-%Y'),hour.strftime('%H:%M:%S')+'.00',str(0).rjust(5),str(0).rjust(4),str(nobs).rjust(sep)*7,9999))

for i in range(var.shape[0]):
        for j in range(var.shape[1]):
                #station header
                f_out.write("{} {} {} {} {} {} {}\n".format(str(varname).rjust(sep),np.around(lat[i][j],decimals=2),str(np.around(lon[i][j],decimals=2)).rjust(sep),str(np.around(elev[i][j],decimals=0)).rjust(5),str("SA").rjust(2),str(hour.strftime('%H%M')).rjust(10), "".rjust(8) ))
                #Data variable:line1
                f_out.write(" {} {} {} {} {} {} {} {} {}\n".format(str(np.round(var[i][j],decimals=1)).rjust(9),str(-99.9).rjust(6),str(-99.9).rjust(5),str(-99.9).rjust(5),str(-99.9).rjust(5),str(-99.9).rjust(5),str(-99.9).rjust(6),str(-99.9).rjust(6),str(-99.9).rjust(6)))
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






