# https://www.plate-archive.org/applause/documentation/scripted-access-tap/

import requests
import os.path
import pyvo as vo
import numpy as np
import pandas
import sys

name = 'APPLAUSE'
url = 'https://www.plate-archive.org/tap'
token = '71966108a826fa1322537884f762862976b80cbb'
#qstr = 'SELECT * FROM applause_dr3.archive limit 5'
#qstr = 'select filename_scan from applause_dr3.scan where plate_id=17133' # INTRODUCE CHECK, DO NOT DOWNLOAD IF FILES DOWNLOADED ALREADY
qstr = 'select filename_scan from applause_dr3.scan where scan_id=17133'

# !! scan id is not plate id

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
results = job.fetch_result()
print(results)

#print(type(results))
#print(type(results.getrecord(0)))
#print(type(results.getrecord(0)['filename_scan']))
#print(results.getrecord()['filename_scan'])
#sys.exit()

#print("Downloading ... {}".format(results.getrecord(0)['filename_scan']))
#print("Downloading ... {}".format(results.getrecord(1)['filename_scan']))
#print(len(results))
#sys.exit()

for i in range(len(results)):
    file_path = results.getrecord(i)['filename_scan']
    print("Downloading .. {} .. {}".format(i,results.getrecord(i)['filename_scan']))
    #print("Downloading ... {}".format(filename_url.getrecord(0)['filename_scan']))
    try:
        r = requests.get(results.getrecord(i)['filename_scan'])
    except requests.exceptions.HTTPError as e:  # https://pavolkutaj.medium.com/exception-handling-of-python-requests-module-73dcdeb42aa4
        print(e, file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
    #filename = "tmp/test{}.fits".format(str(i))
    filename = "DATA_FITS/{}".format(file_path.split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(r.content)
