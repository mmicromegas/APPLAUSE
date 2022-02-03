# browser automation with selenium uses selenium web driver which controls your web browser without touching it

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys
import pandas as pd

# useful stuff:
# https://towardsdatascience.com/how-to-scrape-dynamic-web-pages-with-selenium-and-beautiful-soup-fa593235981
# https://stackoverflow.com/questions/35531069/find-submit-button-in-selenium-without-id/35532972
# https://stackoverflow.com/questions/16346914/python-3-2-unicodeencodeerror-charmap-codec-cant-encode-character-u2013-i
# https://pytutorial.com/find-all-by-class-with-python-beautifulsoup#1

class DssWebscraper():
    def __init__(self, username, password, chrome_location, chrome_selenium_driver_location, tracker_login_page):

        # instantiate options
        opts = Options()

        # Headless Chrome is a way to run the Chrome browser in a headless environment without the full browser UI.
        # Headless Chrome gives you a real browser context without the memory overhead of running a full version of
        # Chrome.

        # run Chrome in headless mode
        # opts.add_argument("--headless")  # without headless your chrome will pop-up and will show nicely the automatic
        # login process

        # set the path to you browser’s location
        opts.binary_location = chrome_location

        # Set the location of the webdriver (downloaded from web)
        chrome_driver = chrome_selenium_driver_location

        # instantiate a webdriver
        driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

        # head to tracker login page
        driver.get(tracker_login_page)

        # find username field and send the username itself to the input field
        driver.find_element_by_name("username").send_keys(username)

        # find password input field and insert password as well
        driver.find_element_by_name("password").send_keys(password)

        # click Login button
        driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()

        # wait the ready state to be complete
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        # logged driver
        self.driver = driver

    def seleniumLoggedDriver(self):
        # return logged driver for main
        return self.driver

    def scraper(self, driver, object_name,image_size_x,image_size_y, survey,output_format):

        # print some message
        print('Scraping for bug {}'.format(bug_id))

        # find bug_id input field and insert it
        driver.find_element_by_name("bug_id").send_keys(bug_id)

        # click Jump button
        driver.find_element_by_xpath("//input[@type='submit' and @value='Jump']").click()

        # put the page source into a variable f and create a BeautifulSoup object from it
        f = driver.page_source
        soup = BeautifulSoup(f, 'lxml')  # we want data to be read as lxml # this requires installation of lxml package

        # dictionary for the tracker data
        trackerData = {}

        # parse data from Tracker and store them into dictionary elements
        bugId = {'bugId': bug_id}
        trackerData.update(bugId)

        title = {'title': ''}

        try:
            title = {'title': soup.title.contents[0]}
        except:
            pass
