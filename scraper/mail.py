import smtplib

# Here are the email package modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from userdata import config_updater
from userdata import config
 

def send_message(subject, msg):
    credentials = config_updater.get_id_and_password('mail')
    auth = (credentials['sender'], credentials['sender_app_password'])
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    
    message = MIMEMultipart()
    message['From'] = credentials['sender']
    message['To'] = credentials['recipient']
    message['Subject'] =  subject
    
    body = MIMEText(msg, 'plain')
    message.attach(body)
    try:
        server.sendmail(credentials['sender'], credentials['recipient'], message.as_string())
    except Exception as e:
        print(e)
    server.quit()
