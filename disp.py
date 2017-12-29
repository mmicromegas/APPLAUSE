import APPLAUSE as appl
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

# ----------- #
# INITIALIZE
# ----------- #

applause_input_csv   = 'DATA/master_ra_0_360_dec_m10_p10.csv'
#horizons_results_csv = 'testresults.txt'
dss_plate_fits       = ' '
mode = 2
horizons_results_csv = 'master_ra_0_360_dec_m10_p10.csv_results.txt'

# if mode = 0, RA is vertical   increasing from T2B, DEC is horizontal increasing from R2L 	
# if mode = 1, RA is horizonal  increasing from R2L, DEC is vertical increasing from B2T
# if mode = 2, RA is horizontal increasing from L2R, DEC is vertical increasing from B2T
# R2L is right to left, T2B is top to bottom

# ----------- #
#  LOAD INPUT
# ----------- #

applause_input   = pd.read_csv(applause_input_csv)
columns = ['obs','scan_id','obj_number','obj_designation','obj_ra','obj_dec','obj_ra_hrsmmss','obj_dec_dgrmmss','obj_mag']	
horizons_results = pd.read_csv(horizons_results_csv,sep=' ',names=columns)
		
for i in horizons_results.scan_id:		
    # get and read DSS fits
    dss_fits = 'DATA/DSS/dss.1.35.5+16.1.4.fits'
	
    idx_r = np.where(horizons_results.scan_id == i)
    object = horizons_results.obj_designation.as_matrix()[idx_r]		
    objra = horizons_results.obj_ra.as_matrix()[idx_r]	
    objde = horizons_results.obj_dec.as_matrix()[idx_r]	
    objmag = horizons_results.obj_mag.as_matrix()[idx_r]	

    szobj = np.size(idx_r)

    # field of view for zoom
    fov = 1./3. # in degrees
	
    for obj in range(szobj):
        object_s = object[obj]
        objra_s  = objra[obj]
        objde_s  = objde[obj]
        objmag_s = objmag[obj]
	
        # initialize plate object by attributes
        plate_1 = appl.applause(i,applause_input,object_s,objra_s,objde_s,objmag_s,dss_fits,mode)

        figsize = plate_1.get_shape()
        xsz = figsize[1]
        ysz = figsize[0]
        xsize = 7.
        ysize = int(ysz*xsize/xsz)

        # initialize figure
        fig_1 = plt.figure(1,figsize=(xsize,ysize))	
	
        plate_1.display_plate('gray','auto','lower',0.0,0.0)
        plate_1.display_stars()
        plate_1.display_object() 
#        plate_1.enable_clicks(fig_1)
        plate_1.save_plate()
#        plate_1.show_header('DATE-AVG')
	
        # initialize figure	
        fig_2 = plt.figure(2,figsize=(6,6))	

        plate_1.display_plate_zoom(fov,'gray','auto','lower',1.,1)
        plate_1.display_stars_zoom(fov)
        plate_1.display_object() 
#        plate_1.enable_clicks(fig_2)
        plate_1.save_plate_zoom()

	
        # initialize figure
#        fig_3 = plt.figure(3,figsize=(6,6))	

#        plate_1.display_observation(fov,'gray_r','auto','lower',1)
#        plate_1.display_object() 
#        plate_1.save_obs_zoom()

        plt.close('all')

#plt.show()


