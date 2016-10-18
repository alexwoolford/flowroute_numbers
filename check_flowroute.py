#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import time
import os

def scrape_numbers():
    browser = webdriver.Firefox()
    browser.get('http://www.flowroute.com')
    
    loginDropdown = browser.find_element_by_partial_link_text('Login')
    loginDropdown.click()
    
    userbox = browser.find_element_by_id('id_username')
    userbox.send_keys(os.environ['FLOWROUTE_USER'])
    
    passbox = browser.find_element_by_id('id_password')
    passbox.send_keys(os.environ['FLOWROUTE_PASS'] + Keys.ENTER)
    
    time.sleep(5)
    
    browser.get('https://www.flowroute.com/accounts/dids/purchase')
    
    time.sleep(5)
    
    result = []
    
    areaCodeSelector = browser.find_element_by_id('areaCode')
    for areaCode in areaCodeSelector.find_elements_by_tag_name('option'):
        if areaCode.text in [u'303', u'720']:
            areaCode.click()
            time.sleep(2)
            prefixSelector = browser.find_element_by_id('prefix')
            for prefix in prefixSelector.find_elements_by_tag_name('option'):
                prefix.click()
                prefix.send_keys(Keys.ENTER)
                time.sleep(2)
                soup = BeautifulSoup(browser.page_source)
                for element in soup.findAll('div', {'class':'number mono mono-did'}):
                    did = element.text
                    didType = element.findParent().findParent().findAll('td')[1].find('div', {'class':'description'}).text
                    didSetup = element.findParent().findParent().findAll('td')[1].find('div', {'class':'setupFee'}).text
                    if didType != 'Standard: Standard Numbers':
                        result.append({'did':did, 'didType':didType, 'didSetup':didSetup})
    
    browser.get('https://www.flowroute.com/accounts/logout')
    
    browser.quit()
    
    return result

if __name__ == "__main__":
    for element in scrape_numbers():
        print element['did'][1:], element['didSetup'].replace('Setup Fee: ', '')


