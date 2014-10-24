# !/usr/bin/python  
#	
#	DESCRIPTION
# 		Program to create the input file of surface observations created with the statistical model to be assimilated in ADAS
#		
#	USER INPUT
#		

#import module
import numpy as np

#===== File Header
#Date (DD-MMM-YYY format)
#UTC Time (HH:MM:SS.SS format)
#Number of mesonet stations
#Number of mesonet stations possible
#Number of SAOs in analysis grid
#Number of SAO’s possible
#Total number of surface stations in analysis grid
#Total number of surface stations in .lso file
#Total number of surface stations possible
#----exemple
#5-MAY-1995 18:00:00.00 83 0 54 176 176 176 137 176 259 400
# Notes -> only the Total number of surface stations in .lso file is used !!! (see ADAS documentation)
ctime="5-MAY-2010"
nmeso="12:00:00.00"
nmesord=-99.9
nsaog=-99.9
nsao=-99.9
nsaord=-99.9
nobsg=-99.9
totObs=-99.9
nobsb= len(data["Irradiance"])*len(data["Irradiance"][1])
maxsta=-99.9

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

staname="TMP"
lat=conversion(data["north:"])
lon=conversion(data["east:"])
elev=182.
DTD="SA"
UTC="1200"
#weather=

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
#Missing Data are indicated by –99.

#Cloud data Lines:
#Cloud Amout (“ CLR”,” SCT”,”-SCT”,” BKN”,”-BKN”,” OVC”,”-OVC”,” X”,or ”-X”)
#Cloud Height (m)

#-----Exemple
#60.0 54.0 50. 7. -100. -100. -99.9 1020.0 1020.7
#	2  2286.0 1371.6 1.0 20.000 -99.9 -99
#		SCT 1371.6
#		OVC 2286.0

#open file to write 
f=open('surface.lso', 'w')

#write in the file
#Header 
f.write("{} {} {} {} {} {} {} {} {} {}\n".format(ctime,nmeso,nmesord,nsaog,nsao,nsaord,nobsg,totObs,nobsb,maxsta))

rows=range(int(data["rows:"]))
cols=range(int(data["cols:"]))
for i in rows:
	for j in cols:
		#station header
		f.write("{} {} {} {} {} {}\n".format(staname,mlat[i][j],mlon[i][j],data[filename[1]][i][j],DTD,UTC))
		#Data variable:line1
		f.write("{} {} {} {} {} {} {} {}\n".format(data[filename[1]][i][j],-99.9,-99.9,-99.9,-99.9,-99.9,-99.9,-99.9))
		#Data variable:line2
		f.write("{} {} {} {} {} {} {}\n".format(-99.9,-99.9,-99.9,-99.9,-99.9,-99.9,-99.9))

#close the file
f.close()


