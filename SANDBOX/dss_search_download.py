# https://www.geeksforgeeks.org/downloading-files-web-using-python/

# imported the requests library
import requests
import sys

ra = "20 23 10" # in hh mm ss
dec = "-14 14 4"   # in +/- dd mm ss
# object_name = 'm31' # if you enter object, it will over-ride the ra/dec
object_name = ""
image_size_x = 40  # in arcminutes
image_size_y = 40  # in arcminutes
survey = 'DSS1'  # DSS1,DSS2-red,DSS2-blue,DSS2-infrared
output_format = 'download-gif'  # download-gif, download-fits etc.nnn

# get url from F12 > Network tab
image_url = "https://archive.eso.org/dss/dss/image?ra={}&dec={}&equinox=J2000&name={}&x={}&y={}&Sky-Survey={}&mime-type={}&statsmode=WEBFORM".format(ra,dec,object_name,image_size_x,image_size_y,survey,output_format)
#image_url = "http://archive.eso.org/dss/dss/image?ra=&dec=&equinox=J2000&name=m31&x=5&y=5&Sky-Survey=DSS1&mime-type=download-fits&statsmode=WEBFORM"
#image_url = "http://archive.eso.org/dss/dss/image?ra=11+23+10&dec=%2B2+2+2&equinox=J2000&name=&x=5&y=5&Sky-Survey=DSS1&mime-type=download-gif&statsmode=WEBFORM" ra 11 23 10, dec +2 2 2
#image_url = "http://archive.eso.org/dss/dss/image?ra=11+23+10&dec=-3+3+3&equinox=J2000&name=&x=5&y=5&Sky-Survey=DSS1&mime-type=download-gif&statsmode=WEBFORM" ra 11 23 10, dec -3 3 3
#image_url = "http://archive.eso.org/dss/dss/image?ra=11+23+10&dec=4+4+4&equinox=J2000&name=&x=5&y=5&Sky-Survey=DSS1&mime-type=download-gif&statsmode=WEBFORM" ra 11 23 10, dec 4 4 4

# label no object
if object_name == "":
    object_name = "noobj"

# URL of the image to be downloaded is defined as image_url
try:
    r = requests.get(image_url)  # create HTTP response object
except requests.exceptions.HTTPError as e: # https://pavolkutaj.medium.com/exception-handling-of-python-requests-module-73dcdeb42aa4
    print(e, file=sys.stderr)
except requests.exceptions.RequestException as e:
    print(e, file=sys.stderr)
#except requests.exceptions.Timeout as e:
#    print("Maybe set up for a retry, or continue in a retry loop",e)
#except requests.exceptions.TooManyRedirects as e:
#    print("Tell the user their URL was bad and try a different one",e)
#except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
#    raise SystemExit(e)

# send a HTTP request to the server and save
# the HTTP response in a response object called r
filename = "tmp/dss_{}_ra_{}_dec_{}_x_{}_y_{}_{}.gif".format(object_name,ra.replace(" ","_"),dec.replace(" ","_"),image_size_x,image_size_y,survey)
with open(filename, 'wb') as f:
    # Saving received content as a file in
    # binary format

    # write the contents of the response (r.content)
    # to a new file in binary mode.
    f.write(r.content)