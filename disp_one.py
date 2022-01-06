import APPLAUSE as appl
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
#import commands
import subprocess

# ----------- #
# INITIALIZE 
# ----------- #

applause_input_csv = 'DATA/master_ra_0_360_dec_m10_p10.csv'
horizons_results_csv = 'RESULTS/master_ra_0_360_dec_m10_p10.csv_results.txt'
mode = 2
# scan_id = 17017
# scan_id = 17220
# scan_id = 17176
# scan_id = 17351
# scan_id = 17999 # something wrong
# scan_id = 17971
# scan_id = 17997
scan_id = 18052

# if mode = 0, RA is vertical   increasing from T2B, DEC is horizontal increasing from R2L 	
# if mode = 1, RA is horizonal  increasing from R2L, DEC is vertical increasing from B2T
# if mode = 2, RA is horizontal increasing from L2R, DEC is vertical increasing from B2T
# R2L is right to left, T2B is top to bottom

# ----------- #
#  LOAD INPUT
# ----------- #

applause_input = pd.read_csv(applause_input_csv)
columns = ['obs', 'scan_id', 'obj_number', 'obj_designation', 'obj_ra', 'obj_dec', 'obj_ra_hrsmmss', 'obj_dec_dgrmmss',
           'obj_mag']
horizons_results = pd.read_csv(horizons_results_csv, sep=' ', names=columns)

i = scan_id

idx_r = np.where(horizons_results.scan_id == i)
object = horizons_results.obj_designation.to_numpy()[idx_r]
objra = horizons_results.obj_ra.to_numpy()[idx_r]
objde = horizons_results.obj_dec.to_numpy()[idx_r]
objmag = horizons_results.obj_mag.to_numpy()[idx_r]
objrahrsmmss = horizons_results.obj_ra_hrsmmss.to_numpy()[idx_r]
objdecdgrmmss = horizons_results.obj_dec_dgrmmss.to_numpy()[idx_r]

szobj = np.size(idx_r)

# field of view for zoom
fov = 1. / 3.  # in degrees
fovm = int(fov * 60.)

# get DSS fits

print(object)

# one scan can have multiple objects on it, hence the next loop
for obj in range(szobj):
    object_s = object[obj]
    objra_s = objra[obj]
    objde_s = objde[obj]
    objmag_s = objmag[obj]
    objrahrsmmss_s = objrahrsmmss[obj]
    objdecdgrmmss_s = objdecdgrmmss[obj]

    dssfits = str(object[obj]) + '_dss'
    dssfits = dssfits.replace(" ", "_")
    dssfits = dssfits.replace("(", "_")
    dssfits = dssfits.replace(")", "_")

    print(dssfits, objrahrsmmss[0], objdecdgrmmss[0])

    #   parse input for dss batch tool

    objrahrsmmss_s = objrahrsmmss_s.replace("(", "")
    objrahrsmmss_s = objrahrsmmss_s.replace(")", "")
    objrahrsmmss_s = objrahrsmmss_s.replace(",", "")

    objdecdgrmmss_s = objdecdgrmmss_s.replace("(", "")
    objdecdgrmmss_s = objdecdgrmmss_s.replace(")", "")
    objdecdgrmmss_s = objdecdgrmmss_s.replace(",", "")

    if (objdecdgrmmss_s[0:1] == "-"):
        objdecdgrmmss_s = objdecdgrmmss_s.replace("-", "")
        objdecdgrmmss_s = '-' + objdecdgrmmss_s
    else:
        objdecdgrmmss_s = objdecdgrmmss_s

    if (objdecdgrmmss_s[0:1] == "0" and objdecdgrmmss_s[2:3] == "-"):
        objdecdgrmmss_s = objdecdgrmmss_s.replace("-", "")
        objdecdgrmmss_s = '-' + objdecdgrmmss_s
    else:
        objdecdgrmmss_s = objdecdgrmmss_s

    print(objrahrsmmss_s, objdecdgrmmss_s)

    dssf = "dssinput.in"
    dssw = dssfits + ' ' + objrahrsmmss_s + ' ' + objdecdgrmmss_s + ' ' + str(fovm) + ' ' + str(fovm)
    print(dssw)
    fl = open(dssf, "w")
    fl.write(dssw)
    fl.close()

    os.system("dss1 -i dssinput.in")
    #sts, dss_fits = commands.getstatusoutput("ls *.fits")
    sts, dss_fits = subprocess.check_output("ls *.fits")
    os.system("mv *.fits DATA/")  # move the file to RESULTS
    os.system("rm -f dssinput.in")

    print(dss_fits)

    # initialize plate object by attributes
    plate_1 = appl.applause(i, applause_input, object_s, objra_s, objde_s, objmag_s, dss_fits, mode)

    figsize = plate_1.get_shape()
    xsz = figsize[1]
    ysz = figsize[0]
    xsize = 7.
    ysize = int(ysz * xsize / xsz)

    # define offsets if needed
    #    raoffset = -0.001 # scan 17017 723 Hammonia
    #    decoffset = 0.005 # scan 17017 723 Hammonia
    #    raoffset = -0.018 # scan 17220 350 Ornamenta
    #    decoffset = -0.003 # scan 17220 350 Ornamenta
    raoffset = 0.
    decoffset = 0.

    print("raoffset (in minutes): ", round(raoffset * 60., 2))
    print("decoffset (in minutes): ", round(decoffset * 60., 2))
    #    raoffset = 0.
    #    decoffset = 0.

    # initialize figure
    fig_1 = plt.figure(1, figsize=(xsize, ysize))

    plate_1.display_plate('gray', 'auto', 'lower', raoffset, decoffset)
    plate_1.display_stars()
    plate_1.display_object()
    plate_1.enable_clicks(fig_1)
    #    plate_1.save_plate()
    #    plate_1.show_header('DATE-AVG')

    # initialize figure
    fig_2 = plt.figure(2, figsize=(6, 6))

    plate_1.display_plate_zoom(fov, 'gray', 'auto', 'lower', 1., 1, raoffset, decoffset)
    plate_1.display_stars_zoom(fov)
    plate_1.display_object()
    plate_1.enable_clicks_zoom(fig_2, fov)
    #    plate_1.save_plate_zoom()

    # initialize figure
    fig_3 = plt.figure(3, figsize=(6, 6))

    plate_1.display_observation(fov, 'gray_r', 'auto', 'lower', 1)
    plate_1.display_object()
    #    plate_1.save_obs_zoom()

    #    plt.close('all')

    plt.show()
