import time
import os

from playsound import playsound
from userdata import config
from userdata import config_updater
from scraper.course import Course
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime


class Torrey(Course):
    obj_list = {'login_page': {
                    'obj': 'https://foreupsoftware.com/index.php/booking/19347/1468#/login', 
                    'wait_on': '//*[@id="bs-example-navbar-collapse-1"]/ul[1]/li[1]/a', 
                    'time_out': 15
                    },
                'tee_time_sheet': {
                    'obj': '//*[@id="bs-example-navbar-collapse-1"]/ul[1]/li[1]/a',
                    'url': 'https://foreupsoftware.com/index.php/booking/19347/1468#/teetimes',
                    'wait_on':'//*[@id="content"]/div/button[1]',
                    'time_out': 15
                    },
                '0_7_days_slot': {
                    'obj': '//*[@id="content"]/div/button[1]',
                    'wait_on': '//*[@id="schedule_select"]/option[2]',
                    'time_out': 15
                    },
                '8_90_days_slot': {
                    'obj': '//*[@id="content"]/div/button[2]',
                    'wait_on': '//*[@id="schedule_select"]/option[2]',
                    'time_out': 15
                    },
                'South': {
                    'obj': '//*[@id="schedule_select"]/option[1]',
                    'wait_on': '//*[@id="booking_class"]/div/span',
                    'time_out': 15
                    },
                'North': {
                    'obj': '//*[@id="schedule_select"]/option[2]',
                    'wait_on': '//*[@id="booking_class"]/div/span',
                    'time_out': 15
                    },
                'date': {
                    'obj': '//*[@id="date"]/div/div[1]/table/tbody/tr[{}]/td[{}]',
                    'wait_on': '//*[@id="booking_class"]/div/span',
                    'time_out': 15
                    },
                'tee_time_list': {
                    'obj': 'booking-start-time-label', 
                    'wait_on':'booking-start-time-label',
                    'time_out': 2 } }
    
    def __init__(self, driver):
        self.driver = driver
    

    def book_tee_time(self):
        success_or_not = False
        try:
            self.driver.find_element(By.XPATH, '//*[@id="book_time"]/div/div[2]/div[5]/div[1]/div/a[4]').click()
            self.driver.find_element(By.XPATH, '//*[@id="book_time"]/div/div[3]/button[1]').click()
            #TODO: If booked, save it to a file so that we don't book another tee time in the same week
            success_or_not = True
        except:
            print('DEBUG: Failed to find the "book" button...')
        return success_or_not

    def hold_tee_time(self, tee_time, not_so_encrypted_msg):
        success_or_not = False
        try:
            buttons = self.driver.find_elements(By.CLASS_NAME, Torrey.obj_list['tee_time_list']['obj'])
            for button in buttons:
                if button.text == tee_time:
                    button.click()
                    success_or_not = True
                    break
                
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="book_time"]/div/div[3]/button[1]')))
            '''
            send_imsg('Found tee time: ' + not_so_encrypted_msg + 'To book, send an email to moches.yun@gmail.com with below text as subject:')
            send_imsg('Book ' + not_so_encrypted_msg)
            if mail.check_input('Book ' + not_so_encrypted_msg):
                if book_tee_time(driver):
                    success_or_not = True
            '''
        except:
            print('DEBUG: Timer expired')
        
        return success_or_not

    def alert_tee_time(self, course, search_window='week'):
        this_month = datetime.now().month
        first_enabled_date_found = False
        week = 0
        tee_times_to_email = ''
        while week < 6:
            week += 1
            day = 0
            while day < 7:
                day += 1
                # find which day we're currently looking at
                today = self.driver.find_element(By.XPATH, Torrey.obj_list['date']['obj'].format(week, day))
                if first_enabled_date_found == False and 'disabled' in today.get_attribute('class'):
                    continue
                elif first_enabled_date_found == True and 'disabled' in today.get_attribute('class'):
                    break

                first_enabled_date_found = True

                self.driver.find_element(By.XPATH, Torrey.obj_list['date']['obj'].format(week, day)).click()
                time.sleep(0.5)
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, Torrey.obj_list['date']['wait_on'])))            

                # find which day we're currently looking at
                date = self.driver.find_element(By.ID, 'date-field')
                date_str = date.get_attribute('value')
                date_obj = datetime.strptime(date_str, '%m-%d-%Y')

                # We've moved to the next month.  Need to re-iterate the calendar again
                if date_obj.month != this_month:
                    # There's only one case where week will be in the second row
                    week = 2
                    day = 1
                    # Check if above assumption was incorrect
                    for i2 in range (1,8):
                        new_today = self.driver.find_element(By.XPATH, Torrey.obj_list['date']['obj'].format(1, i2))
                        if 'active' in new_today.get_attribute('class'):
                            week = 1
                            day = i2
                            break
                    this_month = date_obj.month

                # Allow tee time list to load
                try:
                    WebDriverWait(self.driver, Torrey.obj_list['tee_time_list']['time_out']).until(EC.presence_of_element_located((By.CLASS_NAME, Torrey.obj_list['tee_time_list']['wait_on'])))  
                except:
                    print('DEBUG: {} - {} No Tee Time'.format(course, date_str))

                # parse current html page
                html = self.driver.page_source
                soup = BeautifulSoup(html, features="html.parser")

                # get all available tee time and number of players
                tee_time_list = soup.find_all("div", {"class":"booking-start-time-label"})
                # if no tee time shown, move on to the next day
                if not tee_time_list:
                    soup.clear()
                    continue
                num_player_list = soup.find_all("span", {"class":"booking-slot-players js-booking-slot-players"})

                # save each tee time that is acceptable to book
                for tee_time, num_player in zip(tee_time_list, num_player_list):
                    text = date_str + ' [{}]'.format(date_obj.strftime("%a"))+ ' - ' + course + ': '
                    text += tee_time.text + ' ({})'.format(num_player.text.replace('\n',''))

                    tee_time_obj = datetime.strptime(tee_time.text, '%I:%M%p').time()
                    print('DEBUG: {} - {} {}'.format(course, date_str, tee_time.text))

                    if search_window == 'advanced':
                        if tee_time_obj < super().advanced_threshold_time_obj and date_obj.weekday() >= 5 and int(num_player.text) == 4:
                            tee_times_to_email += text
                    else:
                        search_days = [string.lower() for string in config.hold_tee_time['days']]
                        if tee_time_obj < super().threshold_time_obj and date_obj.strftime("%a").lower() in search_days and int(num_player.text) >= config.hold_tee_time['number_of_players']:
                            print('!!!ATTN!!!: Hold the tee time ' + date_str + ' - ' + course + ': '+ text)
                            if self.hold_tee_time(tee_time.text, date_str + ' - ' + course + ': '+ text):
                                # Alarm!
                                t_end = time.time() + 60 * 5
                                while time.time() < t_end:
                                    playsound('alarm.wav')
                            else:
                                # If holding failed, ensure 5 minutes has been elapsed before proceeding
                                time.sleep(5*30)
                        else:
                            break
                soup.clear()

        if search_window == 'advanced' and tee_times_to_email:
            super().save_tee_time(course.replace(' ','_') + '_advanced_tee_time.log', tee_times_to_email, True)

    def find_tee_time(self, search_window='week'):
        time.sleep(1)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, self.obj_list['login_page']['wait_on'])))
        #go to the tee time site
        try:
            super().click_by_xpath(self.driver, Torrey.obj_list['tee_time_sheet'])
        except:
            self.driver.get(Torrey.obj_list['tee_time_sheet']['url'])
        
        #click on residence 0-7 days tee time sheet
        if search_window == 'advanced':
            super().click_by_xpath(self.driver, Torrey.obj_list['8_90_days_slot'])
        else:
            super().click_by_xpath(self.driver, Torrey.obj_list['0_7_days_slot'])

        print('DEBUG: Searching on date: {}'.format(datetime.now()))
        # Get torrey South
        super().click_by_xpath(self.driver, Torrey.obj_list['South'])
        self.alert_tee_time('torrey south', search_window)

        self.driver.refresh()
        time.sleep(1)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, self.obj_list['login_page']['wait_on'])))
        #go to the tee time site
        try:
            super().click_by_xpath(self.driver, Torrey.obj_list['tee_time_sheet'])
        except:
            self.driver.get(Torrey.obj_list['tee_time_sheet']['url'])
        
        #click on residence 0-7 days tee time sheet
        if search_window == 'advanced':
            super().click_by_xpath(self.driver, Torrey.obj_list['8_90_days_slot'])
        else:
            super().click_by_xpath(self.driver, Torrey.obj_list['0_7_days_slot'])

        print('DEBUG: Searching on date: {}'.format(datetime.now()))

        # Get torrey North
        super().click_by_xpath(self.driver, Torrey.obj_list['North'])
        self.alert_tee_time('torrey north', search_window)
        self.driver.refresh()

    def login(self):
        # Opening the website
        self.driver.get(self.obj_list['login_page']['obj'])
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.NAME, 'username')))
        credentials = config_updater.get_id_and_password('torrey')
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        username.send_keys(credentials['user'])
        password.send_keys(credentials['password'])
        password.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, self.obj_list['login_page']['wait_on'])))

