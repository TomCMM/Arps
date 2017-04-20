#===============================================================================
# DESCRIPTION
#    Plot the profile of potential temperature and specific humidity of the PBL 
#===============================================================================

import pandas as pd
import clima_lib.LCBnet_lib as lcb
import matplotlib.pyplot as plt
import glob
from arps_lib.netcdf_lib import arps, BaseVars, SpecVar, netcdf_serie
from clima_lib.Irradiance.irr_lib import LCB_Irr 
import matplotlib
import numpy as np
 
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}
 
matplotlib.rc('font', **font)
 
matplotlib.rcParams['axes.titlesize'] = 20
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['lines.linewidth'] = 3
matplotlib.rcParams['lines.markersize'] = 10
matplotlib.rcParams['xtick.labelsize'] = 14
matplotlib.rcParams['ytick.labelsize'] = 14



if __name__ == '__main__':

    attributes = pd.DataFrame(columns=['Lat', 'Lon'])
# # # #===============================================================================
# # # # Attribute
# # # #===============================================================================
    obs_path = "/home/thomas/phd/obs/staClim/inmet/obs_clean/INMET/A509.txt"
    M_staname = "A509"
        
    AttSta_inmet = lcb.att_sta()
    AttSta_inmet.setInPaths(obs_path)
    stalat = AttSta_inmet.getatt(M_staname, 'Lat')[0]
    stalon = AttSta_inmet.getatt(M_staname, 'Lon')[0]
    print AttSta_inmet.getatt(M_staname, 'Alt')[0]
    attributes.loc[M_staname,:] = [stalat, stalon]
   
    EX_path = '/home/thomas/phd/obs/lcbdata/obs/full_sortcorr/'
    EX_staname = "C05"
         
         
    AttSta_lcb = lcb.att_sta()
    AttSta_lcb.setInPaths(EX_path)
    stalat = AttSta_lcb.getatt(EX_staname, 'Lat')[0]
    stalon = AttSta_lcb.getatt(EX_staname, 'Lon')[0]
    print AttSta_inmet.getatt(EX_staname, 'Alt')[0]
    attributes.loc[EX_staname,:] = [stalat, stalon]
# 
# 
# #===============================================================================
# # Get var ARPS
# #=============================================================================== 
# 
# 
#     sims = [ 's5oc']
#     
#     
#     
#     path = "/dados3/soc/"
#     outpath= "/home/thomas/phd/dynmod/res/soc/"
#     for sim in sims:
#         sim_path=path + sim+"/9kmv4/"
#         sim_outpath = outpath +sim
#         Files=glob.glob(sim_path+"*")
#             
#         Files.sort()
#         Files = Files[:-1]
#             
#         varnames = ['PT', 'QV', 'sm_ms']# does not have the same shape need to be implemented
#     #     varnames = ["QVSFLX", "PTSFLX"]
#     
#     
#         Serie = None
#         ARPS = None
#         BASE= None
#         SPEV = None
#         idx=None
#         ARPS = arps()
#         print Files[0]
#         BASE = BaseVars(Files[0],"ARPS")
#                   
#         SPEV = SpecVar()
#         ARPS.load(BASE)
#         ARPS.load(SPEV)
# #         ARPS.showvar()
#     
#         print attributes
#           
#         idx = ARPS.get_gridpoint_position(attributes['Lat'],attributes['Lon'])
#         Serie = netcdf_serie(Files,'ARPS')
#         
#         print idx
#         
#         
#         data = {}
#         height={}
#         for staname, i,j in zip(attributes.index, idx['i'].values, idx['j'].values):
#             height[staname] = ARPS.get('ZP', Iselect=[[0,10], [i,i+1], [j,j+1]]).flatten()
#             data[staname]={}
#             for var in varnames:
#                 data[staname][var] = Serie.getdfmap(var, Iselect=[[0,1], [0,10], [i,i+1], [j,j+1] ])
# #     
# #         print height
#         for staname in attributes.index:
#             for var in varnames:
#                 df = data[staname][var].groupby(lambda x: (x.hour)).mean().copy()
#                 fig = plt.figure()
#                 ax1 = fig.add_subplot(111)
#                  
#                 for e in df.index:
#                     x =df.loc[e,:]
#                     y = height[staname]
#                     plt.plot(x, y, label=e)
# #                 plt.show()
#                         
#                 # Color lines
#                 colormap = plt.cm.viridis #nipy_spectral, Set1,Paired   
#                 colors = [colormap(p) for p in np.linspace(0, 1,len(ax1.lines))]
#                 for o,r in enumerate(ax1.lines):
#                     r.set_color(colors[o])
#                 plt.title('Vertical profile of the ' + var + ' at the station ' + staname)
#                 plt.xlabel(var)
#                 plt.ylabel("Altitude (m)")
#                 plt.legend(loc="upper left", bbox_to_anchor=(1,1))
# #                 plt.savefig(sim_outpath+"/"+var+staname+'.pdf')
#                 plt.show()
# # # # #      
# # 
# #      
# #      
# #     
    
    
    
  
      