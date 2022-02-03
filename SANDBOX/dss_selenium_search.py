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

    # chromedriver for 94
    chrome_selenium_driver_location = 'C:\\Users\\mmocak\\ChromeSeleniumDriver94\\chromedriver.exe'
    tracker_login_page = 'http://archive.eso.org/dss/dss'

    # instantiate scraper
    tw = DssWebscraper(username, password, chrome_location, chrome_selenium_driver_location, tracker_login_page)

    # get logged driver - login just once
    loggedDriver = tw.seleniumLoggedDriver()

    # ra =  # in hh mm ss
    # dec = # in +/- dd mm ss
    object_name = 'm31'
    image_size_x = 50. # in arcminutes
    image_size_y = 50. # in arcminutes
    survey = 'DSS1' # DSS1,DSS2-red,DSS2-blue,DSS2-infrared
    output_format = 'download-gif' # download-gif, download-fits etc.nnn

    dssData = tw.scraper(loggedDriver, object_name,image_size_x,image_size_y, survey,output_format)  # dssData dictionary

    # close the driver after scraping
    loggedDriver.close()


# EXECUTE MAIN
if __name__ == "__main__":

    main()

# END

