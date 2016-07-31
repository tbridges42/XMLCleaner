from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import selenium.webdriver.phantomjs
import time
import sys


def get_browser():
    browser = webdriver.PhantomJS()
    return browser


def get_creds():
    creds = {}
    with open("config.txt") as file:
        for line in file:
            (key, val) = [x.strip() for x in line.split('=')]
            creds[key.lower()] = val
    return creds


def login(creds, browser):
    print("Going to page...")
    browser.get(url='http://sunshine.wi.gov/MemberPages/ReportingMain.aspx')
    print("Maximizing window...")
    browser.maximize_window()
    time.sleep(4)
    try:
        print("Entering username")
        username = browser.find_element_by_id('ContentPlaceHolder1_LoginSunshine_UserName')
        print("Found log in")
        username.click()
        print("Clicked")
        username.clear()
        print("Cleared")
        username.send_keys(creds['username'])
        print("Entering password")
        browser.find_element_by_id('ContentPlaceHolder1_LoginSunshine_Password').send_keys(creds['password'])
        browser.find_element_by_id('ContentPlaceHolder1_LoginSunshine_LoginButton').click()
    except NoSuchElementException as e:
        if browser.current_url == "https://fs.wisconsin.gov/adfs/ls/":
            zscaler_login(creds, browser)
            login(creds, browser)
        else:
            raise e

# TODO: Get info from config file


def zscaler_login(creds, browser):
    print("Caught by ZScaler")
    username = browser.find_element_by_id('userNameInput')
    username.click()
    username.clear()
    username.send_keys(creds['zscalerusername'])
    print("Entered zscaler username")
    browser.find_element_by_id('passwordInput').send_keys(creds['zscalerpass'])
    print("Entered zscaler password")
    browser.find_element_by_id('submitButton').click()


def accept_purchases_on_screen(browser):
    while True:
        try:
            browser.find_element_by_id('ctl00_ContentPlaceHolder1_RadGridPurchasingApprovals_ctl00_ctl04_EditButton')\
                .click()
            time.sleep(2)
            try:
                print("Accepting a purchase")
                browser.find_element_by_id('ContentPlaceHolder1_ButtonSave').click()
                time.sleep(2)
            except NoSuchElementException:
                # If we can't find the Accept button, we will try clicking select again
                pass
        except NoSuchElementException:
            break


def accept_purchases(browser, creds):
    print("Logging in...")
    login(creds, browser)
    print(browser.title)
    time.sleep(5)
    browser.find_element_by_xpath("//*[text()='Purchase Approvals']").click()
    time.sleep(1)

    select = browser.find_element_by_xpath( "//select[@id='ContentPlaceHolder1_DropDownListPurchaseTypes']")  # get the select element
    options = select.find_elements_by_tag_name("option")  # get all the options into a list

    optionsList = []

    for option in options:  # iterate over the options, place attribute value in list
        optionsList.append(option.get_attribute("value"))

    for optionValue in optionsList:
        select = Select(browser.find_element_by_xpath("//select[@id='ContentPlaceHolder1_DropDownListPurchaseTypes']"))
        select.select_by_value(optionValue)
        time.sleep(3)
        accept_purchases_on_screen(browser)


def upload_xmls(browser, creds):
    login(creds, browser)
    time.sleep(3)
    browser.find_element_by_link_text('Enter Procurement Data')
    browser.find_element_by_link_text('AUTOMATED PURCHASE IMPORT')


def scrape(creds):
    browser = get_browser()
    accept_purchases(browser, creds)
    upload_xmls(browser, creds)


def main():
    print("Working...")
    browser = get_browser()
    print("Loading page...")
    accept_purchases(browser, get_creds())
    upload_xmls(browser, get_creds())


if __name__ == "__main__":
    main()
