from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import shutil
from datetime import datetime,timedelta

class DAILY:
    def __init__(self,driver_obj,local_file_path,local_download_file_path) -> None:
        self.local_file_path = os.getcwd()+'/'+local_file_path
        self.local_download_file_path = os.getcwd()+'/'+local_download_file_path
        self.driver = driver_obj
        self.driver.get("https://www.klaviyo.com/analytics/reports")
        time.sleep(5)
    
    def download_last_month_report(self) : 
        hyperlink_xpath = '#AppShell-SiteBody > div > div > div > div > div > div > div > div > div > div > div.DataTable-sc-7x0ld0-0.inelmj > table > tbody > tr:nth-child(2) > td.Cell__StyledCell-sc-1gctzeb-0.iedUOx > div > div > a > span > span > div'
        hyperlink = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, hyperlink_xpath)))
        hyperlink.click()
        time.sleep(5)

        dropdown_xpath = '#AppShell-SiteBody > div > div > div.ReportBuilderPage__ReportBuilderBodyContainer-sc-1flm7kt-2.gIYoax > div.LegacyCardBase-sc-4yka2c-0.cQxvjd > form > div > div:nth-child(3) > div > div.CollapsibleContainerComponent__BodyDiv-sc-1ftmgba-2.eQTSjS > div > div > div:nth-child(3) > div > div:nth-child(1) > div > span > div'
        dropdown = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_xpath)))

        # Click on the dropdown to open it
        ActionChains(self.driver).move_to_element(dropdown).click().perform()
        time.sleep(2)  # Adjust the sleep time if needed

        # Locate and click on the desired option (replace 'option_xpath' with the actual XPath)
        option_xpath = '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/div/div[3]/div/div[1]/div/div/div/div[8]'
        option = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, option_xpath)))
        option.click()
        time.sleep(2)

        # Save and Run Report Button
        run = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/button/span')
        run.click()
        time.sleep(10)

        # Export CSV Button
        run = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/button')
        run.click()
        time.sleep(5)

        # Get the last month's year and month
        last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        # Construct the file name with the last month's year and month
        new_file_path_last_month = os.path.join(self.local_file_path, f"daily_{last_month}.csv")

        # Move the latest downloaded file to the desired directory with the constructed file name
        shutil.move(self.local_download_file_path + '/' +os.listdir(self.local_download_file_path)[0], new_file_path_last_month)
    
    def download_current_month_report(self) :
        dropdown_xpath_currMon = '#AppShell-SiteBody > div > div > div.ReportBuilderPage__ReportBuilderBodyContainer-sc-1flm7kt-2.gIYoax > div.LegacyCardBase-sc-4yka2c-0.cQxvjd > form > div > div:nth-child(3) > div > div.CollapsibleContainerComponent__BodyDiv-sc-1ftmgba-2.eQTSjS > div > div > div:nth-child(3) > div > div:nth-child(1) > div > span > div'
        dropdown1 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_xpath_currMon)))

        # Click on the dropdown to open it
        ActionChains(self.driver).move_to_element(dropdown1).click().perform()
        time.sleep(2)  # Adjust the sleep time if needed

        # Locate and click on the desired option (replace 'option_xpath' with the actual XPath)
        option_xpath1 = '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/div/div[3]/div/div[1]/div/div/div/div[6]'
        option1 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, option_xpath1)))
        option1.click()
        time.sleep(2)

        # Save and Run Report Button
        run1 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/button/span')
        run1.click()
        time.sleep(10)

        # Export CSV Button
        csv1 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/button')
        csv1.click()
        time.sleep(5)

        # Get the current year and month
        formatted_date = datetime.now().strftime("%Y-%m")

        # Construct the file name with the current year and month
        new_file_path_curr_month = os.path.join(self.local_file_path, f"daily_{formatted_date}.csv")

        # Move the latest downloaded file to the desired directory with the constructed file name
        shutil.move(self.local_download_file_path + '/' + os.listdir(self.local_download_file_path)[0], new_file_path_curr_month)