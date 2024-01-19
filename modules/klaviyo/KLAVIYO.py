from modules.klaviyo.auto_login import LOGIN
from modules.klaviyo.download_campaign_report import CAMPAIGN
from modules.klaviyo.download_daily_report import DAILY
from modules.klaviyo.download_flow_report import FLOW
from modules.azure.AZURE import AZURE

from configparser import ConfigParser
import os 
import shutil

class KLAVIYO :
    
    def __init__(self,enviroment) -> None:
            config = ConfigParser()
            config.read('config.ini')
            self.ENV = enviroment
            self.kalviyo_username = config.get(self.ENV,'kalviyo_username')
            self.kalviyo_password = config.get(self.ENV,'kalviyo_password')
            self.kalviyo_secret_key = config.get(self.ENV,'kalviyo_secret_key')
            self.campaign_local_file_path = config.get(self.ENV,'campaign_local_file_path')
            self.daily_local_file_path = config.get(self.ENV,'daily_local_file_path')
            self.flow_local_file_path = config.get(self.ENV,'flow_local_file_path')
            self.local_download_file_path = config.get(self.ENV,'local_download_file_path')
            self.azure_account_name = config.get(self.ENV,'azure_account_name')
            self.azure_account_key = config.get(self.ENV,'azure_account_key')
            self.azure_container_name = config.get(self.ENV,'azure_container_name')
            self.campaign_azure_sub_folder_name = config.get(self.ENV,'campaign_azure_sub_folder_name')
            self.daily_azure_sub_folder_name = config.get(self.ENV,'daily_azure_sub_folder_name')
            self.flow_azure_sub_folder_name = config.get(self.ENV,'flow_azure_sub_folder_name')
            shutil.rmtree(self.local_download_file_path) if os.path.exists(self.local_download_file_path) else ''
            shutil.rmtree(self.campaign_local_file_path) if os.path.exists(self.local_download_file_path) else ''
            shutil.rmtree(self.daily_local_file_path) if os.path.exists(self.local_download_file_path) else ''
            shutil.rmtree(self.flow_local_file_path) if os.path.exists(self.local_download_file_path) else ''
            os.makedirs(self.local_download_file_path,exist_ok=True)
            os.makedirs(self.campaign_local_file_path,exist_ok=True)
            os.makedirs(self.daily_local_file_path,exist_ok=True)
            os.makedirs(self.flow_local_file_path,exist_ok=True)
            self.klaviyo_webdriver = self.login()
    
    def login(self) :
            klaviyo_auto_login_obj = LOGIN(kalviyo_username = self.kalviyo_username,
                                    kalviyo_password = self.kalviyo_password,
                                    kalviyo_secret_key = self.kalviyo_secret_key,
                                    local_download_file_path = self.local_download_file_path)
            
            klaviyo_webdriver = klaviyo_auto_login_obj.login()
            return klaviyo_webdriver
    
    def get_azure_obj(self) :
        azure_obj = AZURE(account_name=self.azure_account_name,account_key=self.azure_account_key,container_name=self.azure_container_name) 
        return azure_obj

    def download_campaign_report(self) :
        try :
            campaign_obj = CAMPAIGN(self.klaviyo_webdriver.get('driver'),self.campaign_local_file_path,self.local_download_file_path)
            campaign_obj.download_last_month_report()
            campaign_obj.download_current_month_report()
            azure_obj =  self.get_azure_obj()
            blob_client =  azure_obj.get_blob_client()
            
            for report_file in os.listdir(self.campaign_local_file_path) :
                azure_obj.upload_to_blob(blob_client,self.campaign_local_file_path+report_file,report_file,self.campaign_azure_sub_folder_name)
                os.remove(self.campaign_local_file_path+report_file)
                
            return {'message' : 'Klaviyo Campaign Report Execution Success','Flag' : True}
        except :
            return {'message' : 'Klaviyo Campaign Report Execution Failed','Flag' : False}

    def download_daliy_report(self) :
        try :
            daily_obj = DAILY(self.klaviyo_webdriver.get('driver'),self.daily_local_file_path,self.local_download_file_path)
            daily_obj.download_last_month_report()
            daily_obj.download_current_month_report()
            
            azure_obj =  self.get_azure_obj()
            blob_client =  azure_obj.get_blob_client()
            
            for report_file in os.listdir(self.daily_local_file_path) :
                azure_obj.upload_to_blob(blob_client,self.daily_local_file_path+report_file,report_file,self.daily_azure_sub_folder_name)
                os.remove(self.daily_local_file_path+report_file)
                
            return {'message' : 'Klaviyo Daily Report Execution Success','Flag' : True}
        except :
            return {'message' : 'Klaviyo Daily Report Execution Failed','Flag' : False}

    def download_flow_report(self) :
        try :
            flow_obj = FLOW(self.klaviyo_webdriver.get('driver'),self.flow_local_file_path,self.local_download_file_path)
            flow_obj.download_last_month_report()
            flow_obj.download_current_month_report()
            
            azure_obj =  self.get_azure_obj()
            blob_client =  azure_obj.get_blob_client()
            
            for report_file in os.listdir(self.flow_local_file_path) :
                azure_obj.upload_to_blob(blob_client,self.flow_local_file_path+report_file,report_file,self.flow_azure_sub_folder_name)
                os.remove(self.flow_local_file_path+report_file)
            
            return {'message' : 'Klaviyo Flow Report Execution Success','Flag' : True}
        except :
            return {'message' : 'Klaviyo Flow Report Execution Failed','Flag' : False}

    def quit_browser(self) :
        self.klaviyo_webdriver.get('driver').quit()

if __name__ == '__main__' :
    pass