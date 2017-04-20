#===============================================================================
# DESCRIPTION
#    Use the cnvgrib.x script to convert the the *.grib2 files into the GRIB1 format used by ARPS
#===============================================================================

import glob
import subprocess

def cnv_fname_fnl(file_grib2):
    seg = file_grib2.split('_')
    file_grib1 = seg[0]+'.'+seg[1]+seg[2]+'f'+seg[3][0:2]
    return file_grib1


if __name__ == '__main__':
    cnvgrib = "/home/thomas/phd/dynmod/tools/cnvgrib.x"
    inpath = "/dados2/gfs/s5oc/"
    files_grib2 = glob.glob(inpath+'*.grib2')
    
    #===============================================================================
    # run the script cnvgrib
    #===============================================================================
    for file_grib2 in files_grib2:
        grib1file = cnv_fname_fnl(file_grib2)
        args = [cnvgrib, '-g21', file_grib2, grib1file]
        subprocess.call(args) 



