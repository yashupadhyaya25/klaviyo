from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import pyotp

class LOGIN :
    def __init__(self,kalviyo_username,kalviyo_password,kalviyo_secret_key,local_download_file_path) :
        self.kalviyo_username = kalviyo_username
        self.kalviyo_password = kalviyo_password
        self.kalviyo_secret_key = kalviyo_secret_key
        self.local_download_file_path = local_download_file_path
        self.msg = ''

    def login(self) :
        try :
            local_download_file_path = self.local_download_file_path
            
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
            driver.get("https://www.klaviyo.com/login")
            
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
            
            # Checking that login is succesfull or not 
            try :
                account_switch_key = driver.find_element(By.ID,"account-switcher-toggle")
                account_switch_key.click()
                self.msg = 'Login Success'
                return {'message' : self.msg,'Flag' : True,'driver' : driver}
            except :
                self.msg = 'Login Failed as OTP is incorrect'
                driver.quit()
                return {'message' : self.msg,'Flag' : False}
        except :
            self.msg = 'Login Failed'
            driver.quit()
            return {'message' : self.msg,'Flag' : False}

if __name__ == '__main__' :
    pass