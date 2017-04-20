#===============================================================================
# DESCRIPTION
#    Compare model results with station observations
#===============================================================================
from clima_lib.LCBnet_lib import LCB_net, att_sta, LCB_station
import pandas as pd
import matplotlib.pyplot as plt 

if __name__== '__main__':
    
    #===============================================================================
    # User Input
    #===============================================================================
    var = 'Ta C'

    #===========================================================================
    # Import model calculated variables dataframe
    #===========================================================================
    df_model_ctrl = pd.read_csv("/home/thomas/phd/dynmod/res/sim_140214/data/ctrl/Tc_at_stations_position.csv", index_col=0, parse_dates=True)
    df_model_assim_obs = pd.read_csv("/home/thomas/phd/dynmod/res/sim_140214/data/assim_obs/Tc_at_stations_position.csv", index_col=0, parse_dates=True)
    df_model_assim_statmod = pd.read_csv("/home/thomas/phd/dynmod/res/sim_140214/data/assim_statmod/Tc_at_stations_position.csv", index_col=0, parse_dates=True)

    #===============================================================================
    # Import station observation
    #===============================================================================
    net_inmet = LCB_net()
    net_iac = LCB_net()
    net_LCB = LCB_net()
    net_svg =  LCB_net()
    net_peg =  LCB_net()
                   
#     Path_Sinda = '/home/thomas/PhD/obs-lcb/staClim/Sinda/obs_clean/Sinda/'
    Path_INMET ='/home/thomas/phd/obs/staClim/inmet/full/'
    Path_IAC ='/home/thomas/phd/obs/staClim/iac/data/full/'
    Path_LCB='/home/thomas/phd/obs/lcbdata/obs/full_sortcorr/'
    Path_svg='/home/thomas/phd/obs/staClim/svg/SVG_2013_2016_Thomas_30m.csv'
    Path_peg='/home/thomas/phd/obs/staClim/peg/Th_peg_tar30m.csv'
      
    AttSta_IAC = att_sta()
    AttSta_Inmet = att_sta()
    AttSta_LCB = att_sta()
         
    AttSta_IAC.setInPaths(Path_IAC)
    AttSta_Inmet.setInPaths(Path_INMET)
    AttSta_LCB.setInPaths(Path_LCB)
    
    stanames_IAC =  AttSta_IAC.stations(values=['IAC']) # this does not work anymore
    stanames_Inmet = AttSta_Inmet.stations(values=['Innmet'])
    stanames_LCB = AttSta_LCB.stations(values = ['Ribeirao'])

    #------------------------------------------------------------------------------ 
    # Create Dataframe
    #------------------------------------------------------------------------------ 
    Files_IAC =AttSta_IAC.getatt(stanames_IAC,'InPath')
    Files_Inmet =AttSta_Inmet.getatt(stanames_Inmet,'InPath')
    Files_LCB =AttSta_LCB.getatt(stanames_LCB,'InPath')
         
         
    net_inmet.AddFilesSta(Files_Inmet, net='INMET')
    net_iac.AddFilesSta(Files_IAC, net='IAC')
    net_LCB.AddFilesSta(Files_LCB)
#     net_svg.AddFilesSta([Path_svg], net='svg')
#     net_peg.AddFilesSta([Path_peg], net='peg')
    
    df_iac = net_iac.getvarallsta(var=var,by='H')
    df_inmet = net_inmet.getvarallsta(var=var,by='H')
    df_LCB = net_LCB.getvarallsta(var=var, by='H')
    df_svg = LCB_station(Path_svg, net='svg').getData(var=var, by='H')
    df_svg.columns =['svg']
    df_peg = LCB_station(Path_peg, net='peg').getData(var=var, by='H')
    df_peg.columns =['peg']
  
    df_stations = pd.concat([df_iac, df_LCB, df_inmet, df_iac, df_svg, df_peg], axis=1)
    #df_stations = df_stations.resample("H").mean()

    #===========================================================================
    # Get stations in Domain
    #===========================================================================
    
    ax = df_model_ctrl.mean(axis=1).plot(label='ctrl')
    df_model_assim_obs.mean(axis=1).plot(ax=ax,label='assim_obs')
    df_model_assim_statmod.mean(axis=1).plot(ax=ax,label='assim_statmod')
    df_stations.loc[df_model_ctrl.index,df_model_ctrl.columns].mean(axis=1).plot(ax=ax,label='observed')

    plt.legend()
    plt.ylabel('Temperature (C)')
    plt.xlabel('Time')
 
#     plt.savefig('/home/thomas/phd/dynmod/res/sim_111115/comparison_temperature.png')
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


