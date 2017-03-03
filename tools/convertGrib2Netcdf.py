import glob
import subprocess

# InPath="/dados2/gfs/"
#Files=glob.glob(InPath+"*.grb2")

# InPath= "/dados3/gfs/"
# InPath= "/dados2/gfsZ24/"
InPath= "/dados1/gfsZ96/"
Files=glob.glob(InPath+"*.grb2")


Files.sort()

wgrib2Path='/home/thomas/PhD/arps/utility/grib2/wgrib2/wgrib2'

print Files

for File in Files:
    print "%" * 100
    print File
    subprocess.call(wgrib2Path+' '+File+" -netcdf "+File+'.nc', shell=True)
    

