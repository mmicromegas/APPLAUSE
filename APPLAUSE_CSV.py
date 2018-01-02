from astropy.io import fits
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy
from scipy import ndimage

class applause:

    def __init__(self,datacsv):
		# read CSV
		
        self.platecsv = pd.read_csv('DATA/'+datacsv)
		
        self.raj2000   = self.platecsv.raj2000
        self.dej2000   = self.platecsv.dej2000
		
    def extract(self,key):
        return self.platecsv[key]

    def extract_scan_data(self,key):
        return self.platecsv.loc[self.platecsv['scan_id'] == key]		
		
    def get_bndry(self,param):
        # put values in series
        bndry = {'minra':np.min(self.raj2000),'maxra':np.max(self.raj2000), 'minde': np.min(self.dej2000), 'maxde': np.max(self.dej2000)}
        return bndry[param]		
		
    def return_plateid(self):	
        return self.plate_id[0]
		
    def return_scanid(self):	
        return self.scan_id[0]
		
    def return_utmid(self):	
        return self.ut_mid[0]
		
    def calc_ra(self,ra):
        ra = ra/15.
        hours = int(ra)
        minutes = (ra-hours)*60. 
        seconds = (minutes-int(minutes))*60.
        return hours,int(minutes),int(seconds)	
	
    def calc_dec(self,dec):
        degrees = int(dec)
        minutes = (dec-degrees)*60. 
        seconds = (minutes-int(minutes))*60.
        return degrees,int(minutes),int(seconds)
