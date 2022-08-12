import time
import selenium
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bank_func import *


def app():
    b = Bank('username', 'password')
    b.open_site()
    b.sign_in()
    b.extract_csv_from_site()
    time.sleep(10)


    


app()
