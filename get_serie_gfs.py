#!/usr/bin/python
#===============================================================================
# DESCRIPTION
#    Get a serie of GFS value
#===============================================================================
import sys
import pandas as pd
from netcdf_lib import *


sys.path.append('/home/thomas/PhD/arps/Arps')
sys.path.append('/home/thomas/PhD/climaP/LCB-net')
sys.path.append('/home/thomas/workspace/statmod')


#===============================================================================
# Get variable at a point
#===============================================================================
# PAS  SUR QUE MON PROGRAMME A UN PROBLEME
# iL CE PEUX SIMPLEMENT QUE CE SOIT LES NETCDF FILES
if __name__=='__main__':
#     InPath="/dados3/gfs/"

#     Files = glob.glob(InPath+"*nc")
#     Files.sort()
    # Files = Files[:400]
    
# file that I use to initialized my simulation with asis
# Files = ['/dados2/arps/sim/realexp/run/inputdata/gfs.t12z.pgrbf00.grib2.nc']
# print len(Files)

Files =['/dados3/gfs/gfs_4_20150603_1800_012.grb2.nc']

model='GFS_for'

# ARPS = arps()
# BASE = BaseVars(Files[0], model)
# ARPS.load(BASE)
# ARPS.showvar()
# 
# VVEL_950mb
# RH_950mb
# HGT_950mb
# CLWMR_500mb
Serie = netcdf_serie(Files,model)

# T = pd.read_csv('/home/thomas/serie.csv')
# T = T.append(Serie.get('TMP_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]]))
df = Serie.get(['TMP_950mb', "VVEL_950mb", "RH_950mb", "HGT_950mb","CLWMR_500mb" ],select=[[0],[-22.86],[360-46.28,360-46.29]])

#     print T
df.to_csv('/home/thomas/gfs_data_GFS_131202.csv')

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
