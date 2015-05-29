import glob
import subprocess

InPath="/dados2/gfs/"
Files=glob.glob(InPath+"*201504*012.grb2")
Files.sort()

wgrib2Path='/home/thomas/Downloads/grib2/wgrib2/wgrib2'

for File in Files:
    subprocess.call(wgrib2Path+' '+File+" -netcdf "+File+'.nc', shell=True)

