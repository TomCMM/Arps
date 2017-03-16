#	DESCRIPTION
#		Read Radar Data and plot reflectivity
#=====================================================
from __future__ import division
import numpy as np
import struct
from math import *
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib.pyplot import *
import geopy 
from geopy.distance import VincentyDistance


def polar2cart(r, theta):
	x = r * np.cos(theta)
	y = r * np.sin(theta)
	return x, y


def radar_values(radar_file_path):
	"""
	RETURN THE VALUES OF THE RADAR
	"""
	fd = open(radar_file_path,'rb')
	position =100 # puch the header
	no_of_doubles = 300000000
	
	#numpy_data = np.fromfile(fd,dtype = np.dtype('float32'), count = no_of_doubles)
	# move to position in file
	fd.seek(position,0)
	
	# straight to numpy data (no buffering) 
	#numpy_data = np.fromfile(fd, dtype = np.dtype('uint8'), count = no_of_doubles)
	numpy_data = np.fromfile(fd, dtype = np.dtype('uint8'), count = no_of_doubles)
	start=(240*360)*5
	end=(240*360)*6
	
	dada=17+numpy_data[range(start,end)]*0.22 
	dada=np.array(map(float,dada))
	Rdata=dada.reshape(360,240)
	
	values=Rdata
	return values


def position_radar_observation():
	"""
	RETURN
		A tuple with the latitude, longitude, height of the radar observation
	"""
	Elev_angle=2.9
	# Earth radius (m)
	R=6371.0072*10**3
	# Altitude Radar
	H_rad=925
	#Latitude position 
	Lat_ctr=-23.60
	#Longitude position of the radar
	Lon_ctr=-45.9722
	
	# Equivalent earth radius
	#Authalic radius of the earth ("equal area -hypothetical perfect sphere")
	Re=R*(4/3)
	
	#------ Radar range 
	zeniths=np.array([])
	zeniths=np.append(zeniths,np.arange(0.5,60,0.5))
	zeniths=np.append(zeniths,np.arange(60,120,1))
	zeniths=np.append(zeniths,np.arange(120,242,2))*1000
	
	azimuths=range(0,360)
	
	#% Equation Doviak and Zrnic (2.28b and 2.28c)
	H_pos=(np.sqrt(zeniths**2+(H_rad+Re)**2+2*zeniths*(Re+H_rad)*sin((np.pi/180)*Elev_angle))-Re)
				
	#%length (m)
	Dist_pos=(np.arctan(zeniths*np.cos(Elev_angle*(np.pi/180))/ (zeniths*np.sin(Elev_angle*(np.pi/180))+Re+H_rad))*Re)
	
	
	#============= Transform Polar to cartesian
	Lat_rad=np.array([])
	Lon_rad=np.array([])
	origin = geopy.Point(Lat_ctr, Lon_ctr)
	for i in azimuths:
		for j in Dist_pos:	
			y,x=polar2cart(j,i*(np.pi/180))# convert into meters distance X and Y 
			if x>=0:
				Lon_rad = np.append(Lon_rad,VincentyDistance(kilometers=np.abs(x)/1000).destination(origin,90).longitude)
			else:
				Lon_rad = np.append(Lon_rad,VincentyDistance(kilometers=np.abs(x)/1000).destination(origin,270).longitude)
			if y>=0:
				Lat_rad = np.append(Lat_rad,VincentyDistance(kilometers=np.abs(y)/1000).destination(origin, 0).latitude)
			else:
				Lat_rad = np.append(Lat_rad,VincentyDistance(kilometers=np.abs(y)/1000).destination(origin, 180).latitude)
	
	
	H_rad=np.tile(H_pos,(360,1)).flatten()
		
	return H_rad, Lon_rad, Lat_rad


def plot_polar_contour(values, azimuths, zeniths):
	theta = np.radians(azimuths)
	zeniths = np.array(zeniths)
	values = np.array(values)
	values = values.reshape(len(azimuths), len(zeniths))
	r, theta = np.meshgrid(zeniths,theta)
	fig, ax = subplots(subplot_kw=dict(projection='polar'))
	ax.set_theta_zero_location("N")
	ax.set_theta_direction(-1)
	jet()
	contour_levels = np.arange(1, 100, 1)
	cax = ax.contourf(theta, r, values,contour_levels)
	cb = fig.colorbar(cax)
	cb.set_label("Pixel reflectance")
	return fig, ax, cax


if "__name__" == "__main__":
	#====== user input
	InputPath="/home/thomas/phd/obs/radar/CSCAN-2013-2014/"
	Fname="cscan_201402142351.dat"
	
	values = radar_values(InputPath+Fname)
	zeniths=np.array([])
	zeniths=np.append(zeniths,np.arange(0,60,0.5))
	zeniths=np.append(zeniths,np.arange(60,120,1))
	zeniths=np.append(zeniths,np.arange(120,240,2))
	
	azimuths=range(0,360)
	
	plot_polar_contour(values, azimuths, zeniths,)
	plt.show()
	
	



































