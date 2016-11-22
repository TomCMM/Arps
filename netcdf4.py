from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import glob 

def Tk(P, PT):
    """
    Calculate the Real Temperature in Kelvin
    """
    print("Calculate the Real temperature in Kelvin")
    P0 = 100000
    Rd = 287.06
    Cp = 1004.5
    Tk = PT*(P/P0)**(Rd/Cp)
    return Tk


if __name__=='__main__':
    InPath="/dados1/sim/sim_coldpool/100m/"
    InPath="/dados1/sim/sim_coldpool/100m_all/v2/"
    
    
    Files=glob.glob(InPath+"*")
    Files.sort()
#     Files = [Files[5]]
#     Files= ['/dados1/sim/sim_coldpool/100m_all/r300m.net000000']
      
    print Files
    for Path in Files:
        print(Path)
        f = Dataset(Path, 'r')
   
        pt = f.variables['PT'][0,0,:,:]
        p = f.variables['P'][0,0,:,:]
        tk = Tk(p, pt)
        print tk.max()
#         tk = f.variables['ZP'][0,:,:]
  
#         levels = np.linspace(290, 304, 50)
        levels = np.linspace(tk.min(), tk.max(), 50)

#         levels = np.linspace(700, 2200, 50)
        plt.contourf(tk, levels=levels, map='inferno')
        plt.colorbar()
        plt.show()
#     
#     
#     levels = np.linspace(-10, 0, 50)
#      
#     f = Dataset(Files[0], 'r')
#     pt = f.variables['PT'][0,0,:,:]
#     p = f.variables['P'][0,0,:,:]
#     tk1 = Tk(p, pt)
#  
#     f = Dataset(Files[4], 'r')
#     pt = f.variables['PT'][0,0,:,:]
#     p = f.variables['P'][0,0,:,:]
#     tk2 = Tk(p, pt)    
#      
#     diff = tk2 - tk1
#     plt.contourf(diff, levels=levels, map='inferno')
#     plt.colorbar()
#     plt.show()
#     