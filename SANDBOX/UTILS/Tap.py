import requests
import pyvo as vo

# https://www.plate-archive.org/applause/documentation/scripted-access-tap/
class Tap():

    def __init__(self,applauseInputCsv):
        self.applauseInputCsv = applauseInputCsv

    def updateApplauseData(self,scanIdList):
        qstr = 'select src.plate_id,src.scan_id,sc.filename_scan,pl.telescope,pl.observatory,' \
               'ex.ut_start,ex.ut_mid,ex.ut_end,src.flag_rim,src.source_id,src.x_source,' \
               'src.y_source,src.x_peak,src.y_peak,src.x_psf,src.y_psf,srcb.raj2000,srcb.dej2000,' \
               'srcb.vmag, srcb.vmagerr,srcb.tycho2_id,srcb.ucac4_id from APPLAUSE_DR3.source src ' \
               'inner join APPLAUSE_DR3.source_calib srcb on src.source_id=srcb.source_id ' \
               'inner join APPLAUSE_DR3.exposure ex on ex.plate_id = src.plate_id ' \
               'inner join APPLAUSE_DR3.plate pl on pl.plate_id=src.plate_id ' \
               'inner join APPLAUSE_DR3.scan sc on sc.scan_id = src.scan_id ' \
               'where (src.scan_id in {}' \
               'and src.flag_rim=0 and srcb.tycho2_id is not null and ex.ut_mid is not null)'.format(scanIdList)

        name = 'APPLAUSE'
        url = 'https://www.plate-archive.org/tap'
        token = '71966108a826fa1322537884f762862976b80cbb'

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

        print('Downloading TAP')
        print(scanIdList)
        results.to_csv(self.applauseInputCsv, index=False)

