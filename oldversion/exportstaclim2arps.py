#       DESCRIPTION

#               Import the different station from IAC, INMET and Sinda and write as an input for ADAS

#=====================================================================================================
#===== Library
import csv
import numpy as np

#===== User input
year=13
month=12
day=15
hour=12

#===== Read INMET station
IP_INMET="/home/thomas/PhD/obs-lcb/staClim/INMET/Caldas-MG/dec13/"
fn_INMET="caldas-mg"

with open(IP_INMET+fn_INMET, 'r') as csvfile_INMET:
        reader_INMET=csv.reader(csvfile_INMET)
        header_INMET=reader_INMET.next()
        data_INMET = {}
        for h in header_INMET:
                data_INMET[h]=[]
        for row in reader:
                for h,v in zip(header_INMET,row):
                        data_INMET[h].append(v)


#===== Read IAC station 
IP_IAC="/home/thomas/PhD/obs-lcb/staClim/IAC/DATA/"
fn_IAC="IAC_Wheater_2014.dat"

with open(IP_IAC+fn_IAC, 'r') as csvfile_IAC:
        reader_IAC=csv.reader(csvfile_IAC)
        header_IAC=reader_IAC.next()
        data_IAC = {}
        for h in header_IAC:
                data_IAC[h]=[]
        for row in reader_IAC:
                for h,v in zip(header_IAC,row):
                        data_IAC[h].append(v)
#===== Read Sinda station
IP_sinda="/home/thomas/PhD/obs-lcb/staClim/sinda/CamposdoJordao-SP/dezembro2013/"
fn_sinda="passo4.jsp"

csv.register_dialect('del', delimiter='\t')#specify the separator

with open(IP_sinda+fn_sinda, 'r') as csvfile_sinda:
        reader_sinda=csv.reader(csvfile_sinda,dialect="del")
        header_sinda=reader_sinda.next()
        data_sinda = {}
        for h in header_sinda:
                data_sinda[h]=[]
        for row in reader_sinda:
                for h,v in zip(header_sinda,row):
                        data_sinda[h].append(v)


#TEST IMPORT MULTUIPLE FILE

import os
IP_INMET="/home/thomas/PhD/obs-lcb/staClim/INMET/"
data_INMET = {}
for path, subdirs, files in os.walk(IP_INMET):
        for subdirname in subdirs:
                data_INMET[subdirname]={}
                for filename in files:
                        data_INMET[subdirname][filename]={}
                        with open(os.path.join(path,subdirs, filename), 'r') as csvfile_INMET:
                                reader_INMET=csv.reader(csvfile_INMET)
                                header_INMET=reader_INMET.next()
                                for h in header_INMET:


                                       data_INMET[filename][h]=[]
                                for row in reader_INMET:
                                        for h,v in zip(header_INMET,row):
                                                data_INMET[filename][h].append(v)



import csv
import os
IP_INMET="/home/thomas/PhD/obs-lcb/staClim/INMET/"
year=13
month=12
day=15
hour=12

#import every variable colomn on every file in every subdirectory on the specified directory
# They are classed hierarchically in a dictionnar dic[subdirname][filename][variablename]
data_INMET = {}
for dirname  in os.walk(IP_INMET).next()[1]:
        data_INMET[dirname]={}
        for subdirname in os.walk(IP_INMET+dirname).next()[1]:
                data_INMET[dirname][subdirname]={}
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



