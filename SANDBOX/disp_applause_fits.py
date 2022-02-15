from astropy.io import fits
import matplotlib.pyplot as plt

dataplate = 'S03479_y.fits'

plate = fits.getdata('tmp/' + dataplate)

plt.imshow(plate)
plt.show()