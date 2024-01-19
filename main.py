from modules.klaviyo.KLAVIYO import KLAVIYO
from modules.gmail.GMAIL import GMAIL

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


ENV = 'development'
sender_email = config.get(ENV,'gmail_sender_email')
receiver_email = config.get(ENV,'gmail_receiver_email')
password = config.get(ENV,'gmail_sender_password')

def main():
    ### Making GMAIL OBJECT ###
    gmail_obj = GMAIL(sender_email,receiver_email,password)
    ### Making GMAIL OBJECT ###
    
    ### DOWNLOAD ALL THE REPORT CSV ###
    klaviyo_obj = KLAVIYO(ENV)
    if not klaviyo_obj.klaviyo_webdriver.get('Flag'):
        print('Login Failed')
        gmail_obj.send_email(mail_subject='KLAVIYO LOGIN FAILED ('+klaviyo_obj.klaviyo_webdriver.get('message')+')',mail_body='There was an error while login in klaviyo ')
        quit()
    campaign_success_msg = klaviyo_obj.download_campaign_report()
    daily_success_msg = klaviyo_obj.download_daliy_report()
    flow_success_msg = klaviyo_obj.download_flow_report()
    klaviyo_obj.quit_browser()

    ### DOWNLOAD ALL THE REPORT CSV ###
    
    ### SEND MAIL IF ANY ERROR WHILE DOWNLOADING REPORTS FROM PORTAL ###
    if (campaign_success_msg.get('Flag')) :
        print('Campaign Report Success')
        gmail_obj.send_email(mail_subject='Klaviyo Campaign Script Execution Complete',mail_body='Klaviyo Campaign Report Exported Successfully and Uploaded.')
    else :
        print('Campaign Report Failed')
        gmail_obj.send_email(mail_subject='Klaviyo Campaign Script Execution Failed',mail_body='The Klaviyo Campaign script encountered an error.')
        
    if (daily_success_msg.get('Flag')) :
        print('Daily Report Success')
        gmail_obj.send_email(mail_subject='Klaviyo Daily Script Execution Complete',mail_body='The Klaviyo Daily Report Exported Successfully and Uploaded.')
    else :
        print('Daily Report Failed')
        gmail_obj.send_email(mail_subject='Klaviyo Daily Script Execution Failed',mail_body='The Klaviyo Daily script encountered an error.')
        
    if (flow_success_msg.get('Flag')) :
        print('Flow Report Success')
        gmail_obj.send_email(mail_subject='Klaviyo Flow Script Execution Complete',mail_body='The Klaviyo Flow Report Exported Successfully and Uploaded.')
    else :
        print('Flow Report Failed')
        gmail_obj.send_email(mail_subject='Klaviyo Flow Script Execution Failed',mail_body='The Klaviyo Flow script encountered an error.')
    ### SEND MAIL IF ANY ERROR WHILE DOWNLOADING REPORTS FROM PORTAL ###

if __name__ == '__main__' :
    main()