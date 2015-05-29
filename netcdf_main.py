from netcdf_lib import *

#if __name__ == "__main__":
#===============================================================================
# Horizontal plot (variable, topography and wind vector)
#===============================================================================
InPath="/dados2/sim/out100m_V11_netcdf/out100m_V11_netcdf/"
Files=glob.glob(InPath+"*")
Files.sort()
Files=Files[0:2]# !!!!! control only one file

cphigh = ArpsFigures2.getparamset()

cplow = cphigh

for Path in Files:
	print(Path)
	ARPS = arps()
	BASE = BaseVars(Path)
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
	FIG.setpara('Altcross',-400)
	FIG.setpara('nlevel',10)
	FIG.setpara('varmin',1)
	FIG.setpara('varmax',10)
	FIG.setpara('DPI',80)
	FIG.contourf('VEGTYP')
	plt.colorbar()
	FIG.setpara('varmin',800)
	FIG.setpara('varmax',1400)
	FIG.setpara('nlevel',20)
	CS=FIG.contour('ZP')
	CS.ax.grid(True, zorder=0)
	plt.clabel(CS, inline=10, fontsize=15,fmt='%4.f',)
# 	FIG.setpara('Nbarb',2)
# 	FIG.setpara('Lbarb',6)
# 	FIG.windvector()
	plt.savefig('control'+os.path.basename(Path)+'.png',dpi=FIG.getpara('DPI'))
	plt.close()

#===============================================================================
#  Vertical plot
#===============================================================================
from netcdf_lib import *

InPath="/dados2/sim/out100m_V11_netcdf/out100m_V11_netcdf/"
Files=glob.glob(InPath+"*")
Files.sort()
for Path in Files:
	print(Path)
	ARPS = arps()
	BASE = BaseVars(Path)
	SPEV = SpecVar()
	ARPS.load(BASE)
	ARPS.load(SPEV)
	FIG=ArpsFigures(ARPS)
	fig=plt.figure(figsize=(FIG.getpara('wfig'),FIG.getpara('hfig')))
	plt.suptitle(FIG.getpara('subtitle'),fontsize=20)
	FIG.setpara('Latmin',-22.90)
	FIG.setpara('Latmax',-22.84)
	FIG.setpara('Lonmin',-46.27)
	FIG.setpara('Lonmax',-46.23)
	FIG.setpara('ATCDC_entireatmosphere_consideredasasinglelayerltmin',0)
	FIG.setpara('Altmax',8000, )
	FIG.setpara('nlevel',200)
	FIG.setpara('Latcross',-22.88)
	FIG.setpara('varmin',0)
	FIG.setpara('varmax',1)
	FIG.setpara('DPI',80)
	FIG.contourf('TKE')
	cbar=plt.colorbar()
	cbar.set_ticks(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
	cbar.set_ticklabels(np.arange(FIG.getpara('varmin'),FIG.getpara('varmax')))
	FIG.setpara('Nbarb',1)
	FIG.setpara('Lbarb',6)
	FIG.windvector()
	plt.axis([FIG.getpara('Lonmin'),FIG.getpara('Lonmax'),1000,2000])
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

