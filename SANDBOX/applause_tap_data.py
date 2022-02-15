# https://www.plate-archive.org/applause/documentation/scripted-access-tap/

import requests
import os
import pyvo as vo
import numpy as np
import pandas as pd
import sys

name = 'APPLAUSE'
url = 'https://www.plate-archive.org/tap'
token = '71966108a826fa1322537884f762862976b80cbb'
# qstr = 'select filename_scan from applause_dr3.scan where plate_id=367'
scan_id = '17133'
scan_id_list = "({})".format(scan_id)
filename_csv = 'csv_scan_id_{}'.format(scan_id)
build_path_to_csv = os.path.join('DATA_CSV',filename_csv)
print(build_path_to_csv)
if os.path.isfile(build_path_to_csv):
       print('File {}'.format(filename_csv)+' exists')
       results = pd.read_csv(build_path_to_csv)
else:
       print('No file - storing to csv')
       qstr = 'select src.plate_id,src.scan_id,sc.filename_scan,pl.telescope,pl.observatory,' \
              'ex.ut_start,ex.ut_mid,ex.ut_end,src.flag_rim,src.source_id,src.x_source,' \
              'src.y_source,src.x_peak,src.y_peak,src.x_psf,src.y_psf,srcb.raj2000,srcb.dej2000,' \
              'srcb.vmag, srcb.vmagerr,srcb.tycho2_id,srcb.ucac4_id from APPLAUSE_DR3.source src ' \
              'inner join APPLAUSE_DR3.source_calib srcb on src.source_id=srcb.source_id ' \
              'inner join APPLAUSE_DR3.exposure ex on ex.plate_id = src.plate_id ' \
              'inner join APPLAUSE_DR3.plate pl on pl.plate_id=src.plate_id ' \
              'inner join APPLAUSE_DR3.scan sc on sc.scan_id = src.scan_id ' \
              'where (src.scan_id in {}' \
              'and src.flag_rim=0 and srcb.tycho2_id is not null and ex.ut_mid is not null)'.format(scan_id_list)

       print('\npyvo version %s \n' % vo.__version__)
       print('TAP service %s \n' % name)

       tap_session = requests.Session()
       tap_session.headers['Authorization'] = token

       tap_service = vo.dal.TAPService(url, session=tap_session)

       lang = 'PostgreSQL'

       job = tap_service.submit_job(qstr, language=lang)
       job.run()

       job.wait(phases=["COMPLETED", "ERROR", "ABORTED"], timeout=30.)

       job.raise_if_error()
       results = job.fetch_result().to_table().to_pandas()  # STORE THE RESULTS TO DATA_CSV and check before you do TAP again, if you have the data already SKIP

       results.to_csv(build_path_to_csv, index=False)


#print(results)
#print(type(results))

#print(type(results))
#print(type(results.getrecord(0)))
#print(type(results.getrecord(0)['filename_scan']))
#print(results.getrecord(0)['filename_scan'])
#sys.exit()

#print(max(results.getcolumn('dej2000')))
#print(results.getcolumn('ut_mid'))
#print(type(results.getcolumn('ut_mid')))
#print(np.unique(results.getcolumn('ut_mid'))[0])

#for i in range(len(results)):
#    record = results.getrecord(i)
#    print(i,record)

#print(type(record))

#maxra = max(results.getcolumn('raj2000'))
#minra = min(results.getcolumn('raj2000'))
#maxde = max(results.getcolumn('dej2000'))
#minde = min(results.getcolumn('dej2000'))

maxra = max(results.loc[:,"raj2000"])
minra = min(results.loc[:,"raj2000"])
maxde = max(results.loc[:,"dej2000"])
minde = min(results.loc[:,"raj2000"])

#obs_datetime = np.unique(results.getcolumn('ut_mid'))[0]
#obs_filename_scan = np.unique(results.getcolumn('filename_scan'))[0]
#obs_filename_scan_mod = obs_filename_scan[:obs_filename_scan.index(".")]

obs_datetime = np.unique(results.loc[:,"ut_mid"])[0]
obs_filename_scan = np.unique(results.loc[:,"filename_scan"])[0]

obs_scanid = scan_id_list
print('scan_ID:', obs_scanid)
filename = obs_filename_scan.split('/')[-1]
print('filename:',filename)
print('MAXRA: ', maxra, 'MINRA: ', minra, 'MAXDE: ', maxde, 'MINDE: ', minde)
print('UT_MID: ', obs_datetime)
print(type(obs_datetime))
obs_datetime_pd = pd.to_datetime(obs_datetime)
print(obs_datetime_pd)
print(obs_datetime_pd.year)
print(obs_datetime_pd.month)
print(obs_datetime_pd.day)
print(obs_datetime_pd.hour)
print(obs_datetime_pd.minute)
print(obs_datetime_pd.second)
print(obs_datetime_pd.strftime('%Y-%m-%d')) # get date only

# check if the fits exist for the given plate_id , if yes display + show stars

build_path_to_fits = os.path.join('DATA_FITS',filename)
print(build_path_to_fits)
if os.path.isfile(build_path_to_fits):
       print('File {}'.format(filename)+' exists')
       # display fits and stars
else:
       print('No file')
       # download fits
       # display fits and stars


