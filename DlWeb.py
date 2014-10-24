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











