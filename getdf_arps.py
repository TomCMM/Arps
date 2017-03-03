#===============================================================================
# DESCRIPTION
#        Create a dataframe from a serie of netcdf files
#===============================================================================



from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import glob 

from netcdf_lib import *
import pandas as pd




if __name__ == "__main__":

    InPath="/dados1/"
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
        df.to_csv("/home/thomas/phd/statmod/data/model_data/2march/"+var+ "_arps_lastpart.csv")
