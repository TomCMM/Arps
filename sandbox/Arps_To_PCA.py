#===============================================================================
#    DECRIPTION
#        TRANSFORM THE A SIMULATION INTO A DATAFRAME FOR A MODE-t pca ANALYSIS
#===============================================================================
import glob
from netcdf_lib import *
import pandas as pd
from statmod_lib import *
import time
import pickle




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


#===============================================================================
# Write netcdf into dataframe
#===============================================================================
if __name__=='__main__':
#     InPath='/dados1/sim/sim_coldpool/100m_all/v2/'
#     Files=glob.glob(InPath+"*")
#     Files.sort()
#     Files = Files[4:]
#     model='ARPS'
#                
#     zlim = 1 # grid points in the vertical
#              
#     for i, file in enumerate(Files):
#          
#         f = Dataset(file, 'r')
#     
#         pt = f.variables['PT'][0,0,100:-100,100:-100]
#         p = f.variables['P'][0,0,100:-100,100:-100]
#         tk = Tk(p, pt)
#         tk=tk.flatten()
#         print tk.shape
#         pd.DataFrame(tk).to_csv('/home/thomas/pca_surface/'+str(i)+'.csv')
# 
#     InPath = '/home/thomas/pca_surface/'
#     Files=glob.glob(InPath+"*")
#     Files.sort()
#            
#             
#     df = pd.DataFrame()
#     for i,file in enumerate(Files):
#         print i
#         df = pd.concat([df,pd.read_csv(file, index_col=0)], join='outer', axis=1)
#     df.to_csv('/home/thomas/pca_surface/df_pca_arps.csv')

    

#===============================================================================
# PCA
#===============================================================================

 
  
#   
# #     df = pickle.load( open( "/home/thomas/pca/df_pca_arps.p", "rb" ) )
#     df = pd.read_csv('/home/thomas/pca_surface/df_pca_arps.csv', index_col=0)
#     df.columns= range(len(df.columns))
#     df = df-273.15
# 
#  
# #       
# #     rngs = np.linspace(10000,1000000,5)
# #     comp_times=[]
# #     for rng in rngs:
# #     start_time = time.time()
#     stamod = StaMod(df, None)
#     stamod.pca_transform(nb_PC=4, standard=False, center=False, sklearn=True)
#     
#     
# #     print("--- %s seconds ---" % (time.time() - start_time))
# #     stamod.plot_scores_ts()
# #     plt.show()
# #     stamod.plot_exp_var()
# #     plt.show()
#     print stamod.eigenvectors
#     print stamod.eigenvectors.shape
#     loadings = stamod.eigenvectors
#     
#     
#     
#     plt.subplot(221)
#     plt.plot(loadings.T)
# #     print loadings
# #     loadings.plot()
#         
#     PCs = stamod.scores
#     print PCs.shape
#     print PCs
#        
#     
#     plt.subplot(222)
#     PC1 = PCs.loc[:,1].reshape((1002, 1002))
#     plt.contourf(PC1, levels=np.linspace(PC1.min(), PC1.max(),50))
#     plt.colorbar()
#     
#     plt.subplot(223)
#     PC2 = PCs.loc[:,2].reshape((1002, 1002))
#     plt.contourf(PC2, levels=np.linspace(PC2.min(), PC2.max(),50))
#     plt.colorbar()
#     
#     plt.subplot(224)
#     PC3 = PCs.loc[:,3].reshape((1002, 1002))
#     plt.contourf(PC3, levels=np.linspace(PC3.min(), PC3.max(),50))
#     plt.colorbar()
#     plt.show()
#           
#     PC4 = PCs.loc[:,4].reshape((1002, 1002))
#     plt.contourf(PC4, levels=np.linspace(PC4.min(), PC4.max(),50))
#     plt.colorbar()
#     plt.show()

# #  
#      
    
    
#         comp_times.append(time.time() - start_time)
#     plt.plot(rngs,comp_times)
     
#     stamod.plot_exp_var()
#     plt.show()
#     stamod.plot_scores_ts()
    
    
    
    
    
    