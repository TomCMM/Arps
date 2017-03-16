#===============================================================================
# DESCRIPTION
#        Create a dataframe from a serie of netcdf files
#    TODO
#        Implement a to_df method in the ARPS object
#===============================================================================



from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import glob 

from netcdf_lib import *
import pandas as pd




if __name__ == "__main__":

    InPath="/dados1/sim_coldpool/"
    Files=glob.glob(InPath+"*r100m*")
    Files.sort()
    print Files





#     varnames = ['Latgrid', 'Longrid']
    varnames = ['ZP']
    ARPS = arps()
    BASE = BaseVars(Files[0],"ARPS")
    SPEV = SpecVar()
    ARPS.load(BASE)
    ARPS.load(SPEV)
    ARPS.showvar()



    latgrid = ARPS.get("ZP")
    latgrid = latgrid[0,:,:].flatten()
    print latgrid.shape
    latlon = pd.DataFrame(latgrid ).T
#     latlon.columns = varnames
    latlon = latlon.to_csv('/home/thomas/phd/statmod/data/model_data/ZP.csv')

 
#     latlon = pd.DataFrame([ARPS.get(var) for var in varnames]).T
#     latlon.columns = varnames
#     latlon = latlon.to_csv('/home/thomas/phd/statmod/data/model_data/latlon.csv')
#     print dir(ARPS)
#     print ARPS.f

#     latgrid = ARPS.get("Longrid")
#     latgrid = latgrid[0,:,:].flatten()
#     print latgrid.shape
#     latlon = pd.DataFrame(latgrid ).T
# #     latlon.columns = varnames
#     latlon = latlon.to_csv('/home/thomas/phd/statmod/data/model_data/longrid.csv')
#     print dir(ARPS)
#     print ARPS.f
#     
# 
#     Serie = netcdf_serie(Files,'ARPS')
#         
#     for var in varnames:
#         df = Serie.getdfmap(var,Iselect=[[0,1],[0,1],[0,1201],[0,1201]])
#         print df
#         df = df.T
#         df.to_csv("/home/thomas/phd/statmod/data/model_data/2march/"+var+ "_arps_lastpart.csv")
