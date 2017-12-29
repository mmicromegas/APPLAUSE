from astropy.io import fits
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy
from scipy import ndimage

class applause:

    def __init__(self,scan,datacsv,object,objra,objde,objmag,dataobs,mode):
		# read CSV
		
        self.platecsv = datacsv
        self.mode = mode				
		
		# extract from CSV

        self.plate_id  = self.platecsv.plate_id
        self.scan_id = self.platecsv.scan_id	
        self.filename_scan = self.platecsv.filename_scan		
        self.row_id    = self.platecsv.row_id
        self.ut_mid    = self.platecsv.ut_mid
        self.source_id = self.platecsv.source_id
        self.x_source  = self.platecsv.x_source
        self.y_source  = self.platecsv.y_source
        self.x_peak    = self.platecsv.x_peak
        self.y_peak    = self.platecsv.y_peak
        self.x_psf     = self.platecsv.x_psf
        self.y_psf     = self.platecsv.y_psf
        self.raj2000   = self.platecsv.raj2000
        self.dej2000   = self.platecsv.dej2000
        self.vmag      = self.platecsv.vmag
        self.vmagerr   = self.platecsv.vmagerr
        self.tycho2_id = self.platecsv.tycho2_id
        self.ucac4_id  = self.platecsv.ucac4_id
		
		# manipulate input data for PROCESSING 

        idx = np.where(self.scan_id == scan)

#        print(scan,idx)		
        self.filename_scan_matrix = self.filename_scan.as_matrix()[idx]
        dataplate = self.filename_scan_matrix[0]
        print(dataplate)
		
	    # read FITS
		
        self.plate    = fits.getdata('DATA\\'+dataplate)
		
        self.plate_id_uq = self.plate_id.as_matrix()[idx]
        self.scan_id_uq = self.scan_id.as_matrix()[idx]		
        self.ut_mid_matrix = self.ut_mid.as_matrix()[idx]
        self.row_id_matrix    = self.row_id.as_matrix()[idx]
        self.tycho2_id_matrix  = self.tycho2_id.as_matrix()[idx]  # convert dataframe to an array
        self.raj2000_matrix   = self.raj2000.as_matrix()[idx]
        self.dej2000_matrix   = self.dej2000.as_matrix()[idx]
        self.vmag_matrix      = self.vmag.as_matrix()[idx]
		
        self.x_source_matrix  = self.x_source.as_matrix()[idx]
        self.y_source_matrix  = self.y_source.as_matrix()[idx]
        self.x_peak_matrix    = self.x_peak.as_matrix()[idx]
        self.y_peak_matrix    = self.y_peak.as_matrix()[idx]
        self.x_psf_matrix     = self.x_psf.as_matrix()[idx]
        self.y_psf_matrix     = self.y_psf.as_matrix()[idx]

        self.object = object
        self.objra = objra
        self.objde = objde
        self.objmag = objmag 		
        print(object)
		
# this is for _x

        if (self.mode == 0 or self.mode == 3):
            self.xexmin = np.min(self.dej2000_matrix)
            self.xexmax = np.max(self.dej2000_matrix) 
            self.yexmin = np.min(self.raj2000_matrix)
            self.yexmax = np.max(self.raj2000_matrix)

# this is for _y
		
        if (self.mode == 1 or self.mode == 2):
            self.xexmin = np.min(self.raj2000_matrix)
            self.xexmax = np.max(self.raj2000_matrix) 
            self.yexmin = np.min(self.dej2000_matrix)
            self.yexmax = np.max(self.dej2000_matrix)
			
        self.ixmin  = np.min(self.x_peak_matrix)
        self.ixmax  = np.max(self.x_peak_matrix)
        self.iymin  = np.min(self.y_peak_matrix)
        self.iymax  = np.max(self.y_peak_matrix)		
		
        if dataobs =='':
            self.dataobsname = ''
            pass
        else:
            self.dataobsname = dataobs		
            self.dataobs =  fits.getdata(dataobs)

    def get_literal(self,dataplate):
        filename_scan_literal = dataplate[dataplate.index(".")-1:dataplate.index(".")]		
        return filename_scan_literal
			
    def get_shape(self):
	    return self.plate.shape
		
    def display_plate(self,param_cmap,param_aspect,param_origin,raoffset,decoffset):
        if self.mode == 0:
            plt.imshow(self.plate[self.iymin:self.iymax,self.ixmin:self.ixmax], extent=(self.xexmax+decoffset,self.xexmin+decoffset,self.yexmax+raoffset,self.yexmin+raoffset),cmap=param_cmap,aspect=param_aspect,origin=param_origin)
        if self.mode == 1:
            plt.imshow(self.plate[self.iymin:self.iymax,self.ixmin:self.ixmax], extent=(self.xexmin+raoffset,self.xexmax+raoffset,self.yexmax+decoffset,self.yexmin+decoffset),cmap=param_cmap,aspect=param_aspect,origin=param_origin)
        if self.mode == 2:
            plt.imshow(self.plate[self.iymin:self.iymax,self.ixmin:self.ixmax],extent=(self.xexmax+raoffset,self.xexmin+raoffset,self.yexmin+decoffset,self.yexmax+decoffset),cmap=param_cmap,aspect=param_aspect,origin=param_origin)			
        if self.mode == 3:
            plt.imshow(self.plate[self.iymin:self.iymax,self.ixmin:self.ixmax], extent=(self.xexmax+decoffset,self.xexmin+decoffset,self.yexmax+raoffset,self.yexmin+raoffset),cmap=param_cmap,aspect=param_aspect,origin=param_origin)
        plt.rcParams.update({'axes.titlesize': 'small'})
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.title(str(self.object)+' '+str(self.plate_id_uq[0])+' '+str(self.ut_mid_matrix[0])+' '+str(np.around(self.objmag,decimals=3))) 		

    def display_observation(self,fov,param_cmap,param_aspect,param_origin,alpha):
        ra = self.objra[0]
        dec = self.objde[0]	
        xsz = fov/2.
        ysz = fov/2.
        dpx = (self.xexmin-self.xexmax)/(self.ixmax-self.ixmin)
        dpy = (self.yexmax-self.yexmin)/(self.iymax-self.iymin)
        xszpx = int(xsz/dpx)
        yszpx = int(ysz/dpy)	
        iyminz = (self.iymin+int((dec-self.yexmin)/dpy))-yszpx 
        iymaxz = (self.iymin+int((dec-self.yexmin)/dpy))+yszpx 
        ixminz = (self.ixmin+int((self.xexmin-ra)/dpx))-xszpx
        ixmaxz = (self.ixmin+int((self.xexmin-ra)/dpx))+xszpx
        xexminz = ra+xsz
        xexmaxz = ra-xsz
        yexminz = dec-ysz
        yexmaxz = dec+ysz
        plt.imshow(self.dataobs, cmap=param_cmap,extent=(xexminz,xexmaxz,yexminz,yexmaxz),aspect=param_aspect,origin=param_origin,alpha=alpha)
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.title(str(self.dataobsname))
		
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
	
		
    def display_plate_zoom(self,fov,param_cmap,param_aspect,param_origin,alpha,dsp):
        ra = self.objra
        dec = self.objde	
        xsz = fov/2.
        ysz = fov/2.
        dpx = (self.xexmin-self.xexmax)/(self.ixmin-self.ixmax)
        dpy = (self.yexmax-self.yexmin)/(self.iymax-self.iymin)
        xszpx = int(xsz/dpx)
        yszpx = int(ysz/dpy)	
        iyminz = (self.iymin+int((dec-self.yexmin)/dpy))-yszpx 
        iymaxz = (self.iymin+int((dec-self.yexmin)/dpy))+yszpx 
        ixminz = (self.ixmax+int((self.xexmin-ra)/dpx))-xszpx
        ixmaxz = (self.ixmax+int((self.xexmin-ra)/dpx))+xszpx
        xexminz = ra+xsz
        xexmaxz = ra-xsz
        yexminz = dec-ysz
        yexmaxz = dec+ysz

        if dsp == 1:
            plt.imshow(self.plate[iyminz:iymaxz,ixminz:ixmaxz], cmap=param_cmap,extent=(xexminz,xexmaxz,yexminz,yexmaxz),aspect=param_aspect,origin=param_origin,alpha=alpha)
        else:
            print('RAmax: ',self.calc_ra(xexminz),'RAmin: ',self.calc_ra(xexmaxz),'DECmax: ',self.calc_dec(yexminz),'DECmin: ',self.calc_dec(yexmaxz))

        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.rcParams.update({'axes.titlesize': 'small'})
        plt.title(str(self.object)+' '+str(self.plate_id_uq[0])+' '+str(self.ut_mid_matrix[0])+' '+str(np.around(self.objmag,decimals=3))) 
		
    def display_tycho2(self,lmag,minra,maxra,minde,maxde):
        f = fits.open('build/tyc2.fits')  # open a FITS file
        tbdata = f[1].data  # assume the first extension is a table
		
        tycho2star_ra = []
        tycho2star_de = []

        for row in tbdata:
            if (row['MAG_VT']) < lmag and (minra < row['RA'] < maxra) and (minde < row['DEC'] < maxde):
                tycho2star_ra.append(row['RA']) 
                tycho2star_de.append(row['DEC'])
				
        plt.scatter(tycho2star_ra, tycho2star_de, c='g', s=30,alpha=0.3,picker=True)
				
    def display_stars(self):
        if (self.mode == 0 or self.mode == 3):
            plt.scatter(self.dej2000_matrix, self.raj2000_matrix, c='r', s=40,alpha=0.3,picker=True)
        if (self.mode == 1 or self.mode == 2):
            plt.scatter(self.raj2000_matrix, self.dej2000_matrix, c='r', s=40,alpha=0.3,picker=True)			

    def display_stars_zoom(self,fov):
        ra = self.objra
        dec = self.objde
        xsz = fov/2.
        ysz = fov/2.
        ramin = ra - xsz
        ramax = ra + xsz
        decmin = dec - ysz 
        decmax = dec + ysz			
        razoom = []
        deczoom = []
        raj2000 = self.raj2000_matrix
        dej2000 = self.dej2000_matrix	
        sz = np.size(raj2000)		
        for i in range(sz):
            if ((ramin < raj2000[i] < ramax) and (decmin < dej2000[i] < decmax)):
                    razoom.append(raj2000[i])
                    deczoom.append(dej2000[i])
		
        plt.scatter(razoom, deczoom, c='r', s=40,alpha=0.3,picker=True)


    def display_object(self):
        ra = self.objra
        de = self.objde
        if self.mode == 2:
            plt.scatter(ra,de,c='b',s=100,alpha=0.1)	
        if self.mode == 3:
            plt.scatter(de,ra,c='b',s=100,alpha=0.1)			

    def get_bndry(self,param):
        # put values in series
        bndry = {'minra':np.min(self.raj2000_matrix),'maxra':np.max(self.raj2000_matrix), 'minde': np.min(self.dej2000_matrix), 'maxde': np.max(self.dej2000_matrix)}
        return bndry[param]
		
    def SetMatplotlibParams(self):
        # plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
        plt.rc('font',**{'family':'serif','serif':['Times New Roman']})
        plt.rc('font',size=18.)
        plt.rc('lines',linewidth=2,markeredgewidth=2.,markersize=10)
        plt.rc('axes',linewidth=1.5)
        plt.rcParams['xtick.major.size']=6.
        plt.rcParams['xtick.minor.size']=2.
        plt.rcParams['figure.subplot.bottom']=0.13
        plt.rcParams['figure.subplot.left']=0.17

    def convra(self,ra):
        self.dgrhrs = 15.
        self.rah = np.trunc(ra/self.dgrhrs)
        self.ram = (ra/self.dgrhrs-self.rah)*60.
        self.ras = (self.ram-np.trunc(self.ram))*60.
        return self.rah[0],np.trunc(self.ram[0]),np.trunc(self.ras[0])

    def convde(self,de):
        self.ded = np.trunc(de)
        self.dem = (de-self.ded)*60.
        self.des = (self.dem-np.trunc(self.dem))*60.
        return self.ded[0],np.trunc(self.dem[0]),np.trunc(self.des[0])
	
    def onpick(self,event):
        ind = event.ind
        print 'IND: ',ind
        print 'ROW_ID: ', self.row_id_matrix[ind]
        print 'TYCHO2 catalog ID:', self.tycho2_id_matrix[ind]
        print 'RAJ2000 (hrs/mm/sss): ',self.convra(self.raj2000_matrix[ind])
        print 'DEJ2000 (dgr/mm/ss): ',self.convde(self.dej2000_matrix[ind])
        print 'VMAG: ', self.vmag_matrix[ind]
 #       print 'dataloc: vmag' , data.loc[row_id[ind]-1,'vmag'].values			

    def enable_clicks(self,figure):
	    figure.canvas.mpl_connect('pick_event', self.onpick)
 
    def show_header(self,param):	
        #https://www.plate-archive.org/applause/project/fits-header-for-photoplates/ 
        self.plateh   = fits.getheader(self.dataplate)	
        print self.plateh[param] 
		
    def return_header(self,param):	
        #https://www.plate-archive.org/applause/project/fits-header-for-photoplates/ 
        self.plateh   = fits.getheader(self.dataplate)	
        return self.plateh[param] 		
		
    def return_plateid(self):	
        return self.plate_id[0]
		
    def return_utmid(self):	
        return self.ut_mid_matrix[0]
		
    def save_plate(self):
        object = self.object
        filename=str(object)+'_'+str(self.scan_id_uq[0])+'_plate.png'
#        filename=str(object)+'_plate.png'
        filename = 'RESULTS//'+filename.replace(" ","_")
        filename = filename.replace("(","_")
        filename = filename.replace(")","_")		
        plt.savefig(filename)
		
    def save_plate_zoom(self):
        object = self.object
        filename=str(object)+'_'+str(self.scan_id_uq[0])+'_zoom_plate.png'
		
#        filename=str(object)+'_zoom_plate.png'
        filename = 'RESULTS//'+filename.replace(" ","_")
        filename = filename.replace("(","_")
        filename = filename.replace(")","_")
        plt.savefig(filename)
		
    def save_obs_zoom(self):
        object = self.object
        filename=str(object[0:object.index("(")-1])+'_zoom_obs.png'
        filename = 'RESULTS//'+filename.replace(" ","_")
        plt.savefig(filename)
		