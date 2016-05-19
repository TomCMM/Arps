import glob
import subprocess

# InPath="/dados2/gfs/"
#Files=glob.glob(InPath+"*.grb2")

# Ceux que j'ai utilisé pour faire la simulation avec assimilation
InPath= "/dados2/arps/sim/realexp/run/inputdata/"
Files=glob.glob(InPath+"*.grib2")


Files.sort()
# Files = Files[390:]

wgrib2Path='/home/thomas/PhD/arps/utility/grib2/wgrib2/wgrib2'
  
for File in Files:
    print "%" * 100
    print File
    subprocess.call(wgrib2Path+' '+File+" -netcdf "+File+'.nc', shell=True)
    

