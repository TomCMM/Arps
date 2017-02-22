#===============================================================================
# DESCRIPTION
#    Read multiple sounding file from Wyoming university 
#    Write sounding in ARPS format
#===============================================================================

import pandas as pd
import glob
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime



if __name__ =='__main__':
    inpath ="/home/thomas/PhD/obs-lcb/soundings/campo_marte/"
    files = glob.glob(inpath+"*")
    files.sort()
    columns = ['PRES', "HGHT", "TEMP", 'DWPT', 'RELH', 'MIXR', 'DRCT', 'SKNT', 'THTA','THTE', 'THTV']
#     files = files[1:2]
    height = np.arange(250,18250,500)
    height = np.insert(height,0,0)
    print height
    newdf = pd.DataFrame(index=height, columns = columns)
    soundings = {}
    filenames = []
    cold_pool = pd.read_csv('/home/thomas/cold_poolevents.csv', index_col=0, header=None,parse_dates=True)
#     cold_pool_index = cold_pool.index.strftime('%Y%m%d')
    print cold_pool.index
        
        
    for i,file in enumerate(files):
    
        try:
            data = pd.read_csv(file, skiprows=7, header=None, delim_whitespace=True, error_bad_lines=False)
            data =data.convert_objects(convert_numeric=True)
    
            data = data.dropna()
            data.columns = columns
                   
            data.index = data['HGHT']
    
            newdata = pd.concat([data, newdf],axis=0, join='outer')
            newdata = newdata.sort_index()
            newdata = newdata.groupby(level=0)
            newdata = newdata.last()
    
            newdata = newdata.interpolate()
            newdata = newdata[newdata.index.isin(height)]
                  
            filename = os.path.basename(file)[-15:-5]
            date = datetime.strptime(filename, '%Y%m%d%H')
            date = date - pd.Timedelta(hours=3)
            print date
    
            soundings[date] = newdata
        except ValueError:
            pass
          
    
     
    soundings = pd.Panel(soundings)
    print soundings
    print soundings.items
    soundings = soundings[soundings.items.isin(cold_pool.index)]
    print soundings.items
    mean_sounding = soundings.mean(0)
    print mean_sounding
    plt.show()