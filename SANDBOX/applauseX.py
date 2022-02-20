# applauseX a.k.a. applause(Xploration)

import importlib

import os
import numpy as np
import pandas as pd
import UTILS
importlib.reload(UTILS)
importlib.reload(UTILS.Display)

from UTILS.ApplauseFits import ApplauseFits
from UTILS.Display import Display
from UTILS.ApplauseMetadata import ApplauseMetadata
from UTILS.ReadParams import ReadParams

import sys

# def main(): # using def main breaks the onclick

# check python version
if sys.version_info[0] < 3:
    print("Python " + str(sys.version_info[0]) + "  is not supported. EXITING.")
    sys.exit()

# create os independent path and read parameter file
paramFile = os.path.join('PARAMS', 'param.display')
params = ReadParams(paramFile)

# get input parameters
scanIdDisp = params.getParam('prop')['scanIdDisp']

#scanIdDisp = '17139'
scanIdList = "({})".format("'17133','17134'")

applauseInputCsv = os.path.join('DATA_CSV', 'masterApplauseInfoScan.csv')

if os.path.isfile(applauseInputCsv):
    print('File {}'.format(applauseInputCsv) + ' exists')
    results = pd.read_csv(applauseInputCsv)
    scanIdUnique = pd.unique(results['scan_id']).tolist()

    if scanIdDisp in scanIdUnique:
        results = pd.read_csv(applauseInputCsv)
    else:
        tap = ApplauseMetadata(applauseInputCsv, "({})".format(scanIdDisp))
        tap.updateApplauseData()
        results = pd.read_csv(applauseInputCsv)
else:
    print('No file - storing to csv')
    tap = ApplauseMetadata(applauseInputCsv, scanIdList)
    tap.createApplauseData()
    results = pd.read_csv(applauseInputCsv)

resultscanIdDisp = results.loc[results['scan_id'] == scanIdDisp]

maxra = max(resultscanIdDisp.loc[:, "raj2000"])
minra = min(resultscanIdDisp.loc[:, "raj2000"])
maxde = max(resultscanIdDisp.loc[:, "dej2000"])
minde = min(resultscanIdDisp.loc[:, "raj2000"])

# obs_datetime = np.unique(resultscanIdDisp.getcolumn('ut_mid'))[0]
# obs_filename_scan = np.unique(resultscanIdDisp.getcolumn('filename_scan'))[0]
# obs_filename_scan_mod = obs_filename_scan[:obs_filename_scan.index(".")]

obs_datetime = np.unique(resultscanIdDisp.loc[:, "ut_mid"])[0]
obs_filename_scan = np.unique(resultscanIdDisp.loc[:, "filename_scan"])[0]

#obs_scanid = scanIdList
#print('scan_ID:', obs_scanid)

print('scan_ID:', scanIdDisp)
filename = obs_filename_scan.split('/')[-1]
print('filename:', filename)
print('MAXRA: ', maxra, 'MINRA: ', minra, 'MAXDE: ', maxde, 'MINDE: ', minde)
print('UT_MID: ', obs_datetime)
print(type(obs_datetime))
obs_datetime_pd = pd.to_datetime(obs_datetime)
# print(obs_datetime_pd)
# print(obs_datetime_pd.year)
# print(obs_datetime_pd.month)
# print(obs_datetime_pd.day)
# print(obs_datetime_pd.hour)
# print(obs_datetime_pd.minute)
# print(obs_datetime_pd.second)
# print(obs_datetime_pd.strftime('%Y-%m-%d')) # get date only

# check if the fits exist for the given plate_id , if yes display + show stars

path_to_fits = os.path.join('DATA_FITS', filename)
if os.path.isfile(path_to_fits):
    print('File {}'.format(filename) + ' exists')

    # initialize plate object by attributes
    mode = 2
    plate = Display(scanIdDisp, results, mode)
    fig = plate.displayPlate('gray', 'auto', 'lower')
    plate.displayStars()
    # plate.display_object()
    plate.enableClicks(fig)
else:
    print('No fits file exists!')

    # download fits
    appl = ApplauseFits()
    appl.getFits(scanIdDisp)

    # initialize plate object by attributes
    mode = 2  # can be deduced from _x and _y ?
    plate = Display(scanIdDisp, results, mode)
    fig = plate.displayPlate('gray', 'auto', 'lower')
    plate.displayStars()
    plate.enableClicks(fig)

# EXECUTE MAIN
# if __name__ == "__main__":
#    main()

# END
