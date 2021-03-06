import pytest
from selenium import webdriver
import os
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import SeleniumTest
import time
from random import randint


class SeleniumTestClass:

    def _to_param(self, name, provider, closer):
        return pytest.param(provider, closer, id=name)

    def pytest_generate_tests(self, metafunc):
        if 'TRAVIS_INTEGRATION' in os.environ:
            chrome = [self._to_param('Firefox headless', _launch_headles_firefox, close_driver)]
        else:
            chrome = [self._to_param('Firefox', _launch_head_firefox, close_driver)]

        metafunc.parametrize(argnames=['get_driver', 'close_driver'], argvalues=chrome, scope="module")

def close_driver(driver):
    driver.close()

def _launch_head_firefox():
    firefox_options = Options()
    firefox_options.add_argument("--window-size=1920,1080")
    return webdriver.Firefox(firefox_options=firefox_options)

def _launch_headles_firefox():
    firefox_options = Options()
    firefox_options.add_argument("-headless")
    firefox_options.add_argument("--window-size=1920,1080")

    profile = FirefoxProfile()
    profile.set_preference('browser.cache.disk.enable', False)
    profile.set_preference('browser.cache.memory.enable', False)
    profile.set_preference('browser.cache.offline.enable', False)
    #profile.set_preference('network.cookie.cookieBehavior', 2)

    browser = webdriver.Firefox(firefox_options=firefox_options, firefox_profile=profile)
    return browser

def enter_test_mode(driver):
    driver.get('http://localhost:5000/production/testmode')


def fill_element(driver, elementname, content):
    elem = driver.find_element_by_name(elementname)
    elem.clear()
    elem.send_keys(content)

def define_kategorie(driver, kategorie_name):
    driver.get('http://127.0.0.1:5000/configuration/')
    fill_element(driver, 'neue_kategorie', kategorie_name)
    button = driver.find_element_by_id('add_kategorie')
    button.click()

def select_option(driver, option_id, item):
    el = driver.find_element_by_id(option_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text == item:
            option.click()  # select() in earlier versions of webdriver
            break

def get_options(driver, option_id):
    el = driver.find_element_by_id(option_id)
    result = []
    for option in el.find_elements_by_tag_name('option'):
        result.append(option.text)
    return result

def get_selected_option(driver, option_id):
    select = Select(driver.find_element_by_id(option_id))
    selected_option = select.first_selected_option
    return selected_option.text

def pagename(driver):
    return driver.find_element_by_id('pagetitle').get_attribute('innerHTML')

def generate_unique_name():
    return 'u' + str(time.time()).replace('.', '') + str(randint(0,10000))

def login(driver, email, passwd):
    driver.get('http://localhost/login.php')
    fill_element(driver, 'email', email)
    fill_element(driver, 'password', passwd)
    driver.find_element_by_id('btn_login').click()
    assert driver.title == 'BudgetButlerWeb - Dashboard'



