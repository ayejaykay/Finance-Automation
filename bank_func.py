import time
import re
import selenium
import os
import gspread
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global driver
sa = gspread.service_account()
sh = sa.open("Sheet name")
wks = sh.worksheet("Tab name")
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=default/chrome/profile")
driver = uc.Chrome(executable_path='/path/to/chromedriver.exe', use_subprocess=True, options=options)

class Bank():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.date_of_last_entry = self.get_last_date()
        self.date_today = date.today()


    def sign_in(self):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(self.username)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(self.password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signInBtn"]'))).click()


    def open_site(self):
        driver.get('https://www.bank.com/')


    def extract_csv_from_site(self):
        WebDriverWait(driver, 65).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordion-section-CHECKING"]/div/div/div/div/div/bank-row[1]/div/citi-column[1]/div/bank-cta'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="timePeriodDrop"]/div'))).click()
        driver.execute_script("window.scrollTo(0, 1000)")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="timePeriodDrop-listbox"]/bank-options2[6]/div/span'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dinputRng_From"]'))).send_keys(self.date_of_last_entry)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dinputRng_End"]'))).send_keys(str(self.date_today))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="customRangeViewButton"]'))).click()

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="downloadTrans"]'))).click()
        except TimeoutException as timeout:
            print('Could not find link to download transaction')
            exit()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="exportOverlay"]/div/div[2]/div[3]/div/div/div/bank-row[1]/div/citi-column/div/bank-cta[1]'))).click()


    def get_last_date(self):
        response = wks.col_values(1)
        full_date = response[-1]
        day = re.split('/', full_date)
        day[1] = str(int(day[1]) + 1)
        return '/'.join(day)

class CSV():

    def __init__(self, file_path):
        self.file_path = file_path

    def write_to_google_sheet(self):
        with open(self.file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            with open('csv_to_write.csv', 'w') as new_file:
                fieldnames = ['Date', 'Description', 'Debit', 'Credit', 'Account', 'Category']
                csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

                for line in csv_reader:
                    del line[None]
                    del line['Status']
                    line['Account'] = 'Account Name'

                    changeDescript(line)
                    debitCredit(line)

                    wks.append_row([line['Date'], float(line['Debit']), line['Description'], line['Account'], line['Category']], value_input_option = 'USER_ENTERED')

    def delete_csv(self):
        os.remove(self.file_path)
