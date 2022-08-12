import time
import selenium
import os
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global driver
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=path")
driver = uc.Chrome(executable_path='path', use_subprocess=True, options=options)

class Bank():

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def sign_in(self):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(self.username)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(self.password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signInBtn"]'))).click()


    def open_site(self):
        driver.get('url')


    def extract_csv_from_site(self):
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordion-section-CHECKING"]/div/div/div/div/div/citi-row[1]/div/citi-column[1]/div/citi-cta'))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="timePeriodDrop"]/div'))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="timePeriodDrop-listbox"]/citi-options2[6]/div')))


class CSV():

    def __init__(self, file_path):
        self.file_path = file_path

    def delete_csv(self):
        os.delete(self.file_path)
