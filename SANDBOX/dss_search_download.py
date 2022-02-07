# https://www.geeksforgeeks.org/downloading-files-web-using-python/

# imported the requests library
import requests

# ra =  # in hh mm ss
# dec = # in +/- dd mm ss
object_name = 'm31'
image_size_x = 20.  # in arcminutes
image_size_y = 20.  # in arcminutes
survey = 'DSS1'  # DSS1,DSS2-red,DSS2-blue,DSS2-infrared
output_format = 'download-gif'  # download-gif, download-fits etc.nnn

# get url from F12 > Network tab
image_url = "https://archive.eso.org/dss/dss/image?ra=&dec=&equinox=J2000&name={}&x={}&y={}&Sky-Survey={}&mime-type={}&statsmode=WEBFORM".format(object_name,image_size_x,image_size_y,survey,output_format)
#image_url = "http://archive.eso.org/dss/dss/image?ra=&dec=&equinox=J2000&name=m31&x=5&y=5&Sky-Survey=DSS1&mime-type=download-fits&statsmode=WEBFORM"

# URL of the image to be downloaded is defined as image_url
r = requests.get(image_url)  # create HTTP response object

# send a HTTP request to the server and save
# the HTTP response in a response object called r
with open("tmp/image.gif", 'wb') as f:
    # Saving received content as a png file in
    # binary format

    # write the contents of the response (r.content)
    # to a new file in binary mode.
    f.write(r.content)