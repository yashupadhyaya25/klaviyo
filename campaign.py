import os
import shutil
import smtplib
import time
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyotp
from azure.storage.blob import BlobServiceClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Campaign:
    
    def __init__(self, 
                 azure_account_name, 
                 azure_account_key, 
                 azure_container_name, 
                 campaign_azure_sub_folder_name,
                 campaign_local_file_path,
                 local_download_file_path,
                 kalviyo_username,
                 kalviyo_password,
                 kalviyo_secret_key,
                 gmail_sender_email,
                 gmail_receiver_email,
                 gmail_sender_password,
                 download_report_flag
                 ):
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={azure_account_name};AccountKey={azure_account_key};EndpointSuffix=core.windows.net"
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.azure_account_name = azure_account_name
        self.azure_account_key = azure_account_key
        self.azure_container_name = azure_container_name
        self.sub_folder_name = campaign_azure_sub_folder_name
        self.local_file_path = campaign_local_file_path
        self.local_download_file_path = local_download_file_path
        self.kalviyo_username = kalviyo_username
        self.kalviyo_password = kalviyo_password
        self.kalviyo_secret_key = kalviyo_secret_key
        self.gmail_sender_email = gmail_sender_email
        self.gmail_receiver_email = gmail_receiver_email
        self.gmail_sender_password = gmail_sender_password
        self.download_report_flag = download_report_flag

    def upload_blob(self, local_file_path, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.azure_container_name, blob=f"{self.sub_folder_name}/{blob_name}")

        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def send_email(self,subject, body):
        # Email configurations
        sender_email = self.gmail_sender_email
        receiver_email = self.gmail_receiver_email
        password = self.gmail_sender_password

        subject = "Klaviyo Campaign Script Execution Failed"
        body = "The Klaviyo Campaign script encountered an error."
        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())

    def download_reports(self):
        MAX_RETRIES = 2  # Number of maximum retries
        RETRY_INTERVAL = 1 * 60  # 10 minutes in seconds
        
        for attempt in range(1, MAX_RETRIES + 1): 
            try:
                if not(self.download_report_flag) :
                    # Local file path
                    local_file_path = self.local_file_path  # Replace with the actual file path
                    local_download_file_path = self.local_download_file_path # Replace with the actual file path

                    current_working_directory = os.getcwd()
                    service = Service()
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                    chrome_options.add_experimental_option("detach", True)
                    chrome_options.add_experimental_option("prefs",{
                        "download.default_directory" : current_working_directory+"\\"+local_download_file_path
                        })
                    capsolver_extension_path = current_working_directory + "/capsolver_extension"
                    chrome_options.add_argument(f"--load-extension={capsolver_extension_path}")
                    driver = webdriver.Chrome(service=service, options=chrome_options)

                    # Your existing script code here...
                    driver.get("https://www.klaviyo.com/dashboard")

                    
                    # Open the login page
                    username = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div/div/div/div[2]/div[3]/div[1]/form/div[1]/div/div[1]/div/input")
                    username.clear()
                    username.send_keys(self.kalviyo_username)
                    print("STEP-3 : Email Enter")
                    time.sleep(4)

                    password = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div/div/div/div[2]/div[3]/div[1]/form/div[2]/div/div[1]/div/input")
                    password.clear()
                    password.send_keys(self.kalviyo_password)
                    print("STEP-4 : Password Enter")
                    time.sleep(7)

                    checkmark = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div/div[2]/div[3]/div[1]/form/div[4]/div')))
                    checkmark.click()
                    print("STEP-5 : Captcha resolver")
                    time.sleep(15)

                    # Find and click the login button
                    elem = driver.find_element(By.XPATH,"//*[@id='fender-root']/div/div/div/div/div/div/div[2]/div[3]/div[1]/form/div[5]/button")
                    elem.click()
                    print("STEP-6 : Login button click")
                    time.sleep(5)

                    # Wait for the OTP field to be present (replace with actual ID of the OTP field)
                    otp_field = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div[4]/div/div[1]/div/div[1]/div/input")
                    # Generate OTP using pyotp (replace 'your_secret_key' with your actual secret key)
                    secret_key = self.kalviyo_secret_key
                    totp = pyotp.TOTP(secret_key)
                    generated_otp = totp.now()

                    # Enter the generated OTP into the OTP field
                    otp_field.clear()
                    otp_field.send_keys(generated_otp)
                    time.sleep(3)

                    # Find and click the OTP login button
                    elem = driver.find_element(By.XPATH, "//*[@id='login']")
                    elem.click()
                    time.sleep(6)

                    driver.get("https://www.klaviyo.com/analytics/reports")
                    time.sleep(5)

                    # Click on "Campaign-Sagar" hyperlink
                    hyperlink_xpath = '#AppShell-SiteBody > div > div > div > div > div > div > div > div > div > div > div.DataTable-sc-7x0ld0-0.inelmj > table > tbody > tr:nth-child(1) > td.Cell__StyledCell-sc-1gctzeb-0.iedUOx > div > div > a > span > span > div'
                    hyperlink = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, hyperlink_xpath)))
                    hyperlink.click()
                    time.sleep(5)

                    dropdown_xpath = '#AppShell-SiteBody > div > div > div.ReportBuilderPage__ReportBuilderBodyContainer-sc-1flm7kt-2.gIYoax > div.LegacyCardBase-sc-4yka2c-0.cQxvjd > form > div > div:nth-child(3) > div > div.CollapsibleContainerComponent__BodyDiv-sc-1ftmgba-2.eQTSjS > div > div > div:nth-child(5) > div > div > div > span > div'
                    dropdown = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_xpath)))

                    # Click on the dropdown to open it
                    ActionChains(driver).move_to_element(dropdown).click().perform()
                    time.sleep(2)  # Adjust the sleep time if needed

                    # Locate and click on the desired option (replace 'option_xpath' with the actual XPath)
                    option_xpath = '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/div/div[5]/div/div/div/div/div/div[9]'
                    option = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, option_xpath)))
                    option.click()
                    time.sleep(2)

                    # Save and Run Report Button
                    run = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/button/span')
                    run.click()
                    time.sleep(10)

                    # Export CSV Button
                    run = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/button')
                    run.click()
                    time.sleep(5)

                    # Get the last month's year and month
                    last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

                    # Construct the file name with the last month's year and month
                    new_file_path_last_month = os.path.join(local_file_path,f"campaign_{last_month}.csv")

                    # Move the latest downloaded file to the desired directory with the constructed file name
                    shutil.move(local_download_file_path+'/'+os.listdir(local_download_file_path)[0], new_file_path_last_month)

                    # -------------------------------------------- For Current Month --------------------------------------------------------

                    dropdown_xpath_currMon = '#AppShell-SiteBody > div > div > div.ReportBuilderPage__ReportBuilderBodyContainer-sc-1flm7kt-2.gIYoax > div.LegacyCardBase-sc-4yka2c-0.cQxvjd > form > div > div:nth-child(3) > div > div.CollapsibleContainerComponent__BodyDiv-sc-1ftmgba-2.eQTSjS > div > div > div:nth-child(5) > div > div > div > span > div'
                    dropdown1 = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_xpath_currMon)))

                    # Click on the dropdown to open it
                    ActionChains(driver).move_to_element(dropdown1).click().perform()
                    time.sleep(2)  # Adjust the sleep time if needed

                    # Locate and click on the desired option (replace 'option_xpath' with the actual XPath)
                    option_xpath1 = '/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/div/div[5]/div/div/div/div/div/div[7]/span'
                    option1 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, option_xpath1)))
                    option1.click()
                    time.sleep(2)

                    # Save and Run Report Button
                    run1 = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/div/div[2]/div/button/span')
                    run1.click()
                    time.sleep(10)

                    # Export CSV Button
                    csv1 = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/button')
                    csv1.click()
                    time.sleep(5)

                    # Get the current year and month
                    formatted_date = datetime.now().strftime("%Y-%m")

                    # Construct the file name with the current year and month
                    new_file_path_curr_month = os.path.join(local_file_path,f"campaign_{formatted_date}.csv")

                    # Move the latest downloaded file to the desired directory with the constructed file name
                    shutil.move(local_download_file_path+'/'+os.listdir(local_download_file_path)[0], new_file_path_curr_month)

                    # Upload the CSV files to Azure Blob Storage
                    for csv_file in os.listdir(local_file_path):
                        self.upload_blob(local_file_path+csv_file, csv_file)
                        os.remove(local_file_path+csv_file)

                    self.download_report_flag = True
                else :
                    break

            except Exception as e:
                print("Error in process :",e)
                # If an error occurs, send an email notification
                error_subject = "Klaviyo Campaign Script Execution Failed"
                error_body = f"The Klaviyo Campaign script encountered an error:\n\n{str(e)}"
                self.send_email(error_subject, error_body)

                if attempt < MAX_RETRIES:
                    # Wait for the specified interval before the next retry
                    print(f"Retrying in {RETRY_INTERVAL // 60} minutes...")
                    time.sleep(RETRY_INTERVAL)
                else:
                    # If maximum retries are reached, raise the exception again
                    raise

            finally:
                # Close the browser in the 'finally' block to ensure it's closed even if an exception occurs
                if 'driver' in locals():
                    driver.close()
                    driver.quit()

if __name__ == "__main__":
    pass