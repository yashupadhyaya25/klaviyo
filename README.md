# Klaviyo
Download Klaviyo Report like campaings, daily metric etc

****How to setup on local
**Step 1 :** First of all download the zip or clone the repo.

**Step 2 :** Unzip the file that you have downloaded from above step

**Step 3 :** Add the local path under the ‘ config.ini ’ file like this if file not present make ‘ config.ini ’ file:

    [give name as you like]
         gmail_sender_email = <gmail id>
         gmail_receiver_email = <gmail id>
         gmail_sender_password = <gmail password>
         azure_account_name = <azure_account_name>
         azure_account_key = <azure_account_key>
         azure_container_name = <azure_container_name>
         campaign_azure_sub_folder_name = <campaign_azure_sub_folder_name>
         campaign_local_file_path = <campaign_local_file_path>
         local_download_file_path = <local_download_file_path>
         kalviyo_username = <kalviyo_username>
         kalviyo_password = <kalviyo_password>
         kalviyo_secret_key = <kalviyo_secret_key>
            
**Step 4 :** Download chromedriver according to your chrome verison from ‘ https://chromedriver.chromium.org/downloads ’

**How to run**

Run main.py
