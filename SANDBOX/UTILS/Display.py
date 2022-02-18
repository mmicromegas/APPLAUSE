from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


class Display():

    def __init__(self, scanId, dfCsv, mode):
        self.mode = mode
        dfCsvScanId = dfCsv.loc[dfCsv['scan_id'] == int(scanId)]

        # extract from DATA_CSV
        plate_id = dfCsvScanId.plate_id.unique()[0]
        scan_id = dfCsvScanId.scan_id.unique()[0]
        filename_scan = dfCsvScanId.filename_scan.unique()[0]
        ut_mid = dfCsvScanId.ut_mid
        source_id = dfCsvScanId.source_id
        x_source = dfCsvScanId.x_source
        y_source = dfCsvScanId.y_source
        x_peak = dfCsvScanId.x_peak
        y_peak = dfCsvScanId.y_peak
        x_psf = dfCsvScanId.x_psf
        y_psf = dfCsvScanId.y_psf

        raj2000 = dfCsvScanId.raj2000
        dej2000 = dfCsvScanId.dej2000

        vmag = dfCsvScanId.vmag
        vmagerr = dfCsvScanId.vmagerr
        tycho2_id = dfCsvScanId.tycho2_id
        ucac4_id = dfCsvScanId.ucac4_id

        # read DATA_FITS
        pathToFits = os.path.join('DATA_FITS', filename_scan.split('/')[-1])
        self.plate = fits.getdata(pathToFits)

        # this is for _x
        if self.mode == 0 or self.mode == 3:
            self.xexmin = np.min(dej2000)
            self.xexmax = np.max(dej2000)
            self.yexmin = np.min(raj2000)
            self.yexmax = np.max(raj2000)

        # this is for _y
        if self.mode == 1 or self.mode == 2:
            self.xexmin = np.min(raj2000)
            self.xexmax = np.max(raj2000)
            self.yexmin = np.min(dej2000)
            self.yexmax = np.max(dej2000)

        self.ixmin = np.min(x_peak)
        self.ixmax = np.max(x_peak)
        self.iymin = np.min(y_peak)
        self.iymax = np.max(y_peak)

        self.dej2000 = dej2000
        self.raj2000 = raj2000
        self.tycho2_id = tycho2_id
        self.vmag = vmag


    def displayPlate(self, param_cmap, param_aspect, param_origin):

        raoffset = 0.
        decoffset = 0.

        # print("raoffset (in minutes): ", round(raoffset * 60., 2))
        # print("decoffset (in minutes): ", round(decoffset * 60., 2))

        plate = self.plate
        figsize = plate.shape
        xsz = figsize[1]
        ysz = figsize[0]
        xsize = 7.
        ysize = int(ysz * xsize / xsz)

        # initialize figure
        fig = plt.figure(1, figsize=(xsize, ysize))

        dpx = (self.xexmin - self.xexmax) / (self.ixmax - self.ixmin)
        dpy = (self.yexmax - self.yexmin) / (self.iymax - self.iymin)
        idecoffset = int(decoffset / dpy)
        iraoffset = -int(raoffset / dpx)
        if self.mode == 0:
            plt.imshow(self.plate[self.iymin:self.iymax, self.ixmin:self.ixmax],
                       extent=(self.xexmax, self.xexmin, self.yexmax, self.yexmin), cmap=param_cmap,
                       aspect=param_aspect, origin=param_origin)
        if self.mode == 1:
            plt.imshow(self.plate[self.iymin:self.iymax, self.ixmin:self.ixmax],
                       extent=(self.xexmin, self.xexmax, self.yexmax, self.yexmin), cmap=param_cmap,
                       aspect=param_aspect, origin=param_origin)
        if self.mode == 2:
            print(idecoffset, iraoffset)
            plt.imshow(self.plate[self.iymin + idecoffset:self.iymax + idecoffset,
                       self.ixmin + iraoffset:self.ixmax + iraoffset],
                       extent=(self.xexmax, self.xexmin, self.yexmin, self.yexmax), cmap=param_cmap,
                       aspect=param_aspect, origin=param_origin)
        if self.mode == 3:
            plt.imshow(self.plate[self.iymin:self.iymax, self.ixmin:self.ixmax],
                       extent=(self.xexmax, self.xexmin, self.yexmax, self.yexmin), cmap=param_cmap,
                       aspect=param_aspect, origin=param_origin)
        plt.rcParams.update({'axes.titlesize': 'small'})
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.show(block=False)

        return fig

    def displayStars(self):
        if self.mode == 0 or self.mode == 3:
            plt.scatter(self.dej2000, self.raj2000, c='r', s=40, alpha=0.3, picker=True)
        if self.mode == 1 or self.mode == 2:
            plt.scatter(self.raj2000, self.dej2000, c='r', s=40, alpha=0.3, picker=True)

    def enableClicks(self, figure):
        figure.canvas.mpl_connect('pick_event', self.onpick)

    def onpick(self, event):
        ind = event.ind
        print('IND: ', ind[0])
        print('TYCHO2 catalog ID:', self.tycho2_id.reset_index(drop = True)[ind[0]])
        #print('RAJ2000 (hrs/mm/sss): ', self.convra(self.raj2000.reset_index(drop = True)[ind[0]]))
        #print('DEJ2000 (dgr/mm/ss): ', self.convde(self.dej2000.reset_index(drop = True)[ind[0]]))

        print('RAJ2000: ', self.raj2000.reset_index(drop = True)[ind[0]])
        print('DEJ2000: ', self.dej2000.reset_index(drop = True)[ind[0]])

        print('VMAG: ', self.vmag.reset_index(drop = True)[ind[0]])
        print('++++++++++++++')

    def convra(self, ra):
        self.dgrhrs = 15. # what ?? why 15
        self.rah = np.trunc(ra / self.dgrhrs)
        self.ram = (ra / self.dgrhrs - self.rah) * 60.
        self.ras = (self.ram - np.trunc(self.ram)) * 60.
        return self.rah[0], np.trunc(self.ram[0]), np.trunc(self.ras[0])

    def convde(self, de):
        self.ded = np.trunc(de)
        self.dem = (de - self.ded) * 60.
        self.des = (self.dem - np.trunc(self.dem)) * 60.
        return self.ded[0], np.trunc(self.dem[0]), np.trunc(self.des[0])