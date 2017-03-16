import glob
import subprocess

InPath= "/dados2/gfs/fnl/2014/"
Files=glob.glob(InPath+"*.grib2")

Files = ["/dados2/gfs/fnl/2014/fnl_20140214_12_00.grib2"]
Files.sort()

wgrib2Path='/home/thomas/phd/dynmod/tools/grib2/wgrib2/wgrib2'

print Files

for File in Files:
    print "%" * 100
    print File
    subprocess.call(wgrib2Path+' '+File+" -netcdf "+File+'.nc', shell=True)
    

