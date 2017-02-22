from netcdf_lib import *
import pandas as pd

if __name__ == "__main__":
# #===============================================================================
# # Horizontal plot (variable, topography and wind vector)
# #===============================================================================
# #     InPath="/dados1/thomas/sim/NoBCNoMP/out100m_netcdf/"
#     InPath ="/dados1/sim/sim_280715/out300m/" 
#     InPath="/dados1/sim/sim_coldpool/100m_all/v2/"
#     InPath="/dados2/arps/sim_280715/"
#     InPath="/dados2/arps/out300m/"
    InPath="/dados3/"
    Files=glob.glob(InPath+"*")
    Files.sort()
#     Files = Files[7:9]
#     Files= ['/dados1/sim/sim_coldpool/300m/r300m.net012600']    
#     Files= ['/dados1/sim/sim_coldpool/300m/r300m.net000000']    
    print Files
    for Path in Files:
        print(Path)
        ARPS = arps()
        BASE = BaseVars(Path,"ARPS")
        SPEV = SpecVar()
        ARPS.load(BASE)
        ARPS.load(SPEV)
        ARPS.showvar()
        
#         pt = ARPS.get('PT')
#         print pt[:]
        
        print(ARPS.getatt('THISDMP'))
        FIG=ArpsFigures(ARPS)
        fig=plt.figure(figsize=(FIG.getpara('wfig'),FIG.getpara('hfig')))
        plt.suptitle(FIG.getpara('subtitle'),fontsize=20)
#         FIG.setpara('Latmin',-22.40)
#         FIG.setpara('Latmax',-22.2)
#         FIG.setpara('Lonmin',-46.30)
#         FIG.setpara('Lonmax',-46.20)
        FIG.setpara('Altcross',-400)
#         FIG.setpara('Latmin',-24)
#         FIG.setpara('Latmax',-20)
#         FIG.setpara('Lonmin',-50)
#         FIG.setpara('Lonmax',-46)
#         FIG.setpara('nlevel',17)
#         FIG.setpara('varmin',270)
#         FIG.setpara('varmax',290)
        FIG.setpara('nlevel',50)
        FIG.setpara('varmin',275)
        FIG.setpara('varmax',285)
        FIG.setpara('DPI',80)
        FIG.contourf('Tk')
        plt.colorbar()
        FIG.setpara('varmin',600)
        FIG.setpara('varmax',2000)
        FIG.setpara('nlevel',20)
        CS=FIG.contour('ZP')
        CS.ax.grid(True, zorder=0)
        plt.clabel(CS, inline=10, fontsize=15,fmt='%4.f',)
        FIG.setpara('Nbarb',15)
        FIG.setpara('Lbarb',10)
        FIG.windvector()
        plt.show()
#         plt.savefig('/home/thomas/control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'))
        plt.close()
#  
# #===============================================================================
# #  Vertical plot
# #===============================================================================
#     from netcdf_lib import *
# #         
# # #     InPath="/dados2/arps/sim_280715/"
#     Files=glob.glob(InPath+"*")
#     Files.sort()
#     Files = Files[15::]
#     # Files=Files[1:2]
#     for Path in Files:
#         print(Path)
#         ARPS = arps()
#         BASE = BaseVars(Path,"ARPS")
#         SPEV = SpecVar()
#         ARPS.load(BASE)
#         ARPS.load(SPEV)
#         ARPS.showvar()
#         FIG=ArpsFigures(ARPS)
#         fig=plt.figure(figsize=(FIG.getpara('wfig'),FIG.getpara('hfig')))
#         plt.suptitle(FIG.getpara('subtitle'),fontsize=20)
# #         FIG.setpara('Latmin',-22.92)
# #         FIG.setpara('Latmax',-22.86, )
# #         FIG.setpara('Lonmin',-46.2)
# #         FIG.setpara('Lonmax',-46.3)
# #         FIG.setpara('Latmin',-23)
# #         FIG.setpara('Latmax',-20, )
#      
#         FIG.setpara('ATCDC_entireatmosphere_consideredasasinglelayerltmin',0)
#         FIG.setpara('Altmax',20000)
#         FIG.setpara('nlevel',20)
# #         FIG.setpara('Loncross',-45.5)
#         FIG.setpara('Latcross',-21.5)
#         FIG.setpara('varmin',230)
#         FIG.setpara('varmax',300)
#         FIG.setpara('DPI',80)
#         FIG.contourf('Tk')
#         cbar=plt.colorbar()
#         #	cbar.set_ticks(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
#         #	cbar.set_ticklabels(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
#         FIG.setpara('Nbarb',5)
#         FIG.setpara('Lbarb',10)
#         FIG.windvector()
#         #	plt.axis([FIG.getpara('Lonmin'),FIG.getpara('Lonmax'),1000,2000])
# #         plt.savefig('/home/thomas/res_sim280715/control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'), transparent=False)
#         plt.show()
# #         plt.close()


