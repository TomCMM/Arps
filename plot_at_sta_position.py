#===============================================================================
# DESCRIPTION
#    Plot variables at stations position
#===============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cloLCBnet_lib import *



def geo_idx(dd, dd_array):
    """
      search for nearest decimal degree in an array of decimal degrees and return the index.
      np.argmin returns the indices of minium value along an axis.
      so subtract dd from all values in dd_array, take absolute value and find index of minium.
     """

    geo_idx = (np.abs(dd_array - dd)).argmin()
    return geo_idx


if __name__ == "__main__":
    AttSta = att_sta()
    latsarps = pd.read_csv('/home/thomas/Lat.csv', index_col=0, header=None)
    lonsarps = pd.read_csv('/home/thomas/Lon.csv', index_col=0, header=None)
     
     
     
    latgrid = np.load('/home/thomas/Latgrid.out.npy')[0,1:,1:]
    longrid = np.load('/home/thomas/Longrid.out.npy')[0,1:,1:]
     
    latsarps = latsarps.iloc[1,:].values
    lonsarps = lonsarps.iloc[1,:].values
 
    print latsarps.min()
    print latsarps.max()
    print lonsarps.min()
    print lonsarps.max()
 
    stanames = AttSta.stations(values=['Ribeirao'])
    stalats = np.array(AttSta.getatt(stanames, "Lat")).astype(np.float)
    stalons = np.array(AttSta.getatt(stanames, "Lon")).astype(np.float)
  
    print stanames
 
    lat_idx = []
    lon_idx = []
        
    for lat,lon in zip(stalats, stalons):
            
        lat_idx.append(geo_idx(float(lat), latsarps))
        lon_idx.append(geo_idx(float(lon), lonsarps))
   
    print lat_idx
    print lon_idx
     
    
#     
#  
 
#     dfPT = pd.read_csv('/home/thomas/PT.csv')
#     dfPT =dfPT.T
#     dfPT = dfPT.iloc[1:,:]
#     dfPT.index = dfPT.index.to_datetime()
#        
#     dfP = pd.read_csv('/home/thomas/P.csv')
#     dfP =dfP.T
#     dfP = dfP.iloc[1:,:]
#     dfP.index = dfP.index.to_datetime()
#   
# #     
# #     pt = f.variables['PT'][0,0,:,:]
# #     p = f.variables['P'][0,0,:,:]
#     df = Tk(dfP, dfPT)
#     df = df-273.15
#     df = df.T
#     
#     print df
#     
#     
#     df.to_csv('/home/thomas/tk.csv')
    df = pd.read_csv('/home/thomas/tk.csv', header=0)
    df = df.T
    df = df.iloc[1:,:]
    print df
    
    arpsindexpoint = np.arange(0,len(df.columns))
    print arpsindexpoint
    arpsindexpoint = np.reshape(arpsindexpoint, (1201, 1201))
    
    print arpsindexpoint[lon_idx,lat_idx]
    
    
    df.iloc[:,arpsindexpoint[lon_idx,lat_idx]].plot()
    plt.show()
    
    

