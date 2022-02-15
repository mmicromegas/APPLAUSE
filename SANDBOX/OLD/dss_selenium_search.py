from UTILS.DssWebscraper import DssWebscraper

from datetime import datetime
import os.path


def main():
    global splitidx, bugnote_datetime, bugnote_name

    # configuration
    username = ""
    password = ""
    chrome_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # chrome_selenium_driver_location = 'C:\\Users\\mmocak\\ChromeSeleniumDriver\\chromedriver.exe'

    # chromedriver for 97 # https://chromedriver.chromium.org/downloads
    chrome_selenium_driver_location = 'C:\\Users\\mmocak\\ChromeSeleniumDriver97\\chromedriver.exe'
    dss_archive_eso_page = 'http://archive.eso.org/dss/dss'

    # instantiate scraper
    dw = DssWebscraper(username, password, chrome_location, chrome_selenium_driver_location, dss_archive_eso_page)

    # get logged driver - login just once
    loggedDriver = dw.seleniumLoggedDriver()

    # ra =  # in hh mm ss
    # dec = # in +/- dd mm ss
    object_name = 'm31'
    image_size_x = 50. # in arcminutes
    image_size_y = 50. # in arcminutes
    survey = 'DSS1' # DSS1,DSS2-red,DSS2-blue,DSS2-infrared
    output_format = 'download-gif' # download-gif, download-fits etc.nnn

    # http: // archive.eso.org / dss / dss / image?ra = & dec = & equinox = J2000 & name = m31 & x = 5 & y = 5 & Sky - Survey = DSS1 & mime - type = download - fits & statsmode = WEBFORM
    # http: // archive.eso.org / dss / dss / image?ra = & dec = & equinox = J2000 & name = m31 & x = 5 & y = 5 & Sky - Survey = DSS1 & mime - type = download - gif & statsmode = WEBFORM

    dssData = dw.scraper(loggedDriver, object_name,image_size_x,image_size_y, survey,output_format)  # dssData dictionary

    # close the driver after scraping
    loggedDriver.close()


# EXECUTE MAIN
if __name__ == "__main__":

    main()

# END

