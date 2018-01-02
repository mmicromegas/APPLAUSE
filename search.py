import pandas as pd
import callhorizons
import APPLAUSE_CSV as apcs
import csv
import time
import datetime
import numpy as np
import os
import re

filename='DATA/master_ra_0_360_dec_m90_p90.csv'
#os.system("echo.>RESULTS\restart.txt")


# initialize plate object by attributes
obs = apcs.applause(filename)

scanplates = obs.extract('scan_id').unique()
extlist = np.genfromtxt('RESULTS/'+str('restart')+'.txt',delimiter=' ',dtype=int)

idxarray = []
for row in extlist:
    idx = np.where(scanplates == row)
    idxarray.append(idx)

scanplates_final = np.delete(scanplates,idxarray)


#print(scanplates_final)
#print(scanplates)


#platedata=obs.extract_plate_data(15589)
#print(platedata)

#obs_datetime_csv = platedata['ut_mid'].unique()
#print('DATETIME utmid from csv: ',obs_datetime_csv)

# open file for results
#fileres = open('RESULTS\\'+str(filename)+'_results'+'.txt','a')
#filewri = csv.writer(fileres,delimiter=' ')
#filewri.writerow(['OBS','scan_ID','Object','RA2000','DEC2000','RA2000HHMMSS','DEC2000DDMMSS','MAGNITUDE'])


for scan in scanplates_final:
    scandata=obs.extract_scan_data(scan)      
    maxra = max(scandata['raj2000'])
    minra = min(scandata['raj2000'])
    maxde = max(scandata['dej2000'])
    minde = min(scandata['dej2000'])
    obs_datetime = scandata['ut_mid'].unique()[0]
    obs_filename_scan = scandata['filename_scan'].unique()[0]
    obs_filename_scan_mod = obs_filename_scan[:obs_filename_scan.index(".")]
    obs_scanid = scan
    print('scan_ID and filename: ',obs_scanid,obs_filename_scan_mod)
    print('MAXRA: ',maxra,'MINRA: ',minra,'MAXDE: ',maxde,'MINDE: ',minde)
    print('UT_MID: ',obs_datetime)

	
# parse out date and hours:minutes only

#    print(scandata['ut_mid'].unique())
#    print(obs_datetime)
#    tidx = obs_datetime.index('')
    date = obs_datetime[0:10]
    hrs = obs_datetime[11:13]
    minutes = int(obs_datetime[14:16])

# min_plus is time of observation +1 minute 
    minutes_plus = int(obs_datetime[14:16])+1

# workaround for minutes equal to 59

    if minutes_plus == 60:
        minutes = 58
        minutes_plus = 59

    minutes = str(minutes)    
    minutes_plus = str(minutes_plus)

    obs_dt = date+' '+hrs+':'+minutes
    obs_dt_plus = date+' '+hrs+':'+minutes_plus

#    print('OBS_DT,OBS_DT_PLUS: ',obs_dt,obs_dt_plus,date,hrs,minutes)

    file=open('DATA/MPCfirst2000.txt','r')
    observatory = 29 # this is Hamburg Sternwarte

    timebeg = time.time()
    timebeg0 = timebeg

    fileres = open('RESULTS/'+str(filename)+'_results'+'.txt','a')
    filewri = csv.writer(fileres,delimiter=' ')
	
    i = 0
    for line in file:
        i += 1
#        line = line.replace("\r\n","")
#        print(line.replace("\r\n",""))
        objectno = line[line.find("(")+1:line.find(")")]
        obj = callhorizons.query(objectno)
        obj.set_epochrange(obs_dt, obs_dt_plus, '1h')
        obj.get_ephemerides(observatory)
#        print(objectno,obj['targetname'][0],line.replace("\r\n",""))
        if (minra < obj['RA'][0] < maxra) and (minde < obj['DEC'][0] < maxde):
            print(observatory,obs_scanid,line,obj['targetname'][0],objectno,obj['RA'][0], obj['DEC'][0], obj['V'][0])
#            fileres = open('RESULTS\\'+str(filename)+'_results'+'.txt','a')
#            filewri = csv.writer(fileres,delimiter=' ')
            filewri.writerow([observatory,obs_scanid,objectno,obj['targetname'][0],obj['RA'][0], obj['DEC'][0], obs.calc_ra(obj['RA'][0]),obs.calc_dec(obj['DEC'][0]),obj['V'][0]])
#            fileres.close()
        if (i % 500) == 0:
            timeend = time.time()
            timeelapsed=str(datetime.timedelta(seconds=(timeend-timebeg)))
            timeelapsed0=str(datetime.timedelta(seconds=(timeend-timebeg0)))
            print('Currently at:',str(i)+ ' Last 500 rows done in [hh:mm:ss]',timeelapsed,'Elapsed time: [hh:mm:ss]',timeelapsed0)     
            timebeg = time.time()		

    file.close()
    fileres.close()

# write restart file

    filerst = open('RESULTS/'+str('restart')+'.txt','a')
    filewrirst = csv.writer(filerst)
    filewrirst.writerow([scan])
    filerst.close()
	
# end

	


