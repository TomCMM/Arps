#===============================================================================
# DESCRIPTION
#        Get the netcdf output, select a subset of variables near the surface 
#        and create a dataframe from it.
#===============================================================================



from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import glob 

from netcdf_lib import *
import pandas as pd




if __name__ == "__main__":

    InPath="/dados3/"
    Files=glob.glob(InPath+"*r100m*")
    Files.sort()

    varnames = ['PT','P']#,'ZP','Latgrid','Longrid']
#     varnames = ['Lat', 'Lon']
    ARPS = arps()
    BASE = BaseVars(Files[0],"ARPS")
    SPEV = SpecVar()
    ARPS.load(BASE)
    ARPS.load(SPEV)
    ARPS.showvar()
#     print dir(ARPS)
#     print ARPS.f
    Serie = netcdf_serie(Files,'ARPS')
      
    for var in varnames:
        df = Serie.getdfmap(var,Iselect=[[0,1],[0,1],[0,1201],[0,1201]])
        print df
        df = df.T
        df.to_csv("/home/thomas/"+var+ "_arps_4.csv")
