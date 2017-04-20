#===============================================================================
# DESCRIPTION
#    Compare the simulated radiation with the observed radiation
#===============================================================================

import pandas as pd
import clima_lib.LCBnet_lib as lcb
import matplotlib.pyplot as plt
import glob
from arps_lib.netcdf_lib import *
from clima_lib.Irradiance.irr_lib import LCB_Irr 
import matplotlib 

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}

matplotlib.rc('font', **font)
 
matplotlib.rcParams['axes.titlesize'] = 10
matplotlib.rcParams['axes.labelsize'] = 8
matplotlib.rcParams['lines.linewidth'] = 2
matplotlib.rcParams['lines.markersize'] = 8
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8
matplotlib.rcParams['legend.fontsize'] = 8
# plt.rc('legend',fontsize=20)


if __name__ == '__main__':

# 
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
    attributes.loc[M_staname,:] = [stalat, stalon]
  
    EX_path = '/home/thomas/phd/obs/lcbdata/obs/full_sortcorr/'
    EX_staname = "C09"
        
        
    AttSta_lcb = lcb.att_sta()
    AttSta_lcb.setInPaths(EX_path)
    stalat = AttSta_lcb.getatt(EX_staname, 'Lat')[0]
    stalon = AttSta_lcb.getatt(EX_staname, 'Lon')[0]
    attributes.loc[EX_staname,:] = [stalat, stalon]
  
# #=============================================================================
# # Read data
# #===============================================================================
    # Monte verde
    M = lcb.LCB_station(AttSta_inmet.getatt(M_staname, 'InPath')[0], net="INMET")
    df_obs_M = M.getData(['Rad w/m2', 'Ta C', 'Ua g/kg'])
    df_obs_M.columns = ['Rad_M', 'T_M','QV_M']
    
    # EX
    EX = lcb.LCB_station(AttSta_lcb.getatt(EX_staname, 'InPath')[0], net="LCB")
    df_obs_EX = EX.getData([ 'Ta C', 'Ua g/kg'])
        
    irr = LCB_Irr()
    inpath_obs = '/home/thomas/phd/obs/lcbdata/obs/irradiance/data/'
    files_obs = glob.glob(inpath_obs+"*")
    irr.read_obs(files_obs)
    df_irr = irr.data_obs
    df_irr = df_irr.loc[:,['Pira_397','Pira_369' ]].mean(axis=1)
    print df_irr.index
    
#        
    df_obs_EX = pd.concat([df_irr, df_obs_EX], axis=1, join='outer')
    df_obs_EX.columns = ['Rad_EX', 'T_EX','QV_EX']
    print df_obs_EX
    
    
    df_obs = pd.concat([df_obs_EX, df_obs_M], axis=1, join='outer')
#     df_obs.plot()
#     plt.show()
#        
    
#===============================================================================
# Get var ARPS
#=============================================================================== 
#     sims = ['out9kmk1','out9kmk2','out9kmk3','out9kmk4', 'out9kmk5', 'out9kmk6', 'out9kmk7', 'out9kmk8', 'out9kmk9']

    sims = ['out1kmk3']
    outpath = "/home/thomas/phd/dynmod/res/soc/s5oc/kx/"
    sim_path="/dados3/soc/s5oc/"
    
    for sim in sims:
        Files=glob.glob(sim_path+sim+"/*")
            
        Files.sort()
        Files = Files[:-1]
            
        varnames = ['Tc',"RADSW",'QV', "QVSFLX_wm2", "PTSFLX_wm2", "RNFLX"]
        varnames2 = ['TSOIL', 'QSOIL']# does not have the same shape need to be implemented
    #     varnames = ["QVSFLX", "PTSFLX"]
        
    
    
    
        ARPS = arps()
        BASE = BaseVars(Files[0],"ARPS")
                  
        SPEV = SpecVar()
        ARPS.load(BASE)
        ARPS.load(SPEV)
        ARPS.showvar()
    
        idx = ARPS.get_gridpoint_position(attributes['Lat'],attributes['Lon'])
        print idx
        Serie = netcdf_serie(Files,'ARPS')
          
        df_sim = pd.DataFrame()          
        for var in varnames:
            df = Serie.getdfmap(var,select_points=[[0]*len(idx),[0]*len(idx), idx['i'].values, idx['j'].values])
            print df
            df_sim = pd.concat([df_sim, df],join='outer', axis=1)
    #         
        for var in varnames2:
            df = Serie.getdfmap(var,select_points=[[0]*len(idx),[0]*len(idx),[0]*len(idx), idx['i'].values, idx['j'].values])
            df_sim = pd.concat([df_sim, df],join='outer', axis=1)
              
        df_sim.columns = ['T_M', 'T_EX', 'Rad_M', 'Rad_EX', 'QV_M', 
                          'QV_EX', 'LH_M', 'LH_EX', 'H_M', 'H_EX',
                            'RNFLX_M', 'RNFLX_EX',
                           'Tsoil_M', 'Tsoil_EX', 'Qsoil_M', 'Qsoil_EX',
                            
                           ]
        df_sim.loc[:,['Tsoil_M', 'Tsoil_EX']] = df_sim.loc[:,['Tsoil_M', 'Tsoil_EX']] -273.15
           
    # #===============================================================================
    # # Merge
    # #===============================================================================

        df_obs = df_obs.loc[df_sim.index,:]
    #     df_obs_EX = df_obs_EX.loc[df_sim.index,:]
    #     print df_obs_EX
               
        df_T = pd.concat([df_sim.loc[:,['T_EX', 'T_M']], df_obs.loc[:,['T_EX', 'T_M']] ], join='outer', axis=1)
        df_T.columns = ['sim_EX','sim_M', 'obs_EX','obs_M']
        print df_T
                           
        df_Rad = pd.concat([df_sim.loc[:,['Rad_EX', 'Rad_M']], df_obs.loc[:,['Rad_EX', 'Rad_M']]], join='outer', axis=1)
        df_Rad.columns = ['Rad_EX_sim','Rad_M_sim', 'Rad_EX_obs','rad_M_obs']
        print df_Rad
                 
        df_QV = pd.concat([df_sim.loc[:,['QV_EX', 'QV_M']]*1000, df_obs.loc[:,['QV_EX', 'QV_M']]], join='outer', axis=1)
    #     df_QV.columns = ['sim_EX','sim_M', 'obs_EX','obs_M']
        print df_QV
               
    #       
    # #===============================================================================
    # # Plot
    # #===============================================================================
    #     
        
        f, (ax1, ax2, ax3, ax4) = plt.subplots(4,sharex=True)
        print df_T
        df_T.plot(ax = ax1, style = ['--','--','-','-'], color = ['#1E87C7','#c8994b', '#1E87C7', '#c8994b'])
        ax1.set_xlabel('time (s)')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('Temp (C)')
            
                              
        df_QV.plot(ax = ax2, style = ['--','--','-','-'], color = ['#1E87C7','#c8994b', '#1E87C7', '#c8994b'],legend=False)
        ax2.set_ylabel('Specific Humidity (g/kg)')
        ax2.set_ylim((10,17))
                
        df_sim.loc[:,['Tsoil_M', 'Tsoil_EX']].plot(ax =ax3, color = ['#1E87C7', '#c8994b'],legend=False)
        ax3.set_ylabel('Soil Temperature')
                
                
        df_sim.loc[:,['Qsoil_M', 'Qsoil_EX']].plot(ax =ax4, color = ['#1E87C7', '#c8994b'],legend=False)
        ax4.set_ylabel('Soil Moiture (kg/m2)')
             
        
        plt.show()
#         plt.savefig(outpath + sim+'validation_station.pdf')
       
        f, ax = plt.subplots()
    #     ax2 = ax1.twinx()
        df_Rad.plot(ax = ax, style = ['--','-','--','-'], color = ['#e3170a', '#e3170a','#fcb0b3', '#fcb0b3'],legend=True)
        ax.set_ylabel('Flux (W m--2)')
           
        df_sim.loc[:,['H_M', 'H_EX']].plot(ax =ax, style= ['--','-'], color =  '#ec9801',legend=True)
    #     ax2.set_ylabel('Sensible Heat flux (W/m2)')
        df_sim.loc[:,['LH_M', 'LH_EX']].plot(ax =ax, style= ['--','-'], color = '#3b4873',legend=True)
          
      
    #     df_sim.loc[:,['RADSWNET_M', 'RADSWNET_EX']].plot(ax =ax, style= ['--','-'], color = '#17e99e',legend=True)
          
        df_sim.loc[:,['RNFLX_M', 'RNFLX_EX']].plot(ax =ax, style= ['--','-'], color = '#aabedc',legend=True)
          
#         plt.savefig(outpath + sim+'fluxes.pdf')
        plt.show()
       
        ARPS.close()