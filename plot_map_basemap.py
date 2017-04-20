#===============================================================================
# DESCRIPTION
#    Plot model variable with basemap using shapefile and other information 
#===============================================================================


from netcdf_lib import *
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy

def beautiful_map(var, latgrid, longrid, varunits, title):

    llcrnrlon = longrid.min()
    urcrnrlon = longrid.max()
    llcrnrlat = latgrid.min()
    urcrnrlat = latgrid.max()

    fig     = plt.figure()
    ax      = fig.add_subplot(111)
    
    map = Basemap(projection='mill',lat_ts=10,llcrnrlon=llcrnrlon, \
    urcrnrlon=urcrnrlon,llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat, \
    resolution='i',area_thresh=10000)

    inpath ="/home/thomas/phd/geomap/data/shapefile/"
    
    # brazil regions
    shapefile= inpath + "shapefile_brasil_python/BRA_adm1"
    map.readshapefile(shapefile, 'BRA_adm1', drawbounds=True, linewidth=1.5, color='#536283')
    
    # Cantareira
    shapefile= inpath+ 'cantareira/cantareiraWGS'
    map.readshapefile(shapefile, 'cantareiraWGS', drawbounds=True, linewidth=1.5, color='#48a3e6')
 
    # RMSP
    shapefile= inpath+ 'rmsp/rmsp_polig'
    map.readshapefile(shapefile, 'rmsp_polig', drawbounds=True, linewidth=1.5, color='#890045')
 
    #===============================================================================
    # Draw paralells
    #===============================================================================

    parallels = np.arange(llcrnrlat, -urcrnrlat,1)
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=11, linewidth=0.2)
    # draw meridians
    meridians = np.arange(llcrnrlon, urcrnrlon,1)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=11, linewidth=0.2) 

    map.drawmapscale(urcrnrlon-0.5, llcrnrlat+0.25, urcrnrlon+0.5, llcrnrlat+0.5, 50, barstyle='fancy',fontsize=11,units='km')

    #===========================================================================
    # Background raster
    #===========================================================================

    if var.min() == var.max():
        clevs = np.linspace(0, 1, 10)
    else:
        clevs = np.linspace(var.min(), var.max(), 10)
    
    ny = var.shape[0]; nx = var.shape[1]
    
#     lons, lats = map.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
#     x, y = map(lons, lats) # compute map proj coordinates.
    x, y = map(longrid, latgrid) # compute map proj coordinates.
    
    cs = map.contourf(x, y, var, levels=clevs, cmap=plt.get_cmap('viridis'))
    cbar = map.colorbar(cs,location='right',pad="5%")
    cbar.set_label(varunits)
 
    plt.legend(loc=1, numpoints=1, framealpha=0.4, fontsize=11)
    plt.title(title)
    map.drawmapboundary()
#     plt.show()
    return plt

if __name__ == "__main__":
    # #===============================================================================
    # # Horizontal plot (variable, topography and wind vector)
    # #===============================================================================
    InPath="/dados3/sim_140214/ctrl/"
    outpath = '/home/thomas/phd/dynmod/res/sim_140214/fig/beautifulmap/'
    Files=glob.glob(InPath+"*00")
    Files.sort()

    for Path in Files:
        print(Path)
        ARPS = arps()
        BASE = BaseVars(Path,"ARPS")
        SPEV = SpecVar()
        ARPS.load(BASE)
        ARPS.load(SPEV)
#         ARPS.showvar()
#         ARPS.showatt()
        time = ARPS.getatt('time')
        latgrid = ARPS.get('Latgrid')[0,:,:]
        longrid = ARPS.get('Longrid')[0,:,:]
        varnames =  ARPS.getvarname()
        for varname in varnames:
            print varname
            var = ARPS.get(varname)
            print type(var)
            if not isinstance(var, (np.ndarray, np.generic)): # my calculated variables return a numpy array ..... so I cannot get the units of it 
                if len(var.shape) in [2,3,4]:
                    #### THIS NEEED TO BE IMPLEMENTED IN THE GET OF ARPS
                    if len(var.shape) ==2:
                        data =var[:,:]
                    if len(var.shape) ==3:
                        data =var[0,:,:]
                    if len(var.shape) ==4:
                        data =var[0,0,:,:]
                    if data.shape == latgrid.shape:
                        print var
                        plt = beautiful_map(data, latgrid, longrid, varunits=var.units, title = varname+' '*10+time)
                        if not os.path.exists(outpath+varname):
                            os.makedirs(outpath+varname)
        #                 plt.show()
                        plt.savefig(outpath+varname+'/'+varname+time+'.png')
                
        