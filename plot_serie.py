#===============================================================================
# Plot temporal serie
#===============================================================================


import numpy as np
import matplotlib.pyplot as plt
import glob 

from netcdf_lib import *
import pandas as pd
from clima_lib.LCBnet_lib import att_sta



if __name__ == "__main__":
# 
    InPath="/dados3/sim_140214/ctrl/"
    Files=glob.glob(InPath+"*")

    Files.sort()
    Files = Files[:-1]
    print Files

    varname = 'PTSFLX'
    times = []
    data =[]
    for file in Files:
        print file
        ARPS = arps()
        BASE = BaseVars(file,"ARPS")
        SPEV = SpecVar()
        ARPS.load(BASE)
        ARPS.load(SPEV)
        ARPS.showvar()
#         time = ARPS.getatt('time')
# #         print time
#         times.append(pd.to_datetime(time))
#         var = ARPS.get(varname)
#         print var
#         data.append(var[0,:,:].mean())
#         BASE = None
#         SPEV = None
#         ARPS = None
#     
#     df = pd.DataFrame(data, index=pd.DatetimeIndex(times))
# 
#     df.plot()
#     plt.xlabel('time')
#     plt.ylabel('Surface heat flux (K kg m-1 s-2)')
#     plt.show()
# # #         df.columns = idx.index
# 
# #         df.to_csv("/home/thomas/phd/dynmod/res/sim_111115/data/"+var+ "_at_stations_position.csv")