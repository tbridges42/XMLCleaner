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
import time


def get_browser():
    profile = FirefoxProfile()
    browser = webdriver.Firefox(firefox_profile=profile)
    return browser


def get_creds():
    creds = {}
    with open("config.txt") as file:
        for line in file:
            (key, val) = [x.strip() for x in line.split('=')]
            creds[key.lower()] = val
    return creds


def login(creds, browser):
    browser.get('http://sunshine.wi.gov/MemberPages/ReportingMain.aspx')
    browser.maximize_window()
    time.sleep(4)
    try:
        username = browser.find_element_by_id('ContentPlaceHolder1_LoginSunshine_UserName')
        username.click()
        username.clear()
        username.send_keys(creds['username'])
        browser.find_element_by_id('ContentPlaceHolder1_LoginSunshine_Password').send_keys(creds['password'])
        browser.find_element_by_id('ContentPlaceHolder1_LoginSunshine_LoginButton').click()
    except NoSuchElementException as e:
        if browser.current_url == "https://fs.wisconsin.gov/adfs/ls/":
            zscaler_login(browser)
            login(creds, browser)
        else:
            raise e

# TODO: Get info from config file


def zscaler_login(browser):
    username = browser.find_element_by_id('userNameInput')
    username.click()
    username.clear()
    username.send_keys('blah')
    browser.find_element_by_id('passwordInput').send_keys('blah')
    browser.find_element_by_id('submitButton').click()


def accept_purchases_on_screen(browser):
    while True:
        try:
            browser.find_element_by_id('ctl00_ContentPlaceHolder1_RadGridPurchasingApprovals_ctl00_ctl04_EditButton')\
                .click()
            time.sleep(2)
            try:
                browser.find_element_by_id('ContentPlaceHolder1_ButtonSave').click()
                time.sleep(2)
            except NoSuchElementException:
                # If we can't find the Accept button, we will try clicking select again
                pass
        except NoSuchElementException:
            break


def accept_purchases(browser):
    login(get_creds(), browser)
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


def upload_xmls(browser):
    login(get_creds(), browser)
    time.sleep(3)
    browser.find_element_by_link_text('Enter Procurement Data')
    browser.find_element_by_link_text('AUTOMATED PURCHASE IMPORT')


def main():
    browser = get_browser()
    accept_purchases(browser)
    upload_xmls(browser)


if __name__ == "__main__":
    main()
