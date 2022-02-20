import requests
import pyvo as vo
import sys
import os


# https://www.plate-archive.org/applause/documentation/scripted-access-tap/
class ApplauseFits():

    def __init__(self):

        self.name = 'APPLAUSE'
        self.url = 'https://www.plate-archive.org/tap'
        self.token = '71966108a826fa1322537884f762862976b80cbb'

    def getFits(self, scanId):
        # https://www.plate-archive.org/applause/documentation/scripted-access-tap/

        name = self.name
        url = self.url
        token = self.token

        qstr = 'select filename_scan from applause_dr3.scan where scan_id={}'.format(scanId)

        # !! scan id is not plate id

        # print('\npyvo version %s \n' % vo.__version__)
        # print('TAP service %s \n' % name)

        tap_session = requests.Session()
        tap_session.headers['Authorization'] = token
        tap_service = vo.dal.TAPService(url, session=tap_session)
        lang = 'PostgreSQL'
        job = tap_service.submit_job(qstr, language=lang)
        job.run()
        job.wait(phases=["COMPLETED", "ERROR", "ABORTED"], timeout=30.)
        job.raise_if_error()
        results = job.fetch_result()

        # print(type(results))
        # print(type(results.getrecord(0)))
        # print(type(results.getrecord(0)['filename_scan']))
        # print(results.getrecord()['filename_scan'])
        # sys.exit()

        # print("Downloading ... {}".format(results.getrecord(0)['filename_scan']))
        # print("Downloading ... {}".format(results.getrecord(1)['filename_scan']))
        # print(len(results))
        # sys.exit()

        for i in range(len(results)):
            filePath = results.getrecord(i)['filename_scan']
            print("Downloading .. {} .. {}".format(i, filePath))
            try:
                r = requests.get(results.getrecord(i)['filename_scan'])
            except requests.exceptions.HTTPError as e:  # https://pavolkutaj.medium.com/exception-handling-of-python-requests-module-73dcdeb42aa4
                print(e, file=sys.stderr)
            except requests.exceptions.RequestException as e:
                print(e, file=sys.stderr)
            filename = filePath.split('/')[-1]
            pathToFits = os.path.join('DATA_FITS', filename)
            with open(pathToFits, 'wb') as f:
                f.write(r.content)
