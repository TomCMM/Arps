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
        
        #=======================================================================
        # Transform TO temperature
        #=======================================================================
#         storeP = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/P_store.h5')
#         storePT = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/PT_store.h5')
        storeTk = pd.HDFStore('/home/thomas/phd/statmod/data/model_data/Tk_store.h5')
#         
#         for i,(Pkey, PTkey) in enumerate(zip(storeP.keys(), storePT.keys())):
#             print Pkey
#             storeTk['df_tk'+str(i)] = Tk(storeP[Pkey], storePT[PTkey])
        print storeTk 
        
        #=======================================================================
        # Incremental PCA with chunck of data
        #=======================================================================

        n_components = 10
        ipca = IncrementalPCA(n_components=n_components)
        for key in storeTk.keys():
            print key
            print storeTk[key].shape
            ipca.partial_fit(storeTk[key].T)
        print ('Number of Samples Seen:',ipca.n_samples_seen_ )
        print ('Explained variance by %d PCs:' %n_components, np.sum(ipca.explained_variance_ratio_))

        #=======================================================================
        # Plot loading
        #=======================================================================

        loading = ipca.components_.T[:,3].reshape((1201, 1201))
        plt.contourf(loading, levels=np.linspace(loading.min(), loading.max(),50))
        plt.colorbar()
        plt.show()
 

        