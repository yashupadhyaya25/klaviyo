from campaign import Campaign
from configparser import ConfigParser
import os 

ENV = 'development'

config = ConfigParser()
config.read('config.ini')
gmail_sender_email = config.get(ENV,'gmail_sender_email')
gmail_receiver_email = config.get(ENV,'gmail_receiver_email')
gmail_sender_password = config.get(ENV,'gmail_sender_password')
azure_account_name = config.get(ENV,'azure_account_name')
azure_account_key = config.get(ENV,'azure_account_key')
azure_container_name = config.get(ENV,'azure_container_name')
campaign_azure_sub_folder_name = config.get(ENV,'campaign_azure_sub_folder_name')
campaign_local_file_path = config.get(ENV,'campaign_local_file_path')
local_download_file_path = config.get(ENV,'local_download_file_path')
kalviyo_username = config.get(ENV,'kalviyo_username')
kalviyo_password = config.get(ENV,'kalviyo_password')
kalviyo_secret_key = config.get(ENV,'kalviyo_secret_key')

os.makedirs(local_download_file_path,exist_ok=True)
os.makedirs(campaign_local_file_path,exist_ok=True)

def main():
    campaing_obj = Campaign(
        azure_account_name = azure_account_name, 
        azure_account_key = azure_account_key, 
        azure_container_name = azure_container_name, 
        campaign_azure_sub_folder_name = campaign_azure_sub_folder_name,
        campaign_local_file_path = campaign_local_file_path,
        local_download_file_path = local_download_file_path,
        kalviyo_username = kalviyo_username,
        kalviyo_password = kalviyo_password,
        kalviyo_secret_key = kalviyo_secret_key,
        gmail_sender_email = gmail_sender_email,
        gmail_receiver_email = gmail_receiver_email,
        gmail_sender_password = gmail_sender_password,
        download_report_flag = False
    )
    campaing_obj.download_reports()

if __name__ == '__main__' :
    main()