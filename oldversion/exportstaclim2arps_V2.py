#       DESCRIPTION

#               Import the different station from IAC, INMET and Sinda and write as an input for ADAS

	#versioN	
#		Import sinda and INNMET and Write correctly INNMET. But dosen't write Sinda yet
#		That why I have save it as a version by itself

# 	IMPORTANT
#	 Les informations des station sinda doivent etre mise manuelement a la ligne!!!
#
#
#	Information about
#		INMET
#			Radiacion was in cal/(s.mm2)*2.4=w/m2
#=====================================================================================================
#===== Library
import csv
import numpy as np
from __future__ import division # PERMIT TO DO DIVISION WITH FLOATTING POINT !!!
import datetime

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


#########TEST IMPORT MULTUIPLE FILE

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

###################33

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



###### Test import all file SINDAcal.cm­².mm­¹.
IP_sinda="/home/thomas/PhD/obs-lcb/staClim/sinda/"
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
				 if row[0]=='Altitude':data_sinda[dirname][os.walk(IP_sinda+dirname).next()[2][0]]["Altitude"]=row[1][1:-1]
		for filename in os.walk(IP_sinda+dirname+"/"+subdirname).next()[2]:
			if filename.find("~")==-1:#avoid backup file from gedit
				data_sinda[dirname][subdirname][filename]={}
				with open(IP_sinda+dirname+"/"+subdirname+"/"+filename, 'r') as csvfile_sinda:
					reader_sinda=csv.reader(csvfile_sinda)
					header_sinda=reader_sinda.next()
					for h in header_sinda:					
						data_sinda[dirname][subdirname][filename][h]=[]
					for row in reader_sinda:
						for h,v in zip(header_sinda,row):
							data_sinda[dirname][subdirname][filename][h].append(v)


#################
###### WRITE ADAS
#################

# User input
OutFilename='surface'
OutDirPath='/home/thomas/PhD/arps/obs/AdasInput/'
varname='PT'
hour='23'
dateNeed='01/03/2014'
infosta='stainfo'
sep=7
nobs=2000
####### INMET

f_out=open(OutDirPath+OutFilename+'.lso', 'w')
#header
f_out.write(" "+"{} {} {} {}{} {}\n".format(datetime.datetime.strptime(dateNeed,'%d/%m/%Y').strftime('%d-%b-%Y'),hour+':00:00.00',str(0).rjust(5),str(0).rjust(4),str(nobs).rjust(sep)*7,9999))
for station in data_INMET.keys():#for all the stationof the INNMET
	print("open the station: "+station)
	for monthfolder in data_INMET[station].keys():# for every month
		if monthfolder != infosta:#select only the data file (and not the info file)
			print("open the month: "+monthfolder)
			for monthfile in data_INMET[station][monthfolder].keys():
				for idx,date in enumerate(data_INMET[station][monthfolder][monthfile]["data"]):
					if data_INMET[station][monthfolder][monthfile]['hora'][int(idx)]==hour and data_INMET[station][monthfolder][monthfile]['data'][idx]==dateNeed:
						#station header
		                                f_out.write("{} {} {} {} {} {} {}\n".format(str(varname).rjust(sep),str(np.around(float(data_INMET[station]['stainfo']['Latitude']),decimals=2)),str(np.around(float(data_INMET[station]['stainfo']['Longitude']),decimals=2)).rjust(sep),str(np.around(float(data_INMET[station]['stainfo']['Altitude'].replace(',','.'))*1000,decimals=0)).rjust(5),str("SA").rjust(2),str(hour+'00').rjust(10), "".rjust(8) ))
						#first line
						f_out.write(" {} {} {} {} {} {} {} {} {}\n".format(str(float(data_INMET[station][monthfolder][monthfile]['temp_inst'][idx])*(9/5)+32).rjust(9),str(float( data_INMET[station][monthfolder][monthfile]['pto_orvalho_inst'][idx])*(9/5)+32).rjust(6),str(data_INMET[station][monthfolder][monthfile]['vento_vel'][idx]).rjust(5),str(float(data_INMET[station][monthfolder][monthfile]['vento_direcao'][idx])*1.94384449).rjust(5),str(-99.9).rjust(5),str(-99.9).rjust(5),str(data_INMET[station][monthfolder][monthfile]['pressao'][idx]).rjust(6),str(-99.9).rjust(6),str(-99.9).rjust(6)))
						#Second line 
						f_out.write("{} {} {} {} {} {} {}\n".format(str(0).rjust(6),str(-99.9).rjust(7),str(-99.9).rjust(7),str(-99.9).rjust(5),str("-99.900").rjust(7),str(-99 if data_INMET[station][monthfolder][monthfile]['radiacao'][idx] =='/////' else float(data_INMET[station][monthfolder][monthfile]['radiacao'][idx])/2.4),str(-99).rjust(4)))
						print("write: "+station+monthfolder+date+hour)





f_out.close()


f_out.write(" "+"{} {} {} {}{} {}\n".format(datetime.datetime.strptime(data_INMET[station][monthfolder][monthfile]['data'][idx],'%d/%m/%Y').strftime('%d-%b-%Y'),datetime.datetime.strptime(data_INMET[station][monthfolder][monthfile]['hora'][idx],'%H').strftime('%H:%M:%S')+'.00',str(0).rjust(5),str(0).rjust(4),str(nobs).rjust(sep)*7,9999))















