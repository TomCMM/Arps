#!/usr/bin/python
# DESCRIPTION
#	import file from internet
#
#	download the analysis (f00) and the forecast 3h (f03) 
#	from the indicated moth day hour
# 	for the indicated number of day
#
# TODO
#	find a function which handle the each day of each month (not contstant)
#
# TIPS
#	To create "01" use function zfill : str(1).zfille(2)



import urllib

# ===== USER INPUT
InPath="http://ftpprd.ncep.noaa.gov/data/nccf/com/gfs/prod/"
OutPath="/data1/arps/dataI/gfs/12-17_12_2013/"

month=12
day=01# start at 01 and end at 30 or 31
hour=['00','06','12','18']
fhour=['06']#forecast hour
ForJ=25#for X jour -> min 1 jour

for j in range(0,ForJ):
	for h in hour:
		for fh in fhour:
			# ===== DL data
			folder="gfs.2013"+str(month)+str(day+j).zfill(2)+str(h)+"/"
			filename="gfs.t"+str(h)+"z.pgrb2f"+fh
			url=InPath+folder+filename
			#download
			print("======")
			print("downloading"+" from:  " + InPath)
			print("folder:->"+ folder)
			print("file:->"+filename)
			urllib.urlretrieve(url, OutPath+str(month)+str(day+j).zfill(2)+"-"+filename)
			print("download successful !!!")




#===============================================================================
# NOMAD WEBSITE
#===============================================================================

import urllib

OutPath="/dados2/gfs/"

years=map(str,[2015])
months=map(str,range(01,05))
days=map(str,range(1,32))
hours=map(str,range(0,27,3))

for year in years: 
	for month in months:
		month=month.zfill(2)
		for day in days:
			day=day.zfill(2)
			for hour in hours:
# 				for fhour in hours:
				base="http://nomads.ncdc.noaa.gov/data/gfs4/"
				dirfolder = year+month
				subfolder = year+month+day
				filename = "gfs_4_"+year+month+day+"_"+hour.rjust(2,'0').ljust(4,'0')+"_"+'12'.zfill(3)+".grb2"
				url=base+dirfolder+"/"+subfolder+"/"+filename
				print(url)
				try:
					print("======")
					print("downloading"+" from:  " + url)
					urllib.urlretrieve(url,OutPath+filename)
					print("download successful !!!")
				except:
					print('Not such file or directory')

filename="gfs_4_20140901_0000_000.grb2"
url="http://nomads.ncdc.noaa.gov/data/gfs4/201408/20140820/gfs_4_20140820_0000_000.grb2"
urllib.urlretrieve(url,OutPath+filename)


				
				
				
				
				
