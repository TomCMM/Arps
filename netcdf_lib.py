#!/usr/bin/python
#coding: utf-8 # read special character

#======================================================================================================
#    Thomas Feb 2015
#     DESCRIPTION
#        Manipulate, analyse and plot netcdf ARPS output
#    DONE:
# Separation en Class distinct : SpecVar, Basevar, arps, Arps Figures
# 
#     TO BE DONE:
# -> Implement cross section vertical
# -> gestion de varmin and varmax pour determination de la colorbar
# -> Mettre une shape des regions bresilienne
# -> Creer une classe pour visualiser les stations INMET, SInda etc + Ribeirao das Posses
# -> Modifier le module getvar in ArpsFigures to be more clear (maybe install it in the ARPS module)
#======================================================================================================

#=====================
#===== Library
#=====================
from __future__ import division # to be able to get a floatting point (for the divis
import os.path # to check if the file exist 
from scipy.io import netcdf
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.ndimage
from pylab import *
import matplotlib.gridspec as gridspec
import csv
import datetime
import os.path # basename and folder name of a path
import glob # # Import all the file of a folder
import functools
import pandas as pd

class SpecVar():
    Cst={"P0":100000,
        "Rd":287.06,
        "Cp":1004.5,#J/(kg K)
        "Cpd":1004.7,#J/(kg K)
        "Rv":461.52,#
        "Cl":4218,#J/(kg K)
        "Ci":2106,#J/(kg K)
        "Lv":2.501*10**6,#J/Kg
        "g":9.81}

    def __init__(self, arpsobject = None):
        self.module = {
            'QT': self.__QT,
            'PTc': self.__PTc,
            'Phpa': self.__Phpa,
            'Pbarhpa': self.__Pbarhpa,
            'Ptot': self.__Ptot,
            'ThetaV': self.__ThetaV,
            'Tk': self.__Tk,
            'Pv': self.__Pv,
            'Pd': self.__Pd,
            'Psat': self.__Psat,
            'Rh': self.__Rh,
            'ThetaE':self.__ThetaE,
            'Lat':self.__Lat,
            'Lon':self.__Lon,
            'Latgrid':self.__Latgrid,
            'Longrid':self.__Longrid,
            'Tc':self.__Tc
        }
        self.attributes = { }
        self.varname = {
            'QT':'Total hydrometeors',
            'PTc':'Potential Temperature in degree',
            'Phpa':'Pressure in Hectopascale',
            'Pbarhpa':'Pressure in Hectopascale',
            'Ptot':'Total pressure',
            'ThetaV':'Virtual potential temperature',
            'Tk':'Real temperature in Kelvin',
            'Pv':'Vapor pressur in Pa',
            'Pd':'Dry pressure in Pa',
            'Psat':'Pressure at saturation ',
            'Rh':'relative humidity',
            'ThetaE':'potential equivalent temperature',
            'Lon':'Vector position longitude',
            'Lat':'Vector position latitude',
            'Longrid':'matrix Longitude',
            'Latgrid':'matrix latitude',
            'Tc': 'Temperature in degree Celsius'
        }

    def __QT(self, arps):
        """
        Calculate Total hydrometeors
        """
        print("Calculate Total hydrometeors")

        QI = arps.get('QI')
        QH = arps.get('QH')
        QR = arps.get('QR')
        QC = arps.get('QC')
        QS = arps.get('QS')

        data=QI.data + QH.data + QR.data + QC.data + QS.data
        result = scipy.io.netcdf.netcdf_variable(data, QI.typecode(), QI.shape, QI.dimensions)
        result.long_name=self.varname['QT']

        return result
    def __PTc(self, arps):
        """
        Calculate Potential temperature in degree
        """
        print("Calculate Potential temperature in degree")

        PT=arps.get('PT')
        data=PT.data-273.15
        results=scipy.io.netcdf.netcdf_variable(data,PT.typecode(),PT.shape,PT.dimensions)
        results.long_name=self.varname['PTc']
        results.units='C'
        return results
    def __Phpa(self, arps):
        """
        Calculate the Pressure in hectopascale
        """
        print('Calculate the Pressure in Hectopascale')
        P=arps.get('P')
        data=P.data*10**-2
        results=scipy.io.netcdf.netcdf_variable(data,P.typecode(),P.shape,P.dimensions)
        results.long_name=self.varname['Phpa']
        results.units='hpa'
        return results 
    def __Pbarhpa(self, arps):
        """
        Calculate the Pressure in hectopascale
        """
        print('Calculate the pressure in hectopascale')
        PBAR=arps.get('PBAR')
        data=PBAR.data*10**-2
        results=scipy.io.netcdf.netcdf_variable(data,PBAR.typecode(),PBAR.shape,PBAR.dimensions)
        results.long_name=self.varname['Pbarhpa']
        results.units='hpa'

        return results
    def __Ptot(self, arps):
        """
        Calculate the totale Pressure in hectopascale
        """
        print('calculate the totale pressur in hectopascale') 
        Phpa=arps.get('Phpa')
        Pbarhpa=arps.get('Pbarhpa')
        data=Phpa.data+Pbarhpa.data
        results=scipy.io.netcdf.netcdf_variable(data,Phpa.typecode(),Phpa.shape,Phpa.dimensions)
        results.longname=self.varname['Ptot']

        return results
    def __ThetaV(self, arps):
        """
        Calculate the virtual potential temperature
        """
        print("Calculate the virtual potential temperature")
        Eps=self.Cst['Rd']/self.Cst['Rv']

        QT=arps.get('QT')
        PT=arps.get('PT')
        QV=arps.get('QV')
        data=PT.data*((1+(QV.data/Eps))/(1+QT.data))

        results=scipy.io.netcdf.netcdf_variable(data,QT.typecode(),QT.shape,QT.dimensions)
        results.long_name=self.varname['ThetaV']
        results.units='C'

        return results 
    def __Tk(self, arps):
        """
        Calculate the Real Temperature in Kelvin
        """
        print("Calculate the Real temperature in Kelvin")
        P=arps.get('P')
        PT=arps.get('PT')
        data=PT.data*(P.data/self.Cst['P0'])**(self.Cst['Rd']/self.Cst['Cp'])
        results=scipy.io.netcdf.netcdf_variable(data,P.typecode(),P.shape,P.dimensions)
        results.long_name=self.varname['Tk']
        results.units='k'
        return results
    def __Tc(self,arps):
        Tk=arps.get('Tk')
        data=Tk.data-273.15
        results=scipy.io.netcdf.netcdf_variable(data,Tk.typecode(),Tk.shape,Tk.dimensions)
        results.long_name=self.varname['Tc']
        results.units='C'
        return results
    def __Pv(self, arps):
        """
        Calculate the vapor Pressure
        """
        print('Calculate the partial vapor Pressure')
        QV= arps.get('QV')
        P=arps.get('P')
        data=((QV.data*(P.data))/(0.622+QV.data))
        results=scipy.io.netcdf.netcdf_variable(data,QV.typecode(),QV.shape,QV.dimensions)
        results.long_name=self.varname['Pv']
        results.units='Pa'

        return results
    def __Pd(self, arps):
        """
        Calculate the partial dry air pressure
        """
        print('Calculate the partial dry air Pressure')
        Pv=arps.get('Pv')
        P=arps.get('P')
        data=P.data-Pv.data
        results=scipy.io.netcdf.netcdf_variable(data,P.typecode(),P.shape,P.dimensions)
        results.long_name=self.varname['Pd']
        results.units='Pa'

        return results
    def __Psat(self, arps):
        """
        Calculate vapor pressure at saturation
        CIMO GUIDE , WMO, 2006
        """
        print('Calculate the vapor pressure at saturation')
        Tk=arps.get('Tk')
        data=6.112*np.exp(17.62*(Tk.data-273.15)/(243.12+(Tk.data-273.15)))*10**2
        results=scipy.io.netcdf.netcdf_variable(data,Tk.typecode(),Tk.shape,Tk.dimensions)
        results .long_name=self.varname['Psat']

        return results
    def __Rh(self, arps):
        """
        Calculate the relative humidity
        """
        print('Calculate the relative humidity')
        Pv=arps.get('Pv')
        Psat=arps.get('Psat')
        data=(Pv.data/Psat.data)*100
        results=scipy.io.netcdf.netcdf_variable(data,Pv.typecode(),Pv.shape,Pv.dimensions)
        results.long_name=self.varname['Rh']
        results.units='%'

        return results
    def __ThetaE(self, arps):
        """
        Calculate the Equivalent Potential Temperature
        """
        print('Calculate the Equivalent Potential Temperature')
        QT=arps.get('QT')
        Tk=arps.get('Tk')
        Pd=arps.get('PD')
        QV=arps.get('QV')
        Rh=arps.get('Rh')
        rtc=QT.data*self.Cst['Cl']# Total hydrometeor 
        First=Tk.data*(self.Cst['P0']/Pd.data)**(self.Cst['Rd']/(self.Cst['Cpd']+rtc))
        Second=Rh**((-QV.data*self.Cst['Rv'])/(self.Cst['Cpd']+rtc))
        Third=np.exp((self.Cst['Lv']*QV.data)/((self.Cst['Cpd']+rtc)*Tk.data))
        data=First*Second*Third
        results=scipy.io.netcdf.netcdf_variable(data,QV.typecode(),QV.shape,QV.dimensions)
        results.long_name=self.varname['ThetaE']
        results.units='k'

        return results
    def __Lat(self, arps):
        """
        Calculate the matrix latitude longitude of the domain
        based on a Lambert conformal conic projection 
        """
        try:
            from pyproj import Proj
        except ImportError:
            print('Cant find the module pyproj')

        truelat1=arps.getatt('TRUELAT1')
        truelat2=arps.getatt('TRUELAT2')
        ctrlat=arps.getatt('CTRLAT')
        ctrlon=arps.getatt('CTRLON')
        x_stag=arps.get('x_stag')
        y_stag=arps.get('y_stag')

        pnyc = Proj(proj='lcc',datum='WGS84',lat_1=truelat1,lat_2=truelat2,lat_0=ctrlat,lon_0=ctrlon)
        Lon_arps,Lat_arps= pnyc(x_stag[1:]-(x_stag[:].max())/2,y_stag[1:]-(y_stag[:].max())/2, inverse=True)
        Lat=scipy.io.netcdf.netcdf_variable(Lat_arps,x_stag.typecode(),x_stag.shape[0]-1,x_stag.dimensions)
        Lat.long_name=self.varname['Lat']

        return Lat
    def __Lon(self, arps):
        """
        Calculate the matrix latitude longitude of the domain
        based on a Lambert conformal conic projection 
        """
        try:
            from pyproj import Proj
        except ImportError:
            print('Cant find the module pyproj')

        truelat1=arps.getatt('TRUELAT1')
        truelat2=arps.getatt('TRUELAT2')
        ctrlat=arps.getatt('CTRLAT')
        ctrlon=arps.getatt('CTRLON')
        x_stag=arps.get('x_stag')
        y_stag=arps.get('y_stag')
        
        pnyc = Proj(proj='lcc',datum='WGS84',lat_1=truelat1,lat_2=truelat2,lat_0=ctrlat,lon_0=ctrlon)
        Lon_arps,Lat_arps= pnyc(x_stag[1:]-(x_stag[:].max())/2,y_stag[1:]-(y_stag[:].max())/2, inverse=True)

        Lon=scipy.io.netcdf.netcdf_variable(Lon_arps,y_stag.typecode(),y_stag.shape[0]-1,y_stag.dimensions)
        Lon.long_name=self.varname['Lon']
        
        return Lon
    def __Latgrid(self, arps):
        Lat=arps.get('Lat')
        Lon=arps.get('Lon')
        Z=arps.get('z_stag')
        resLat,resLon=np.meshgrid(Lat.data,Lon.data)
        resLat=transpose(resLat)
        Zarray=np.array([1]).repeat(Z.shape)
        resLat=Zarray[:,None,None]*resLat
        Latgrid=scipy.io.netcdf.netcdf_variable(resLat,Lat.typecode(),(Z.shape,Lat.shape,Lon.shape),(Z.dimensions,Lat.dimensions,Lon.dimensions))
        Latgrid.long_name=self.varname['Latgrid']
        return Latgrid

    def __Longrid(self, arps):
        Lat=arps.get('Lat')
        Lon=arps.get('Lon')
        Z=arps.get('z_stag')
        resLat,resLon=np.meshgrid(Lat.data,Lon.data)
        resLon=transpose(resLon)
        Zarray=np.array([1]).repeat(Z.shape)
        resLon=Zarray[:,None,None]*resLon
        Longrid=scipy.io.netcdf.netcdf_variable(resLon,Lon.typecode(),(Z.shape,Lat.shape,Lon.shape),(Z.dimensions,Lat.dimensions,Lon.dimensions))
        return Longrid

class FileProperties():
        def __init__(self,InPath,model):
            self.attributes={
            "model":model,
            "InPath":InPath,
            "dirname":os.path.dirname(InPath),
            "basename":os.path.basename(InPath)
            }
            self.__time(InPath,model)

        def __time(self,InPath,model):
            UTC=3 #Hour
            
            if model == "ARPS":
                filetime=int(os.path.basename(InPath)[-6:])
                initime=self.__dict__["INITIAL_TIME"]
                UTC=UTC*3600
                Init = datetime.datetime.strptime(initime, "%Y-%m-%d_%H:%M:%S")
                Fortime=datetime.timedelta(seconds=filetime)
                UTCtime=datetime.timedelta(seconds=UTC)
                Time=str(Init+Fortime-UTCtime)
                self.attributes['time']=Time
    
            if model == 'GFS':
                """
                ANALYSIS
                fnl_20150424_06_00.grib2.nc
                """
                filetime=os.path.basename(InPath)[4:18]
                Time = datetime.datetime.strptime(filetime, "%Y%m%d_%H_%M")
                Time=Time-datetime.timedelta(hours=UTC)
                self.attributes['time']=Time

            if model == 'GFS_for':
                """
                From Nomade
                Forecast
                gfs_4_20140815_0000_000.grb2.nc
                """
                filetime=os.path.basename(InPath)[6:19]
                Time = datetime.datetime.strptime(filetime, "%Y%m%d_%H%M")
                Time=Time-datetime.timedelta(hours=UTC)
                fortime=datetime.datetime.strptime(os.path.basename(InPath)[21:23], "%H")

                self.attributes['time']=Time
                self.attributes['forecast']=fortime
#             if model == 'GFS2':
#                 """
#                 GFS_Global_0p5deg_20140101_0000_anl.grib2.nc
#                 """
#                 filetime=os.path.basename(InPath)[18:31]
#                 Time = datetime.datetime.strptime(filetime, "%Y%m%d_%H%M")
#                 Time=Time-datetime.timedelta(hours=UTC)
#                 self.attributes['time']=Time
# 
#             if model == 'CFS':
#                 """
#                 GFS_Global_0p5deg_20140101_0000_anl.grib2.nc
#                 """
#                 filetime=os.path.basename(InPath)[18:31]
#                 Time = datetime.datetime.strptime(filetime, "%Y%m%d_%H%M")
#                 Time=Time-datetime.timedelta(hours=UTC)
#                 self.attributes['time']=Time


        def getcharac(self):
            return self.attributes


class BaseVars():
    """
    Read and manage the netcdf file
    
    InPath: Path of the netcdf file
    model: Type of the model use: Arps or GFS
    """
    def __init__(self, InPath, model):
        f = netcdf.netcdf_file(InPath, 'r')# works with mmap= False but very slow
        self.__dict__ = f.__dict__.copy() # copy the attributs of the object
        self.__dict__['data'] = f.variables
        del(self.variables)
        self.module = { }
        self.varname = { }
        self.attributes = { }
        self.__properties(InPath, model)
         
        self.__load(f)
        f.close() # MARCELO < - Should I close here ??
 
        self.__applymap(model)

    def __properties(self,InPath,model):
        properties = FileProperties(InPath,model)
        charac=properties.getcharac()
        for i in charac:
            self.__setatt('attributes',i,charac[i])
    
    def __applymap(self, model):
        """
        NOTE:
            Maping for GFS has been done for the variable on the level 'Lv_ISBL0' 
            e .g  "TMP_P0_L100_GLL0 :: Temperature" 
            which is concordante with the ARPS domain
        """
        mapping = {
           'GFS': {
                   'TMP_P0_L100_GLL0': 'Tk',
                   'lat_0': 'Lat',
                   'lon_0':'Lon',
                   'UGRD_P0_L100_GLL0':'U',
                   'VGRD_P0_L100_GLL0':'V',
                   'VVEL_P0_L100_GLL0':'W',
                   'RH_P0_L100_GLL0':'Rh',
                   'HGT_P0_L100_GLL0':'ZP',
                   'CLWMR_P0_L100_GLL0':'QC'},
            'GFS_for':{
                       'latitude':'Lat',
                       'longitude':'Lon',
                       'TMP_2maboveground':'Tk',
                       'VGRD_10maboveground':'V',
                       'UGRD_10maboveground':'U',
                       'SPFH_2maboveground':'QV',
                       'TCDC_entireatmosphere_consideredasasinglelayer_':'TCC',
                       'TCDC_entireatmosphere':'TCDC_entireatmosphere_consideredasasinglelayer_',
                       
                       }
            
        }

        if model not in mapping: return

#         todelete = []
        items = self.varname.keys()

        for v in items:
            if v in mapping[model]:
                realv = mapping[model][v]
                if realv in self.varname:
                    raise Exception("Cannot overmap from %s to %s !" % (v, realv))
#                 print "DO MAPPINT %s -> %s" % (v, realv)
                self.varname[realv] = self.varname[v]
                self.module[realv] = self.module[v]
#                 todelete.append(v)

#         for d in todelete:
#             del self.varname[d]
#             del self.module[d]
#
        return

    def __load(self,f):
        for var in self.data.iterkeys():
            ##
            ## Criando funcoes dinamicas (lambda) para encapsular o __get() para cada
            ## variavel do arquivo NETcdf passada
            ##
            #self.__setatt('module',  var, lambda x: self.__get(x,var))
            self.__setatt('module',  var, functools.partial(self.__get, variable = var)) 
            self.__setatt('varname', var, self.data[var].long_name)

        for att in f._attributes:
            self.__setatt('attributes', att, f._attributes[att])

    def __setatt(self,kind,name,value):
        """
        set attributes
        
        kind: type of attribute: 'attributes','module','varname'
        name: name of the attribute
        value: value of the attribute
        """
        if kind == 'attributes':
            try:
#                 print(name)
#                 print(value)
                self.attributes[name]=value
            except:
                print('could not set the attribute: '+ str(name))
        if kind == 'module':
            try:
                self.module[name]=value
            except:
                print('could not set the module')
        if kind == 'varname':
            try:
                self.varname[name] = value
            except:
                print('could not set the varname')

    def __getatt(self,kind,guy):
        """
        get attributes
        
        kind: type of attribute: 'attributes','module','varname'
        name: name of the attribute
        value: value of the attribute
        """
        if kind =='attributes':
            try:
                return self.attributes[guy]
            except KeyError:
                print('This attribute does not exist')
        if kind =='module':
            try:
                return self.module[guy]
            except KeyError:
                print('This attribute does not exist')
        if kind == 'varname':
            try:
                return self.varname[guy]
            except KeyError:
                print('This attribute does not exist')

    def __get(self, arps, variable):
        return self.data[variable]


class arps():
    def __init__(self):
        self.__knowvariables = { }
        self.__cachedata = { }
        self.__attributes = { }
        self.__varname = { }

    def load(self, plugin):
        # module refeers to the variable or the function to calculate it
        for (k, v) in plugin.module.iteritems():
            if k in self.__knowvariables:
                print >>sys.stderr,"%s is already know." % k
            self.__knowvariables[k] = v
        # attributes are the characteristics of the file
        for (k,v) in plugin.attributes.iteritems():
            if k in self.__attributes:
                print >>sys.stderr,"%s is already know." % k
            self.__attributes[k] = v
            # varname is the longname of the variables in the file
        for (k,v) in plugin.varname.iteritems():
            if k in self.__varname:
                print >>sys.stderr,"%s is already know." % k
            self.__varname[k] = v

    def __findI(self,var,varlim):
        #Interpolation:nearest
        indice=min(range(len(var)), key=lambda i: abs(var[i]-varlim))
        return indice

    def __filter(self, data, **kwargs):
        """
        Constant interval grid
        
        IMPORTANT 
            I make a copy of the data (see data.copy) because of a problem of 
            netcdf.close() explication of the problem is here :
            http://stackoverflow.com/questions/5830397/python-mmap-error-too-many-open-files-whats-wrong
            
            I also increase maximum number of open file originally set to 1024 to 2048 through the command $ ulimit -n 2048
            
            Interesting comment about descriptor:
            http://stackoverflow.com/questions/26874195/python-multiprocessing-pool-too-many-files-open-logging-files
            
            Note that when netcdf_file is used to open a file with mmap=True (default for read-only), 
            arrays returned by it refer to data directly on the disk. The file should not be closed, 
            and cannot be cleanly closed when asked, if such arrays are alive. You may want to copy data arrays 
            obtained from mmapped Netcdf file if 
            they are to be processed after the file is closed, see the example below.
        """
        key="all"
        select = np.array(kwargs['kwargs']['select'])
        
        
        olddim = data.dimensions
        newdim = []
        
        userdim = select.shape[0]# subset dimensions
        lendim = len(olddim)
        
        if userdim != lendim: # check if the user gave the right number of parameters
            raise Exception ("Subset parameters %s do not agree with the data dimensions : %s !" % (userdim, lendim))

        # Double the parameter in case of same limit
        for i,v in enumerate(select):
            if len(v) ==1:
                select[i].append(v[0])
        
        
        Iselect = [ ]# Indice of the selection
        for d,s in zip(olddim,select):
            
            if diff(s) != 0:
                newdim.append(d)

            print("dimensions %s",d)
            print("user input %s",s)

            if s[0] == key: # could improve the efficiency
                s[0] = min(self.get(d).data) # MARCELO <- It the only way I found to solve a problem, what do you think about this

            if s[1] == key: # could improve the efficiency 
                s[1] = max(self.get(d).data)
            
            imin=self.__findI(self.get(d).data, s[0])
            imax= self.__findI(self.get(d).data, s[1])
            
            # Le fait que imin peut etre plus grand que imax peut poser probleme
            # Iselect= sorted([imin,imax])??
            if imin < imax:
                Iselect.append([imin,imax])
            elif imin == imax:
                Iselect.append([imin,imax+1])
            else:
                Iselect.append([imax,imin])

        # creation new object
        Newdata=data

        print(lendim)
        print(Iselect)
        if lendim == 1:
            Newdata.data=data.data[Iselect[0][0]:Iselect[0][1]]

        if lendim == 2:
            Newdata.data=data.data[Iselect[0][0]:Iselect[0][1],Iselect[1][0]:Iselect[1][1]]

        if lendim == 3:
            Newdata.data=data.data[Iselect[0][0]:Iselect[0][1],Iselect[1][0]:Iselect[1][1],Iselect[2][0]:Iselect[2][1]]

        if lendim ==4:
            Newdata.data=data.data[Iselect[0][0]:Iselect[0][1],Iselect[1][0]:Iselect[1][1],Iselect[2][0]:Iselect[2][1],Iselect[3][0]:Iselect[3][1]]

        Newdata.select = np.array(select)
        Newdata.Iselect = Iselect
        Newdata.dimensions=newdim

        return Newdata


    def get(self,variable,**kwargs):
        """
        1) Try if the variabile is already in the cache
        2) Try if the variable is in the BASEVAR
        """
        # Try if the variabile is already in the cache

        try:
            data = self.__cachedata[variable]
            return data
        except KeyError, e:
            # try if the variable is in the BASEVAR
            try:
                fn = self.__knowvariables[variable]
                data = fn(self)
                self.__cachedata[variable] = data
            except KeyError,e:
                print >>sys.stderr, "%s is not know,\n%s" % (variable, str(e))
                return None
        return self.__cachedata[variable] if len(kwargs) == 0 else self.__filter(self.__cachedata[variable], kwargs=kwargs)


    def remove(self,variable):
        try:
            del self.__knowvariables[variable]
            del self.__cachedata[variable]
        except KeyError,e:
            print('The variable is not known')

    def showvar(self):

        size=max(max(map(len,self.__varname.keys())), len("Variable"))
        fmt = "%%%ds :: %%s" % (size)
        print fmt % ("Variable", "Description")
        print "-" * size,"  ","-"*len("Description")
        for i in sort(self.__varname.keys()):
            print( fmt % (i, str(self.__varname[i])) )
    def showatt(self):
        for i in self.__attributes:
            print(i+':'+' '*5+str(self.__attributes[i]))
    def getatt(self,attribute):
        try:
            att=self.__attributes[attribute]
            return att
        except KeyError:
            print('This attribute is not know')
    def addatt(self,attribute,value):
        self.__attributes[attribute]=value


# TEST 



class netcdf_serie():
    def __init__(self,files,model):
        self.dataframe=pd.DataFrame([])
        self.__modelserie(files,model)
    def __modelserie(self,files,model):
        for InPath in files:
            properties = FileProperties(InPath,model)
            charac = properties.getcharac()
            if len(self.dataframe) == 0: 
                self.dataframe = pd.DataFrame([charac.values()],columns=charac.keys(),index=[charac['time']])
            else:
                newdataframe = pd.DataFrame([charac.values()],columns=charac.keys(),index=[charac['time']])
                newdataframe=newdataframe
                self.dataframe=self.dataframe.append(newdataframe)
    def get(self,var,**kwargs):
        select=np.array(kwargs['select'])
        data=np.array([])
        dataframe= self.dataframe
        for index,row in dataframe.iterrows(): # COULD USE AN APPLY FUNCTION
            try:
                ARPS = arps()
                BASE = BaseVars(row['InPath'], row['model'])
                ARPS.load(BASE)
                print(index)
                data=np.append(data,ARPS.get(var,select=select).data.flatten())
            except AttributeError:
                print("data dosent exist on file -> ", index)
        dataframe[var]=pd.Series(data, index = dataframe.index)
        return dataframe





class ArpsFigures():
    def __init__(self,arps):
        self.arps=arps# Es ce que ca duplique les donnés de arps ?????????????  
        self.para= { }
        self.paradef= {
            'OutPath':'/home/thomas/',
            'screen_width':1920,
            'screen_height':1080,
            'DPI':96,
            'Latmin':self.arps.get('Lat').data.min(),
            'Latmax':self.arps.get('Lat').data.max(),
            'Lonmin':self.arps.get('Lon').data.min(),
            'Lonmax':self.arps.get('Lon').data.max(),
            'Altmin':self.arps.get('z_stag').data[0],
            'Altmax':self.arps.get('z_stag').data[-1]
            }
        self.__figwidth()
        self.__subtitle(arps)
    def __figwidth(self):
        width=self.getpara('screen_width')
        height=self.getpara('screen_height')
        DPI=self.getpara('DPI')
        wfig=width/DPI #size in inches 
        hfig=height/DPI
        self.setpara('wfig',wfig)
        self.setpara('hfig',hfig)
    def __subtitle(self,arps):
        """
        Write the subtitle of the plot
        """
        sub=self.arps.getatt('time')
        self.setpara('subtitle', sub)

    def setpara(self,parameter,value):
        self.para[parameter]=value
        print(str(parameter)+' has been set to -> '+ str(value))
    def getpara(self,parameter):
        try:
            return self.para[parameter]
        except KeyError:
            print(parameter + ' has been not set -> Default value used ['+str(self.paradef[parameter])+']')
            try:
                return self.paradef[parameter]
            except KeyError:
                print(parameter+ ' dont exist')
    def delpara(self,varname):
        try:
            del self.para[varname]
            print('Deleted parameter-> ',varname)
        except KeyError:
            print('This parameter dont exist')
    def __setparadef(self,parameter,value):
        self.paradef[parameter]=value
        print(str(parameter)+' has been set by [default] to -> '+ str(value))
    def __getparadef(self,parameter):
        try:
            return self.paradef[parameter]
        except KeyError:
                print(parameter+ ' by [default] dont exist')
    def __levels(self,varname):
        self.paradef['nlevel']=10# number of discrete variabel level
        self.paradef['varmax']=int(self.arps.get(varname).data.max())
        self.paradef['varmin']=int(self.arps.get(varname).data.min())
        varmax=self.getpara('varmax')
        varmin=self.getpara('varmin')
        nlevel=self.getpara('nlevel')
        levels=np.linspace(varmin,varmax,nlevel)
        return levels
    def getvar(self,varname):
        """
        This module select data on the needed domain
        """
        #=======================================================================
        # get data and parameters
        #=======================================================================
        self.__getIpos() # find the indice of domain to select
        ILatmin=self.getpara('ILatmin')
        ILatmax=self.getpara('ILatmax')
        ILonmin=self.getpara('ILonmin')
        ILonmax=self.getpara('ILonmax')
        IAltmin=self.getpara('IAltmin')
        IAltmax=self.getpara('IAltmax')
        data=self.arps.get(varname).data
        selected='4d variable selected'
        
        if ILatmin == ILatmax:
            ILatmax=ILatmin+1
        if ILonmin == ILonmax:
            ILonmax=ILonmin+1
        if IAltmin == IAltmax:
            IAltmax=IAltmin+1
        try:
            Ndata=data[0,IAltmin:IAltmax, ILatmin:ILatmax, ILonmin:ILonmax]
            Ndata=np.squeeze(Ndata)
            self.__setparadef('varmax',Ndata.max())
            self.__setparadef('varmin',Ndata.min())
            return Ndata
        except:
            selected="3d variable selected"
            try:
                Ndata=data[IAltmin:IAltmax, ILatmin:ILatmax,ILonmin:ILonmax]
                Ndata=np.squeeze(Ndata)
                self.__setparadef('varmax',Ndata.max())
                self.__setparadef('varmin',Ndata.min())
                return Ndata
            except:
                selected='2d variable selected'
                try:
                    Ndata=data[ILatmin:ILatmax,ILonmin:ILonmax]
                    Ndata=np.squeeze(Ndata)
                    self.__setparadef('varmax',Ndata.max())
                    self.__setparadef('varmin',Ndata.min())
                    return Ndata
                except:
                    selected='1d variables selected'
                    try:
                        if varname == 'Lat':
                            Ndata=data[ILatmin:ILatmax]
                            self.__setparadef('varmax',Ndata.max())
                            self.__setparadef('varmin',Ndata.min())
                            return Ndata
                            print('Lat variable selected')
                        if varname == 'Lon':
                            Ndata=data[ILonmin:ILonmax]
                            self.__setparadef('varmax',Ndata.max())
                            self.__setparadef('varmin',Ndata.min())
                            return Ndata
                            print('Lon variable selected')
                    except:
                        print('Ask your mom she know how to fix the problem!')
            print(selected+" -> "+ varname)
    def __getIpos(self):
        """
        Select and return the position Lat/Lon of the specfied domain
        """
        #=======================================================================
        # Get data and parameters
        #=======================================================================
        Lonmin=self.getpara('Lonmin')
        Lonmax=self.getpara('Lonmax')
        Latmin=self.getpara('Latmin')
        Latmax=self.getpara('Latmax')
        Altmin=self.getpara('Altmin')
        Altmax=self.getpara('Altmax')
        Lat=self.arps.get('Lat').data
        Lon=self.arps.get('Lon').data
        Alt=self.arps.get('z_stag').data[:]
        #=======================================================================
        # Find indices to select the needed domain
        #=======================================================================
        try:
            Altcross=self.getpara('Altcross')
            ILatmin=self.__findI(Lat, Latmin)
            ILatmax=self.__findI(Lat, Latmax)
            ILonmin=self.__findI(Lon, Lonmin)
            ILonmax=self.__findI(Lon, Lonmax)
            IAltmin=self.__findI(Alt, Altcross)
            IAltmax=self.__findI(Alt, Altcross)
            print('==================================')
            print('Horizontal cross section selected')
            print('==================================')
        except KeyError:
            print('To make an horizontal cross section set Altcross')
        try:
            Loncross=self.getpara('Loncross')
            ILatmin=self.__findI(Lat, Latmin)
            ILatmax=self.__findI(Lat, Latmax)
            ILonmin=self.__findI(Lon, Loncross)
            ILonmax=self.__findI(Lon, Loncross)
            IAltmin=self.__findI(Alt, Altmin)
            IAltmax=self.__findI(Alt, Altmax)
            print('==================================')
            print('North South vertical cross section selected')
            print('==================================')
        except KeyError:
            print('To make an North South cross section set Loncross')
        try:
            Latcross=self.getpara('Latcross')
            ILatmin=self.__findI(Lat, Latcross)
            ILatmax=self.__findI(Lat, Latcross)
            ILonmin=self.__findI(Lon, Lonmin)
            ILonmax=self.__findI(Lon, Lonmax)
            IAltmin=self.__findI(Alt, Altmin)
            IAltmax=self.__findI(Alt, Altmax)
            print('==================================')
            print('East West vertical cross section selected')
            print('==================================')
        except KeyError:
            print('To make an East West cross section set Latcross')
        #=======================================================================
        # set Indice in the dictionnary "para"
        #=======================================================================
        try:
            self.setpara('ILatmin',ILatmin)
            self.setpara('ILatmax',ILatmax)
            self.setpara('ILonmin',ILonmin)
            self.setpara('ILonmax',ILonmax)
            self.setpara('IAltmin',IAltmin)
            self.setpara('IAltmax',IAltmax)
        except UnboundLocalError:
            print('Please set Altcross, or Loncross or Latcross ')
    def __findI(self,var,varlim):
        indice=min(range(len(var)), key=lambda i: abs(var[i]-varlim))
        return indice
    def __contour(self,varname):
        var=self.getvar(varname)
        lon=self.getvar('Longrid')
        lat=self.getvar('Latgrid')
        alt=self.getvar('ZP')
        try:
            self.para['Altcross']
            X=lon
            Y=lat
            select="Horizontal cross section is being plotted"
        except KeyError:
            try:
                self.para['Latcross']
                X=lon
                Y=alt
                select="Vertical East West cross section is being plotted"
            except KeyError:
                try:
                    self.para['Loncross']
                    X=lat
                    Y=alt
                    select="Vertical North South cross section is being plotted"
                except:
                    print('Their is a problem on the ploting module - ask your mom')
        print(select)
        print(X.shape)
        print(Y.shape)
        print(var.shape)
        levels=self.__levels(varname)
        return [X,Y,var,levels]
    def contourf(self,varname):
        [X,Y,var,levels]=self.__contour(varname)
        plot=plt.contourf(X,Y,var,cmap=get_cmap('BuRd'),levels=levels)
        return plot
    def contour(self,varname):
        [X,Y,var,levels]=self.__contour(varname)
#         plot=plt.contourf(X,Y,var,cmap=get_cmap('BuRd'),levels=levels)
        plot=plt.contour(X,Y,var,levels=levels,cmap=get_cmap('gist_gray'))
        return plot
    def windvector(self):
        """
        x: vector position horizontal length (n)
        y: vector position vertical length (m)
        U: matrix zonal wind shape (m*n)
        V: matrix meridional wind shape (m*n)
        """
        self.__setparadef('Nbarb',10)
        self.__setparadef('Lbarb',5)
        Nbarb=self.getpara('Nbarb')
        Lbarb=self.getpara('Lbarb')
        U=self.getvar('U')
        V=self.getvar('V')
        W=self.getvar('W')
        lon=self.getvar('Longrid')
        lat=self.getvar('Latgrid')
        alt=self.getvar('ZP')
        try:
            self.para['Altcross']
            X=lon
            Y=lat
            select="Horizontal cross section is being plotted"
        except KeyError:
            try:
                self.para['Latcross']
                X=lon
                Y=alt
                V=W
                select="Vertical East West cross section is being plotted"
            except KeyError:
                try:
                    self.para['Loncross']
                    X=lat
                    Y=alt
                    U=V
                    V=W
                    select="Vertical North South cross section is being plotted"
                except:
                    print('Their is a problem on the ploting module - ask your mom')
        print("U shape"+str(U.shape))
        print("V shape"+str(V.shape))
        print("Y shape"+str(Y.shape))
        print("X shape"+str(X.shape))
        if X.shape != U.shape and Y.shape != V.shape:
            print('x * y does not equal to U or V')
        Up=U[::Nbarb,::Nbarb]
        Vp=V[::Nbarb,::Nbarb]
        Xp=X[::Nbarb,::Nbarb]
        Yp=Y[::Nbarb,::Nbarb]
        #plot=plt.barbs(Xp,Yp,Up,Vp,length=Lbarb, barbcolor=['k'],pivot='middle',sizes=dict(emptybarb=0))
        plot=plt.quiver(Xp,Yp,Up,Vp)
        return plot

    #     ###################################
    #     # Position of the Stations
    #     ###################################
    #     StaPosFile="/home/thomas/PhD/obs-lcb/staClim/LatLonSta.csv"
    #     StaPos={}
    #     with open (StaPosFile) as StaPosF:
    #         reader_IAC=csv.reader(StaPosF,delimiter=",")
    #         header_IAC=reader_IAC.next()
    #         for h in header_IAC:
    #             StaPos[h]=[]
    #         for row in reader_IAC:
    #             for h,v in zip(header_IAC,row):
    #                 StaPos[h].append(v)
    # 
    #     Lat=np.array(Lat)
    #     Lon=np.array(Lon)
    #     LatStaI=[]
    #     LonStaI=[]
    #     LatSta=[]
    #     LonSta=[]
    #     StaName=[]
    #     for ista,sta in enumerate(StaPos['Posto']):
    #         print('open station=> '+sta)
    #         LatI=np.searchsorted(Lat,float(StaPos['Lat '][ista]), side="left")
    #         LonI=np.searchsorted(Lon,float(StaPos['Lon'][ista]), side="left")
    #         if LatI!=0 and LonI!=0:
    #             LatSta=LatSta+[float(StaPos['Lat '][ista])]# Use in compareGFS_OBS.py
    #             LonSta=LonSta+[float(StaPos['Lon'][ista])]#Use in compareGFS_OBS.py
    #             LatStaI=LatStaI+[LatI]
    #             LonStaI=LonStaI+[LonI]
    #             StaName=StaName+[StaPos['Posto'][ista]]
    #             print("In map => "+ StaPos['Posto'][ista] +" at "+ str(LatI) +" and " +str(LonI))
    pass


class ArpsFigures2():
    def __init__(self, arps):
        self.arps = arps

    @staticmethod
    def getpara(p, var):
        return p[var]

    @staticmethod
    def getparamset():
        paradef = {
            'OutPath':'/home/thomas/',
            'screen_width':1920,
            'screen_height':1080,
            'DPI':96,
            'Latmin': -90,
            'Latmax': 90,
            'Lonmin': -180,
            'Lonmax': 180,
            'Altmin': 0,
            'Altmax': 8000
        }
        return paradef

    def fitcoordinate(self, p, var):
        p['Latmin'] = self.arps.get(var).data.min()
        p['Latmax'] = self.arps.get(var).data.max()
        p['Lonmin'] = self.arps.get('Lon').data.min()
        p['Lonmax'] = self.arps.get('Lon').data.max()
        return p

    def contourf(self, param, variables, prefix = None):
        for var in variables:
            filename = "%s%s.png" % (prefix + "_" if prefix else "", var)
            filename = os.path.join(ArpsFigures2.getpara(param, 'output'), filename)
            print filename

        pass


