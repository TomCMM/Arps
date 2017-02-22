#!/usr/bin/python
#===============================================================================
# DESCRIPTION
#    Get a serie of GFS value
#===============================================================================
import sys
import pandas as pd
from netcdf_lib import *
from LCBnet_lib import *

sys.path.append('/home/thomas/PhD/arps/Arps')
sys.path.append('/home/thomas/PhD/climaP/LCB-net')
sys.path.append('/home/thomas/workspace/statmod')
def Tk(P, PT):
    """
    Calculate the Real Temperature in Kelvin
    """
    print("Calculate the Real temperature in Kelvin")
    P0 = 100000
    Rd = 287.06
    Cp = 1004.5
    Tk = PT*(P/P0)**(Rd/Cp)
    return Tk

# 
# varnames = [
#        "ABSV_500mb",
#        "ABSV_550mb",
#        "ABSV_600mb",
#        "ABSV_650mb",
#        "ABSV_700mb",
#        "ABSV_750mb",
#        "ABSV_800mb",
#        "ABSV_850mb",
#        "ABSV_900mb",
#        "ABSV_950mb",
#        "ABSV_975mb",
#        "APCP_surface", # "Total precipitation"
#        "CIN_surface", # Convective Inhibition
#        "CAPE_surface", # Convective Available Potential Energy
#         "CLWMR_500mb",
#         "CLWMR_550mb",
#         "CLWMR_600mb",
#         "CLWMR_650mb",
#         "CLWMR_700mb",
#         "CLWMR_750mb",
#         "CLWMR_800mb",
#         "CLWMR_850mb",
#         "CLWMR_900mb",
#         "CLWMR_950mb",
#         "CLWMR_975mb",
#         "CWAT_entireatmosphere_consideredasasinglelayer_", #Cloud Water
#         "CWORK_entireatmosphere_consideredasasinglelayer_", # Cloud Work Function
#         "DLWRF_surface",# Downward Long-Wave Rad. Flux
#         "DSWRF_surface",# Downward Short-Wave Radiation Flux
#         "GFLUX_surface",# Ground Heat Flux
# #         "GPA_1000mb",# Geopotential Height Anomaly
# #         "GPA_500mb", #Geopotential Height Anomaly
#         "GUST_surface", # Wind Speed (Gust)
#         "HGT_500mb",
#         "HGT_550mb",
#         "HGT_600mb",
#         "HGT_650mb",
#         "HGT_700mb",
#         "HGT_750mb",
#         "HGT_800mb",
#         "HGT_850mb",
#         "HGT_900mb",
#         "HGT_950mb",
#         "HGT_975mb",
#         "HGT_PV_EQ_2eM06_Km_2_kg_s_surface",
#         "HGT_PV_EQ_M2eM06_Km_2_kg_s_surface",
#         "HGT_surface",
#         "HINDEX_surface", # Haines Index
#         "HLCY_3000M0maboveground" # storm relative helicity
#         "HPBL_surface", 
#        "LHTFL_surface", #Latent Heat Net Flux
#        "N4LFTX_surface", # Best (4 layer) Lifted Index
#        "N5WAVA_500mb", #5-Wave Geopotential Height Anomaly
#        "N5WAVH_500mb", #5-Wave Geopotential Height
#        "PEVPR_surface", #Potential Evaporation Rate
#        "PRATE_surface", #Precipitation Rate
#        "PRES_surface",
#        "RH_500mb", 
#        "RH_550mb",
#        "RH_600mb",
#        "RH_650mb",
#        "RH_700mb",
#        "RH_750mb",
#        "RH_800mb",
#        "RH_850mb",
#        "RH_900mb",
#        "RH_950mb",
#        "RH_975mb",
#        "RH_entireatmosphere_consideredasasinglelayer_"
#        "SHTFL_surface", # Sensible heat flux
#        "SOILW_0D1M0D4mbelowground", # Volumetric Soil Moisture Content
#        "SOILW_0D4M1mbelowground", # Volumetric Soil Moisture Content
#        "SOILW_0M0D1mbelowground", # Volumetric Soil Moisture Content
#        "SOILW_1M2mbelowground", # Volumetric Soil Moisture Content
#        "SPFH_2maboveground",#Specific Humidity
#        "SPFH_30M0mbaboveground"
#        "SPFH_80maboveground"
#        "TCDC_boundarylayercloudlayer",#Total Cloud Cover
#        "TCDC_convectivecloudlayer",
#        "TCDC_entireatmosphere_consideredasasinglelayer_",
#        "TCDC_highcloudlayer",
#        "TCDC_lowcloudlayer",
#        "TCDC_middlecloudlayer",
#        "TMAX_2maboveground",
#        "TMIN_2maboveground",
#        "TMP_0D1M0D4mbelowground",
#        "TMP_0D4M1mbelowground",
#        "TMP_0D995sigmalevel",
#        "TMP_0M0D1mbelowground",
#        "TMP_100maboveground",
#        "TMP_1829mabovemeansealevel",
#        "TMP_2743mabovemeansealevel",
#        "TMP_2maboveground",
#        "TMP_30M0mbaboveground",
#        "TMP_3658mabovemeansealevel",
#        "TMP_80maboveground",
#        "TMP_PV_EQ_2eM06_Km_2_kg_s_surface",
#        "TMP_PV_EQ_M2eM06_Km_2_kg_s_surface",
#        "TMP_surface",
#        "TMP_500mb",
#        "TMP_550mb",
#        "TMP_600mb",
#        "TMP_650mb",
#        "TMP_700mb",
#        "TMP_750mb",
#        "TMP_800mb",
#        "TMP_850mb",
#        "TMP_900mb",
#        "TMP_950mb",
#        "TMP_975mb",
#        "UFLX_surface", #Momentum Flux, U-Component
#        "UGRD_10maboveground",
#        "UGRD_100maboveground",
#        "UGRD_1829mabovemeansealevel",
#        "UGRD_2743mabovemeansealevel",
#        "UGRD_30M0mbaboveground",
#        "UGRD_3658mabovemeansealevel",
#        "UGRD_80maboveground",
#        "UGRD_500mb",
#        "UGRD_550mb",
#        "UGRD_600mb",
#        "UGRD_650mb",
#        "UGRD_700mb",
#        "UGRD_750mb",
#        "UGRD_800mb",
#        "UGRD_850mb",
#        "UGRD_900mb",
#        "UGRD_950mb",
#        "UGRD_975mb",
#        "UGRD_maxwind",
#        "UGRD_planetaryboundarylayer",
#        "VFLX_surface", #Momentum Flux, U-Component
#        "VGRD_10maboveground",
#        "VGRD_100maboveground",
#        "VGRD_1829mabovemeansealevel",
#        "VGRD_2743mabovemeansealevel",
#        "VGRD_30M0mbaboveground",
#        "VGRD_3658mabovemeansealevel",
#        "VGRD_80maboveground",
#        "VGRD_500mb",
#        "VGRD_550mb",
#        "VGRD_600mb",
#        "VGRD_650mb",
#        "VGRD_700mb",
#        "VGRD_750mb",
#        "VGRD_800mb",
#        "VGRD_850mb",
#        "VGRD_900mb",
#        "VGRD_950mb",
#        "VGRD_975mb",
#        "VGRD_maxwind",
#        "VGRD_planetaryboundarylayer",
#        "VRATE_planetaryboundarylayer", # ventatilation rate
#        "ULWRF_surface", #Upward Long-Wave Rad. Flux
#        "ULWRF_topofatmosphere",
#        "USWRF_surface",
#        "USWRF_topofatmosphere",
#        "VVEL_500mb",
#        "VVEL_550mb",
#        "VVEL_600mb",
#        "VVEL_650mb",
#        "VVEL_700mb",
#        "VVEL_750mb",
#        "VVEL_800mb",
#        "VVEL_850mb",
#        "VVEL_900mb",
#        "VVEL_950mb",
#        "VVEL_975mb",
#        "VWSH_PV_EQ_2eM06_Km_2_kg_s_surface", #Vertical Speed Shear
#        "VWSH_PV_EQ_M2eM06_Km_2_kg_s_surface" #Vertical Speed Shear
#        ]  


varnames = [
       "ABSV_975mb",
       "APCP_surface", # "Total precipitation"
       "CIN_surface", # Convective Inhibition
       "CAPE_surface", # Convective Available Potential Energy
        "CLWMR_500mb",
        "CLWMR_975mb",
        "CWAT_entireatmosphere_consideredasasinglelayer_", #Cloud Water
        "CWORK_entireatmosphere_consideredasasinglelayer_", # Cloud Work Function
        "DLWRF_surface",# Downward Long-Wave Rad. Flux
        "DSWRF_surface",# Downward Short-Wave Radiation Flux
        "GFLUX_surface",# Ground Heat Flux
        "GPA_1000mb",# Geopotential Height Anomaly
        "GPA_500mb", #Geopotential Height Anomaly
        "GUST_surface", # Wind Speed (Gust)
        "HGT_500mb",
        "HGT_975mb",
        "HGT_surface",
        "HPBL_surface", 
       "LHTFL_surface", #Latent Heat Net Flux
       "N4LFTX_surface", # Best (4 layer) Lifted Index
       "N5WAVA_500mb", #5-Wave Geopotential Height Anomaly
       "N5WAVH_500mb", #5-Wave Geopotential Height
       "PEVPR_surface", #Potential Evaporation Rate
       "PRATE_surface", #Precipitation Rate
       "PRES_surface",
       "RH_500mb", 
       "RH_850mb",
       "RH_900mb",
       "RH_950mb",
       "RH_975mb",
       "RH_entireatmosphere_consideredasasinglelayer_"
       "SHTFL_surface", # Sensible heat flux
       "SPFH_2maboveground",#Specific Humidity
       "SPFH_30M0mbaboveground"
       "SPFH_80maboveground"
       "TCDC_boundarylayercloudlayer",#Total Cloud Cover
       "TCDC_convectivecloudlayer",
       "TCDC_entireatmosphere_consideredasasinglelayer_",
       "TCDC_highcloudlayer",
       "TCDC_lowcloudlayer",
       "TCDC_middlecloudlayer",
       "TMAX_2maboveground",
       "TMIN_2maboveground",
       "TMP_100maboveground",
       "TMP_2maboveground",
       "TMP_30M0mbaboveground",
       "TMP_80maboveground",
       "TMP_PV_EQ_2eM06_Km_2_kg_s_surface",
       "TMP_PV_EQ_M2eM06_Km_2_kg_s_surface",
       "TMP_surface",
       "UFLX_surface", #Momentum Flux, U-Component
       "UGRD_10maboveground",
       "UGRD_100maboveground",
       "UGRD_1829mabovemeansealevel",
       "UGRD_2743mabovemeansealevel",
       "UGRD_30M0mbaboveground",
       "UGRD_3658mabovemeansealevel",
       "UGRD_80maboveground",
       "UGRD_maxwind",
       "UGRD_planetaryboundarylayer",
       "VFLX_surface", #Momentum Flux, U-Component
       "VGRD_10maboveground",
       "VGRD_100maboveground",
       "VGRD_1829mabovemeansealevel",
       "VGRD_2743mabovemeansealevel",
       "VGRD_30M0mbaboveground",
       "VGRD_3658mabovemeansealevel",
       "VGRD_80maboveground",
       "VGRD_maxwind",
       "VGRD_planetaryboundarylayer",
       "VRATE_planetaryboundarylayer", # ventatilation rate
       "ULWRF_surface", #Upward Long-Wave Rad. Flux
       "ULWRF_topofatmosphere",
       "USWRF_surface",
       "USWRF_topofatmosphere",
       "VVEL_500mb",
       "VVEL_800mb",
       "VVEL_850mb",
       "VVEL_900mb",
       "VVEL_950mb",
       "VVEL_975mb",
       "VWSH_PV_EQ_2eM06_Km_2_kg_s_surface", #Vertical Speed Shear
       "VWSH_PV_EQ_M2eM06_Km_2_kg_s_surface" #Vertical Speed Shear
       ]  

if __name__=='__main__':
#===============================================================================
# Get serie ARPS model 
#===============================================================================
#     InPath="/dados2/arps/sim_280715/"
#     Files=glob.glob(InPath+"*")
#     Files.sort()
#     model='ARPS'
#  
#     ARPS = arps()
#     BASE = BaseVars(Files[0],model)
#     SPEV = SpecVar()
#     ARPS.load(BASE)
#     ARPS.load(SPEV)
#     ARPS.showvar()
#     Serie = netcdf_serie(Files,model)
#     df = Serie.get(['PT'],select=[[0],[-400],[-22.86],[-46.28]])
#     print df

#===============================================================================
# Get values multiple stations
#===============================================================================
#     AttSta = att_sta()
# #     stanames = AttSta.stations(all=True)
#     stanames = AttSta.stations(values=['Ribeirao'])
# #     stanames = ['C10']
#     lats = AttSta.getatt(stanames, 'Lat')
#     lons = AttSta.getatt(stanames, 'Lon')
#     print lons
#     print lats
#     print stanames
#     
#     stats = pd.read_csv('/home/thomas/stations_in_domain.csv')
#     lats = stats['lats'].values
#     lons = stats['lons'].values
#     stanames = stats['stanames'].values
#     print len(stanames)
#     
# #     InPath="/dados1/sim/sim_280715/out300m/"
#     InPath="/dados1/sim/sim_coldpool/100m_all/v2/"
# #     InPath="/dados1/sim/NoBCNoMP/out100m_netcdf/"
#     Files=glob.glob(InPath+"*")
#     Files.sort()
#     Files = [Files[5]]
#     print Files    
# #     Files= ['/dados1/sim/sim_coldpool/100m_all/r100m.net023400']
# #     Files= ['/dados3/sim/out100m_V11_netcdf/r100m.net000000']
#     model='ARPS'
#       
#     ARPS = arps()
#     BASE = BaseVars(Files[0],model)
#     SPEV = SpecVar()
#     ARPS.load(BASE)
#     ARPS.load(SPEV)
#     ARPS.showvar()
#     Serie = netcdf_serie(Files,model)
#     var = 'Tk'
#   
#     df = pd.Series(index=stanames, name=var)
#     for lat, lon, sta in zip(lats, lons, stanames):
#         print "T"*80
#         print sta
#         s = Serie.get(['PT', 'P'],select=[[0],[-400],[lat],[lon]])
#         tk = Tk(s['P'],s['PT'] ) 
# #         s = Serie.get([var],select=[[0],[lat],[lon]])
#         print "WHAOU"
# #         df[sta] = s[var] 
#         df[sta] = tk
#         
#      
#     init = pd.read_csv('/home/thomas/arps_coldpool_initial.csv')
#     init.index = df.index
#      
#     print init[var]
#  
#     df = df - init[var]
#     df.to_csv('/home/thomas/arps_coldpool.csv', header=True)
#     print 'alla'
#     print df
    
    
#===============================================================================
# Get variable at a point
#===============================================================================

#     InPath="/dados3/gfs/netcdf/"
    InPath="/dados2/gfsZ24/"
       
    Files = glob.glob(InPath+"*nc")
    Files.sort()
    print Files
#     Files = Files[:-3]
           
    # file that I use to initialized my simulation with asis
    # Files = ['/dados2/arps/sim/realexp/run/inputdata/gfs.t12z.pgrbf00.grib2.nc']
    # print len(Files)
       
#     Files =['/dados3/gfs/gfs_4_20150102_0000_000.grb2.nc']
       
    model='GFS_4'
       
    ARPS = arps()
    BASE = BaseVars(Files[0], model)
    SPEV = SpecVar()
    ARPS.load(BASE)
    ARPS.load(SPEV)
    ARPS.showvar()

    Serie = netcdf_serie(Files,model)
# #     a = Serie.get('TMP_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]])
#        
#     # T = pd.read_csv('/home/thomas/serie.csv')
#     # T = T.append(Serie.get('TMP_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]]))
# #     df = Serie.get(['TMP_950mb', "VVEL_950mb", "RH_950mb", "HGT_950mb","CLWMR_500mb" ],select=[[0],[-22.86],[360-46.28,360-46.29]])
#     df = Serie.get(['TMP_2maboveground', 'TMP_80maboveground','TMP_950mb','TMP_900mb', 'TMP_850mb','TMP_800mb' ,'TMP_750mb','TMP_700mb','TMP_650mb','TMP_600mb','TMP_550mb','TMP_500mb',
#                     'RH_2maboveground','RH_80maboveground','RH_950mb','RH_900mb', 'RH_850mb','RH_800mb','RH_750mb', 'RH_700mb','RH_650mb','RH_600mb', 'RH_550mb','RH_500mb',
#                     'UGRD_10maboveground', 'UGRD_80maboveground','UGRD_950mb','UGRD_900mb', 'UGRD_850mb', 'UGRD_800mb','UGRD_750mb', 'UGRD_700mb', 'UGRD_650mb','UGRD_600mb', 'UGRD_550mb', 'UGRD_500mb',
#                     'VGRD_10maboveground', 'VGRD_80maboveground','VGRD_950mb','VGRD_900mb', 'VGRD_850mb','VGRD_800mb','VGRD_750mb', 'VGRD_700mb','VGRD_650mb','VGRD_600mb', 'VGRD_550mb','VGRD_500mb',
#                     'PRES_surface', 'PRES_80maboveground','HGT_950mb','HGT_900mb','HGT_850mb','HGT_800mb','HGT_750mb','HGT_700mb','HGT_650mb','HGT_600mb','HGT_550mb','HGT_500mb' ]
#                    ,select=[[0],[-22.86],[360-46.28,360-46.29]])
#    

    df = Serie.get(varnames,select=[[0],[-22.86],[360-46.28,360-46.29]])


    df.to_csv('/home/thomas/gfs_data_levels.csv')

#===============================================================================
# To be plot in hovermoller
#===============================================================================


#     U_gfs=Serie.get('UGRD_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]])# permit to avoid "too many file problem"
#     V_gfs=Serie.get('VGRD_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]])
#     CC_gfs=Serie.get('TCDC_entireatmosphere_consideredasasinglelayer_',select=[[0],[-22.86],[360-46.28,360-46.29]])
#     CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'].columns=['TCC']
# 
#     #------------------------------------------------------------------------------ 
#     # WIND histograme 
#     wind=np.sqrt(Serie.dataframe['UGRD_1000mb']**2+Serie.dataframe['VGRD_1000mb']**2)
#     TCC=CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_']
#     
#     U_gfs.plot()
#     plt.show()
#     #------------------------------------------------------------------------------ 
#     # DISTRIBUTION WEATHER CONDITIONS
#     # g = sns.jointplot(wind,CC_gfs['TCC'], kind="kde", size=7, space=0)
#     #sns.jointplot(wind[wind.index.hour==15],CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'][wind.index.hour==15], color="#4CB391")
