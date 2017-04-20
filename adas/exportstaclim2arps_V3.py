#       DESCRIPTION


#               Import the different station from IAC, INMET and Sinda and write as an input for ADAS

#	VERSION	
#		Import sinda and INNMET and Write correctly INNMET AND SINDA. 

# 	IMPORTANT
#		Sinda
#	 		-> Les informations des station sinda doivent etre mise manuelement a la ligne!!!
#	
#	Information about
#		Radiation
#			Due to strange value the data of radiation are not included both for INMET and SINDA
#		INMET
#			Radiacion was in cal/(s.mm2)*2.4=w/m2
#=====================================================================================================

#===== Library
import csv
import numpy as np
from __future__ import division
import os
import datetime

#===== User Imput
#-----Input Path 
IP_INMET="/home/thomas/PhD/obs-lcb/staClim/INMET/"# INMET 
IP_sinda="/home/thomas/PhD/obs-lcb/staClim/sinda/"# SINDA

#-----Simulation date
hour='12'# obs hour
dateNeed='10/02/2014'# obs date

#----- Output
OutFilename='surface'#outfile name 
OutDirPath='/home/thomas/PhD/arps/obs/AdasInput/'# Out file path 
infosta='stainfo'# file name of the station information

#===== IMPORT DATA
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



#===== WRITE Obs in ADAS
#-format option
sep=7 # 
Nsta=0 # Number of station counter


# Merge Data
data={'data_INMET':data_INMET,'data_sinda':data_sinda}
#create a dictionnary for the specific name of the variables which depend of the network
var_INMET={'hour':'hora','date':'data','Altitude':'Altitude','Longitude':'Longitude','Latitude':'Latitude','T':'temp_inst','Td':'pto_orvalho_inst','Vvel':'vento_vel','Vdir':'vento_direcao','P':'pressao','I':'radiacao'}
var_sinda={'hour':'DataHora','date':'DataHora','Altitude':'Altitude','Longitude':'Longitude','Latitude':'Latitude','T':'TempAr','Td':'UmidRel','Vvel':'VelVento10m','Vdir':'DirVento','P':'PressaoAtm','I':'RadSolAcum'}
varname={}
varname['data_INMET']=var_INMET
varname['data_sinda']=var_sinda


#====== Function to convert the format
#As the format of the data are different between the network, the following function permit to transform this 
def same(var):
	var=[var]
	return(var)

def same2(var):
	return var

def SindaDate(var):
	sp=var.split()[0]
	sp=datetime.datetime.strptime(sp,'%Y-%m-%d').strftime('%d/%m/%Y')
	return [sp]

def SindaHora(var):
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

#----- Dictionnary with conversion
conv_sinda={'hour':SindaHora,'date':SindaDate,'elev':same2}
conv_INMET={'hour':same,'date':same,'elev':INMETAlt}
conv={}
conv['data_INMET']=conv_INMET
conv['data_sinda']=conv_sinda

#===== WRITE
f_out=open(OutDirPath+OutFilename+'.lso', 'w')
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
							#station header
		                                	f_out.write("{} {} {} {} {} {} {}\n".format(\
rede[-3::].rjust(sep),\
str(np.around(float(data[rede][station]['stainfo'][varname[rede]['Latitude']]),decimals=2)),\
str(np.around(float(data[rede][station]['stainfo'][varname[rede]['Longitude']]),decimals=2)).rjust(sep),\
str(np.around(float(conv[rede]['elev'](data[rede][station]['stainfo'][varname[rede]['Altitude']])),decimals=0)).rjust(5),\
str("SA").rjust(2),str(hour+'00').rjust(10), "".rjust(8) ))
							#first line
							f_out.write(" {} {} {} {} {} {} {} {} {}\n".format(\
str(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['T']][idx]''','*(9/5)','+32')).rjust(9),\
str(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['Td']][idx]''','*(9/5)','+32')).rjust(6),\
str(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['Vdir']][idx]''','','')).rjust(5),\
str(float(np.around(NoObs('''data[rede][station][monthfolder][monthfile][varname[rede]['Vvel']][idx]''','*1.94384449',''),decimals=1))).rjust(5),\
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

f_out.close()

#====== Write the station header at the top of the file (At the end because the number of station must be known)
f_out=open(OutDirPath+OutFilename+'.lso')
text = f_out.read()
f_out.close() 

f_out= open(OutDirPath+OutFilename+'.lso','w')
f_out.write(" "+"{} {} {} {}{} {}\n".format(datetime.datetime.strptime(dateNeed,'%d/%m/%Y').strftime('%d-%b-%Y'),hour+':00:00.00',str(0).rjust(5),str(0).rjust(4),str(Nsta).rjust(sep)*7,9999))
f_out.write(text) 
f_out.close()










