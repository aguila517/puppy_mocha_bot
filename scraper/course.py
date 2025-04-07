import time
import os
import mac_imessage
import smtplib

from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from userdata import config
from userdata import config_updater

class Course:
    threshold_time_obj = datetime.strptime(config.hold_tee_time['latest_tee_time'], '%H:%M').time()

    def __init__(self):
        pass

    def save_tee_time(self, filename, tee_time, delete_existing_file = False):
        tee_time_found = True
        date_string = datetime.now().strftime("%Y-%m-%d")
        filename = './log/'+filename

        if delete_existing_file and os.path.exists(filename):
            os.remove(filename)

        try:
            with open(filename, 'r+') as file:
                content = file.read()
                # Check the log is for today
                if date_string in content:
                    if tee_time not in content:
                        file.write(tee_time + '\n')
                        tee_time_found = False
                        file.close()
                # If log was for yesterday, clean up old tee times
                else:
                    # Update the date marker and remove old tee times
                    new_text = ''
                    for line in content.splitlines()[1:]:
                        try:
                            date_obj = datetime.strptime(line.split()[0], '%m-%d-%Y')
                            if date_obj.date() >= datetime.now().date():
                                new_text += line + '\n'
                        except:
                            print("DEBUG: Invalid date format {}".format(line.split()[0]))

                    file.close()
                    os.remove(filename)
                    with open(filename, 'w') as file:
                        file.write(date_string + '\n')
                        file.write(new_text)
                        if tee_time not in new_text:
                            file.write(tee_time + '\n')
                            tee_time_found = False
                        file.close()

        except FileNotFoundError:
            with open(filename, 'w') as file:
                file.write(date_string + '\n')
                file.write(tee_time + '\n')
                tee_time_found = False
                file.close()

        return tee_time_found

    def user_wants_alert(self, user_alert_setting, is_weekend, is_morning, num_players):
        send_it = False
        if user_alert_setting == 'never':
            '''
            Don't send anything to this user
            '''
            send_it = False
        elif user_alert_setting == 'few':
            '''
            Only send weekend morning times with 4 some
            '''
            if is_weekend and is_morning and num_players == 4:
                send_it = True
            
        elif user_alert_setting == 'some':
            '''
            Only send weekend morning times with any number of players
            '''
            if is_weekend and is_morning:
                send_it = True
        elif user_alert_setting == 'everything':
            '''
            Send all available morning tee times
            '''
            if is_morning:
                send_it = True
        return send_it

    def send_imsg(self, text, audience, course, is_weekend=False, is_morning=False, num_players=1):

        for contact_dict in config.user_config.items():
            contact = contact_dict[1]
            wanted_courses = contact.get('text_alert_course')
            send_it = False
            
            # If user is disabled, don't send anything except for Admins
            if contact.get('enabled') == False and contact.get('security') == 'guest':
                continue

            # If it's a Farm tee time, filter out non members.
            if course == 'farms' and contact.get('farms_member') == False:
                continue

            # Check if contact did not wnat this course to be notified.
            if course not in wanted_courses and 'all' not in wanted_courses:
                continue

            # Send every message to admin.
            if contact.get('security') == 'admin':
                send_it = True
            # Send if this contact should receive the message.
            elif 'all' in audience:
                alert_frequency = contact.get('text_alert_frequency')
                send_it = self.user_wants_alert(alert_frequency, is_weekend, is_morning, num_players)
            # Special handling for few people...
            elif contact.get('name') in audience:
                send_it = True

            if send_it:
                print('DEBUG: Sending imsg [{}] - sent to [{}]'.format(text, contact.get('name')))
                mac_imessage.send(
                    message=text,
                    phone_number=contact.get('phone'),
                    medium='iMessage'
                    )

    def click_by_xpath(self, driver, cfg_dict):
        time.sleep(1)
        WebDriverWait(driver, cfg_dict['time_out']).until(EC.presence_of_element_located((By.XPATH, cfg_dict['obj'])))
        button = driver.find_element(By.XPATH, cfg_dict['obj'])
        driver.execute_script('arguments[0].scrollIntoView();', button)
        time.sleep(1)
        
        try:
            button.click()
        except:
            driver.execute_script("arguments[0].click();", button)

    def find_tee_time(self):
        print('DEBUG: override function find_tee_time() not implemented')
        pass

    def login(self):
        print('DEBUG:override function login() not impelemented ')
        pass
