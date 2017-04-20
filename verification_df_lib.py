#===============================================================================
# DESCRIPTION
#        Contains object to manipulate ARPS dataframe and stations dataframe for verification
#===============================================================================
import pandas as pd
from scipy.spatial import cKDTree



def find_idxs_at_stations_positions(latgrid, longrid,latlon_sta):
    """
    INPUT:
        lat/longrid from the netcdf file
        lat_lonsta: a dataframe with the latitude/longitude of the stations to select
    Select point at the stations position in dataframe from the ARPS model
    """
    print "Selecting the nearest model gridpoint to the station position"
    tree = cKDTree(zip(latgrid.values.flatten(), longrid.values.flatten()))
    d, inds = tree.query(zip(latlon_sta['Lat'], latlon_sta['Lon']), k = 1)
    idx_sta_in_model = pd.Series(inds, index=latlon_sta.index)
    return idx_sta_in_model

def stations_in_arps_domain(stalatlons, latlon_model):
    """
    Return a Dataframe with the latitude, longitude and names of the stations in the ARPS domain
    """
    latmodelmin = latlon_model.loc[:, 'Lat'].min()
    latmodelmax = latlon_model.loc[:, 'Lat'].max()
    lonmodelmin = latlon_model.loc[:, 'Lon'].min()
    lonmodelmax = latlon_model.loc[:, 'Lon'].max()
    stalats = stalatlons.loc[:,'Lat']
    stalons = stalatlons.loc[:,'Lon']
    stalats = stalats[(stalats > latmodelmin) & (stalats < latmodelmax) ]
    stalons = stalons[(stalons > lonmodelmin) & (stalons < lonmodelmax) ]
    stalatlons = pd.concat([stalats, stalons], axis=1, join='inner')
    return stalatlons
