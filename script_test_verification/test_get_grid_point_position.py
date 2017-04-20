#===============================================================================
# DESCRIPTION
#    sCRIPT TO TEST IF THE GRID POINT ATHT THE FUNCTION GET_GRIDPOINT IS CORRECT
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
        'size'   : 8}

matplotlib.rc('font', **font)

matplotlib.rcParams['axes.titlesize'] = 20
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['lines.linewidth'] = 3
matplotlib.rcParams['lines.markersize'] = 10
matplotlib.rcParams['xtick.labelsize'] = 14
matplotlib.rcParams['ytick.labelsize'] = 14



if __name__ == '__main__':

    #===============================================================================
    # Attribute
    #===============================================================================
    staname = "C05"
        
    AttSta_inmet = lcb.att_sta()
    stalat = AttSta_inmet.getatt(staname, 'Lat')[0]
    stalon = AttSta_inmet.getatt(staname, 'Lon')[0]
    staalt =  AttSta_inmet.getatt(staname, 'Alt')[0]
    

    sim_path= "/dados3/soc/s1oc/netcdf/"
    Files=glob.glob(sim_path+"*")
    Files.sort()
    Files = Files[:-1]
        
    varnames = ['Latgrid', 'Longrid']# does not have the same shape need to be implemented

    ARPS = arps()
    BASE = BaseVars(Files[0],"ARPS")       
    SPEV = SpecVar()
    ARPS.load(BASE)
    ARPS.load(SPEV)
    ARPS.showvar()

       
    idx = ARPS.get_gridpoint_position(stalat, stalon)
    Serie = netcdf_serie(Files,'ARPS')

    i = idx['i'].values
    j =  idx['j'].values

    print "Selected horizontal indexes"
    print i 
    print j

    print "Expected altitude =  " + str(staalt)
    print "Selected altitude = " + str(ARPS.get('ZP', Iselect=[[0,1], [i,i+1], [j,j+1]]).flatten())

    print "="*80
    print "Expected latitude =  " + str(stalat)
    print "Selected latitude = " + str(ARPS.get('Latgrid', Iselect=[[0,1], [i,i+1], [j,j+1]]).flatten())
    
    print "="*80
    print "Expected longitude =  " + str(stalon)
    print "Selected longitude = " + str(ARPS.get('Longrid', Iselect=[[0,1], [i,i+1], [j,j+1]]).flatten())   

        
        
