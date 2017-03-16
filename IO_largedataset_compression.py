#===============================================================================
# DESCRIPTION
#    CONVERT LARGE FILES FROM CSV INTO HDF
#    STORE THEM INTO A EFFICIENT HDF FILE
#    COMPRESS USING PCA
# TODO
#    Exploratory analysis of the simulated temperature
#    Verification goodness of the PCA
#    Found how to make the transformation and obtain the scores
#    Select the different loading at the station position 

#===============================================================================

import pandas as pd
import numpy as np
import math
from sklearn.decomposition import PCA, IncrementalPCA
import matplotlib.pyplot as plt
from clima_lib.LCBnet_lib import *
from statmod_lib.loadingindex.estimateloading import select_stations




def geo_idx(dd, dd_array):
    """
      search for nearest decimal degree in an array of decimal degrees and return the index.
      np.argmin returns the indices of minium value along an axis.
      so subtract dd from all values in dd_array, take absolute value and find index of minium.
     """

    geo_idx = (np.abs(dd_array - dd)).argmin()
    return geo_idx


def rdf(path):
    print "reading" + path
    dfPT = pd.read_csv(path)
    print "done"
    return dfPT

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


if __name__ =='__main__':
#         #=======================================================================
#         # Store the dataframe
#         #=======================================================================
#         inpath = "/home/thomas/phd/statmod/data/model_data/PT/"
# #         files = [
# #              "P_full","P_arps_1.csv","P_arps_2.csv","P_arps_3.csv","P_arps_4.csv","P_arps_1finaly.csv","P_arps_2finaly.csv",
# #             "P_arps_3finaly.csv","P_arps_1finaly.csv","P_arps_2finaly.csv","P_arps_3finaly.csv", "P_arps_somepartsindados3finaly.csv","P_arps_lastpart.csv"
# #              ]
# #         
#         files = [
#          "PT_arps_1.csv","PT_arps_2.csv","PT_arps_3.csv","PT_arps_4.csv","PT_arps_1finaly.csv","PT_arps_2finaly.csv",
#         "PT_arps_3finaly.csv","PT_arps_1finaly.csv","PT_arps_2finaly.csv","PT_arps_3finaly.csv", "PT_arps_somepartsindados3finaly.csv","PT_arps_lastpart.csv"
#          ]
#          
#         store = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/PT_store.h5')
#         for i, file in enumerate(files):
#             df = rdf(inpath+file)
#             store['df_PT_'+str(i)] =  df
#         print store
#         print store.close()
#         store1 = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/PT_store.h5')
#         print "Worked?"
#         print store1
#         store1.close()
        
#         #=======================================================================
#         # Transform TO temperature
#         #=======================================================================
# #         storeP = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/P_store.h5')
# #         storePT = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/PT_store.h5')
#         storeTk = pd.HDFStore('/home/tom/phd/model_data/Tk_store.h5')
    newstoreTk = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/newTk_store.h5')
#         newstoreTk = pd.HDFStore('/home/tom/phd/model_data/new_Tk_store.h5')
# # #         
# # #         for i,(Pkey, PTkey) in enumerate(zip(storeP.keys(), storePT.keys())):
# # #             print Pkey
# # #             storeTk['df_tk'+str(i)] = Tk(storeP[Pkey], storePT[PTkey])
# #         onepoint = pd.HDFStore('/home/tom/phd/model_data/onepoint.h5')
# # #         df = pd.Series()
#         for key in storeTk.keys():
#             print key
#             print storeTk[key].T.iloc[:,:].shape
#             newstoreTk[key] = storeTk[key].T[storeTk[key].T.min(axis=1) > 200].T

#             newstoretk = storeTk[key].T[]
#             
# #             print type(select.index)
# # #             print select.shape()
# #             select.plot()
#             plt.show()
# #             df = df.append(select)
# 
# #         onepoint['onepoint'] = df
# #         df.plot()
# #         plt.show()
# #             
#             
#         #=======================================================================
#         # Incremental PCA with chunck of data
#         #=======================================================================

#         n_components = 10
#         ipca = IncrementalPCA(n_components=n_components)
#         keys = newstoreTk.keys()
#         for key in keys:
#             print key
#             print newstoreTk[key].T.shape
# #             plt.show()
#             data = newstoreTk[key].T
#             data.index = pd.to_datetime(data.index)
#             data = data
#             try:
#                 ipca.partial_fit(data)
#             except ValueError:
#                 pass
#         print ('Number of Samples Seen:',ipca.n_samples_seen_ )
#         print ('Explained variance by %d PCs:' %n_components, np.sum(ipca.explained_variance_ratio_))
#    
#         pc_component = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/pc_component.h5')
#         pc_component["pc_component"] = pd.DataFrame(ipca.components_.T) 

#         #=======================================================================
#         # Plot loading
#         #=======================================================================

#         pc_component = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/pc_component.h5')
#         loading = pc_component['pc_component']
#         print loading
#         for pc in pc_component['pc_component'].columns: 
#             loading = pc_component['pc_component'].loc[:,pc].reshape((1201, 1201))
#             plt.contourf(loading, levels=np.linspace(loading.min(), loading.max(),50))
#             plt.colorbar()
#             plt.show()
# 
#         loading = ipca.components_.T[:,1].reshape((1201, 1201))
#         plt.contourf(loading, levels=np.linspace(loading.min(), loading.max(),50))
#         plt.colorbar()
#         plt.show()
#          
#         loading = ipca.components_.T[:,2].reshape((1201, 1201))
#         plt.contourf(loading, levels=np.linspace(loading.min(), loading.max(),50))
#         plt.colorbar()
#         plt.show()
 
#         loading = ipca.components_.T[:,3].reshape((1201, 1201))
#         plt.contourf(loading, levels=np.linspace(loading.min(), loading.max(),50))
#         plt.colorbar()
#         plt.show()

    #===============================================================================
    # Plot selected stations TEST
    #===============================================================================
#     import pickle
#     loading_true = pickle.load( open(  "/home/thomas/phd/statmod/data/loadingindex/loadings.p", "rb" ) ).T
#     print loading_true
#     coordinates = select_stations(loading_true.index)
#     keys = newstoreTk.keys()
#     dfs = []
#     for key in keys:
#         print key
#         data = newstoreTk[key]
#         data = data.iloc[coordinates['idx_selection'],:]
#         dfs.append(data)
#     df = pd.concat([df.T for df in dfs], axis=0)
#     df.columns = coordinates.index
#     df.to_csv("/home/thomas/phd/dynmod/res/coldpool/validation/T.csv")
#     print df

    #===========================================================================
    # Validation cold pool simulation
    #===========================================================================
    df = pd.read_csv("/home/thomas/phd/dynmod/res/coldpool/validation/T.csv")
    sta_ex = ['C04','C05', 'C06','C07','C08', 'C09','C10','C11', 'C12','C13','C14', 'C15','C16', 'C17','C18']
    sta_ex = ['C04','C05', 'C06','C07','C08', 'C09','C10']
    df.loc[:,sta_ex].plot()
    plt.show()
#     print df
    
         