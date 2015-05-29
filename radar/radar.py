#	DESCRIPTION
#		Read Radar Data and plot reflectivity
#=====================================================
#======================
import numpy as np
import struct
from math import *
import numpy as np
from matplotlib.pyplot import *
from __future__ import division

#====== user input
InputPath="/home/thomas/PhD/obs-lcb/radar/CSCAN-2013-2014/"
Fname="cscan_201402142351.dat"

file_in =InputPath+Fname
fd = open(file_in,'rb')
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
zeniths=np.array([])
zeniths=np.append(zeniths,np.arange(0,60,0.5))
zeniths=np.append(zeniths,np.arange(60,120,1))
zeniths=np.append(zeniths,np.arange(120,240,2))

	        
azimuths=range(0,360)

plot_polar_contour(values, azimuths, zeniths,)
plt.show()


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


































