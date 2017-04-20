#===============================================================================
# DESCRIPTION
#        Create a dataframe from a serie of netcdf files
#    TODO
#        Implement a to_df method in the ARPS object
#===============================================================================



import numpy as np
import matplotlib.pyplot as plt
import glob 

from netcdf_lib import *
import pandas as pd
from clima_lib.LCBnet_lib import att_sta



if __name__ == "__main__":
# 
    InPath="/dados3/sim_111115/"
    Files=glob.glob(InPath+"*")

    Files.sort()
    Files = Files[:-1]
    print Files
# 
# 
    varnames = ['Tc']
    ARPS = arps()
    BASE = BaseVars(Files[0],"ARPS")
     
      
    SPEV = SpecVar()
    ARPS.load(BASE)
    ARPS.load(SPEV)
    print ARPS.showatt()
#     ARPS.showvar()
# 
# #     latgrid = ARPS.get("ZP")
# #     latgrid = latgrid[0,:,:].flatten()
# #     print latgrid.shape
# #     latlon = pd.DataFrame(latgrid ).T
# # #     latlon.columns = varnames
# #     latlon = latlon.to_csv('/home/thomas/phd/statmod/data/model_data/ZP.csv')
# # 
# #  
# #     latlon = pd.DataFrame([ARPS.get(var) for var in varnames]).T
# #     latlon.columns = varnames
# #     latlon = latlon.to_csv('/home/thomas/phd/statmod/data/model_data/latlon.csv')
# #     print dir(ARPS)
# #     print ARPS.f
# 
# #     latgrid = ARPS.get("Longrid")
# #     latgrid = latgrid[0,:,:].flatten()
# #     print latgrid.shape
# #     latlon = pd.DataFrame(latgrid ).T
# # #     latlon.columns = varnames
# #     latlon = latlon.to_csv('/home/thomas/phd/statmod/data/model_data/longrid.csv')
# #     print dir(ARPS)
# #     print ARPS.f
# #     
# # 
# #     Serie = netcdf_serie(Files,'ARPS')
# #           
# #     for var in varnames:
# #         df = Serie.getdfmap(var,Iselect=[[0,1],[0,1],[0,1201],[0,1201]])
# #         print df
# #         df = df.T
# #         df.to_csv("/home/thomas/phd/statmod/data/model_data/2march/"+var+ "_arps_lastpart.csv")
#          
# 
#     #===========================================================================
#     # Dataframe at selected points
#     #===========================================================================
# 
    AttSta = att_sta()
    stalat = AttSta.attributes.loc[:, ['Lat']]
    stalon = AttSta.attributes.loc[:, ['Lon']]
    idx = ARPS.get_gridpoint_position(stalat,stalon)
     
    Serie = netcdf_serie(Files,'ARPS')
            
    for var in varnames:
        df = Serie.getdfmap(var,select_points=[[0]*len(idx),[0]*len(idx), idx['i'].values, idx['j'].values])
        df.columns = idx.index
        print df
        df.to_csv("/home/thomas/phd/dynmod/res/sim_111115/data/"+var+ "_at_stations_position.csv")




