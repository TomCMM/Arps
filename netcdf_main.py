from netcdf_lib import *

#if __name__ == "__main__":
#===============================================================================
# Horizontal plot (variable, topography and wind vector)
#===============================================================================
InPath="/home2/thomas/sim/NoBCNoMP/out100m_netcdf/"
Files=glob.glob(InPath+"*")
Files.sort()

#Files=Files[0:1]# !!!!! control only one file

# cphigh = ArpsFigures2.getparamset()
# 
# cplow = cphigh

for Path in Files:
	print(Path)
	ARPS = arps()
	BASE = BaseVars(Path,"ARPS")
	SPEV = SpecVar()
	ARPS.load(BASE)
	ARPS.load(SPEV)
	print(ARPS.getatt('THISDMP'))
	FIG=ArpsFigures(ARPS)
	fig=plt.figure(figsize=(FIG.getpara('wfig'),FIG.getpara('hfig')))
	plt.suptitle(FIG.getpara('subtitle'),fontsize=20)
	FIG.setpara('Latmin',-22.90)
	FIG.setpara('Latmax',-22.84, )
	FIG.setpara('Lonmin',-46.28)
	FIG.setpara('Lonmax',-46.22)
# 	FIG.setpara('Latmin',-22.95)
# 	FIG.setpara('Latmax',-22.80, )
# 	FIG.setpara('Lonmin',-46.3)
# 	FIG.setpara('Lonmax',-46.15)
	FIG.setpara('Altcross',-400)
	FIG.setpara('nlevel',100)
	FIG.setpara('varmin',-1)
	FIG.setpara('varmax',1)
	FIG.setpara('DPI',80)
	FIG.contourf('PTSFLX')
	plt.colorbar()
	FIG.setpara('varmin',800)
	FIG.setpara('varmax',1800)
	FIG.setpara('nlevel',20)
	CS=FIG.contour('ZP')
	CS.ax.grid(True, zorder=0)
	plt.clabel(CS, inline=10, fontsize=15,fmt='%4.f',)
	FIG.setpara('Nbarb',2)
	FIG.setpara('Lbarb',10)
	FIG.windvector()
	plt.savefig('control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'))
	plt.close()

#===============================================================================
#  Vertical plot
#===============================================================================
from netcdf_lib import *

InPath="/home2/thomas/sim/NoBCNoMP/out100m_netcdf/"
Files=glob.glob(InPath+"*")
Files.sort()
# Files=Files[1:2]
for Path in Files:
	print(Path)
	ARPS = arps()
	BASE = BaseVars(Path,"ARPS")
	SPEV = SpecVar()
	ARPS.load(BASE)
	ARPS.load(SPEV)
	FIG=ArpsFigures(ARPS)
	fig=plt.figure(figsize=(FIG.getpara('wfig'),FIG.getpara('hfig')))
	plt.suptitle(FIG.getpara('subtitle'),fontsize=20)
	FIG.setpara('Latmin',-22.92)
	FIG.setpara('Latmax',-22.86, )
	FIG.setpara('Lonmin',-46.2)
	FIG.setpara('Lonmax',-46.3)
	FIG.setpara('ATCDC_entireatmosphere_consideredasasinglelayerltmin',0)
	FIG.setpara('Altmax',4000, )
	FIG.setpara('nlevel',100)
	FIG.setpara('Loncross',-46.25)
	FIG.setpara('varmin',295)
	FIG.setpara('varmax',310)
	FIG.setpara('DPI',80)
	FIG.contourf('PT')
	cbar=plt.colorbar()
#	cbar.set_ticks(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
#	cbar.set_ticklabels(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
	FIG.setpara('Nbarb',1)
	FIG.setpara('Lbarb',6)
	FIG.windvector()
#	plt.axis([FIG.getpara('Lonmin'),FIG.getpara('Lonmax'),1000,2000])
	plt.savefig('control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'), transparent=False)
	plt.close()



#===============================================================================
# Get variable at a point
#===============================================================================
from netcdf_lib import *
import pandas as pd
import sns


InPath="/dados2/gfs/"

Files=glob.glob(InPath+"*nc")
Files.sort()

model='GFS_for'


Serie = netcdf_serie(Files,model)

U_gfs=Serie.get('UGRD_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]])# permit to avoid "too many file problem"
V_gfs=Serie.get('VGRD_1000mb',select=[[0],[-22.86],[360-46.28,360-46.29]])
#T_gfs=Serie.get('Tk',select=[[100000],[-22.86],[360-46.28,360-46.29]])['Tk']
CC_gfs=Serie.get('TCDC_entireatmosphere_consideredasasinglelayer_',select=[[0],[-22.86],[360-46.28,360-46.29]])
Serie.dataframe.index
CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'].columns=['TCC']

#------------------------------------------------------------------------------ 
# WIND histograme 
wind=np.sqrt(Serie.dataframe['UGRD_1000mb']**2+Serie.dataframe['VGRD_1000mb']**2)
TCC=CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_']
#------------------------------------------------------------------------------ 
# DISTRIBUTION WEATHER CONDITIONS
# g = sns.jointplot(wind,CC_gfs['TCC'], kind="kde", size=7, space=0)
#sns.jointplot(wind[wind.index.hour==15],CC_gfs['TCDC_entireatmosphere_consideredasasinglelayer_'][wind.index.hour==15], color="#4CB391")

