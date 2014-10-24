#       DESCRIPTION


#               Import the different station from IAC, INMET and Sinda and write as an input for ADAS

#	VERSION	5.1
#		CREATE A MAP OF STATION OBSERVATION BASE ON THE GFS ALTITUDE AND THE FIT 

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
OutFilename='SO_T'#outfile name 
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
		else:
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



#===== WRITE
#-format option
sep=7 # 
Nsta=0 # Number of station counter

f_out=open(OutDirPath+OutFilename+'_'+hour+'.lso', 'w')
for rede in data:
	print('------'+'\n'+rede+'\n'+'------')
	for station in data[rede].keys():
		print('\n'+"open the station: "+station)
		for monthfolder in data[rede][station].keys():
			if monthfolder != infosta:
				print("open the month: "+monthfolder)
				for monthfile in data[rede][station][monthfolder].keys():
					for idx,date in enumerate(data[rede][station][monthfolder][monthfile][varname[rede]['date']]):
						if conv[rede]['hour'](data[rede][station][monthfolder][monthfile][varname[rede]['hour']][int(idx)])[0]==hour and conv[rede]['date'](data[rede][station][monthfolder][monthfile][varname[rede]['date']][idx])[0]==dateNeed:
							print("Selected data------["+monthfolder+']------')
							print("write: "+station+monthfolder+'--'+date+'--'+hour)
							Nsta=Nsta+1
							bite=idx
							print('ID de la derniere station :    '+str(bite))
							print('Nombre de station exrite:    '+str(Nsta))
							#station header
		                                	f_out.write("{} {} {} {} {} {} {}\n".format(\
rede[-2::].rjust(5),\
str(np.around(float(NoObs('''data[rede][station]['stainfo'][varname[rede]['Latitude']]''','','')),decimals=2)).ljust(6,'0'),\
str(str(np.around(float(NoObs('''data[rede][station]['stainfo'][varname[rede]['Longitude']]''','','')),decimals=2)).ljust(6,'0')).rjust(sep),\
str(str(int(conv[rede]['elev'](data[rede][station]['stainfo'][varname[rede]['Altitude']])))+'.').ljust(5,'0'),\
str("SA").rjust(2),str(hour+'00').rjust(10), "".rjust(8) ))
							#first line
							f_out.write(" {} {} {} {} {} {} {} {} {}\n".format(\
str(float(np.around(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['T']][idx]''','*(9/5)','+32'),decimals=1))).rjust(9),\
str(float(np.around(NoObs('''str(conv[rede]['Td'](data[rede][station][monthfolder][monthfile][varname[rede]['Td']][idx],data[rede][station][monthfolder][monthfile][varname[rede]['T']][idx]))''','*(9/5)','+32'),decimals=1))).rjust(6),\
str(-99.9).rjust(5),\
str(-99.9).rjust(5),\
str(-99.9).rjust(5),\
str(-99.9).rjust(5),\
str(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['P']][idx]''','','')).rjust(6),\
str(-99.9).rjust(6),\
str(-99.9).rjust(6)))
							#Second line 
							f_out.write("{} {} {} {} {} {} {}\n".format(\
str(0).rjust(6),\
str(-99.9).rjust(7),\
str(-99.9).rjust(7),\
str(-99.9).rjust(5),\
str("-99.900").rjust(7),\
str(-99.9).rjust(6),\
str(-99).rjust(4)))
							print("write: "+station+monthfolder+date+hour)
							Elev=int(conv[rede]['elev'](data[rede][station]['stainfo'][varname[rede]['Altitude']]))
							T=float(np.around(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['T']][idx]''','*(9/5)','+32'),decimals=1))
							Td=float(np.around(NoObs('''str(conv[rede]['Td'](data[rede][station][monthfolder][monthfile][varname[rede]['Td']][idx],data[rede][station][monthfolder][monthfile][varname[rede]['T']][idx]))''','*(9/5)','+32'),decimals=1))
							Vdir=NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['Vdir']][idx]''','','')
							Vvel=float(np.around(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['Vvel']][idx]''','*1.94384449',''),decimals=1))
							

f_out.close()

#====== Write the station header at the top of the file (At the end because the number of station must be known)
f_out=open(OutDirPath+OutFilename+'_'+hour+'.lso')
text = f_out.read()
f_out.close() 

f_out= open(OutDirPath+OutFilename+'_'+hour+'.lso','w')
f_out.write(" "+"{} {} {} {}{} {}\n".format(datetime.datetime.strptime(dateNeed,'%d/%m/%Y').strftime('%d-%b-%Y'),hour+':00:00.00',str(0).rjust(5),str(0).rjust(4),str(Nsta).rjust(sep)*7,9999))
f_out.write(text) 
f_out.close()



