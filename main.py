import json 
import schedule
import time as t
import webbrowser
import datetime
import argparse 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1280,720")
options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block 
    "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block 
    "profile.default_content_setting_values.geolocation": 2,          # 1:allow, 2:block 
    "profile.default_content_setting_values.notifications": 2         # 1:allow, 2:block 
})

# Opening JSON file 
f = open('slots.json')
g = open('your_slots.json') 
h = open('secret.json')




driver = webdriver.Chrome('./chromedriver', chrome_options=options)

def login():

    secret = json.load(h)

    #login
    driver.get('https://teams.microsoft.com')
    
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="i0116"]').send_keys(secret['username'])
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="i0118"]').send_keys(secret['password'])
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()

def start_meeting(meeting_link, meeting_type): 
    print("Opening meeting link {}".format(meeting_link))
    
    if meeting_type == 'browser':
        webbrowser.open(meeting_link, new=2)
    elif meeting_type == 'microsoft_teams':
        
        driver.get(meeting_link)

        driver.find_element_by_xpath('//*[@id="openTeamsClientInBrowser"]').click()
        t.sleep(10)
        driver.find_element_by_xpath('//*[@id="m1589448645693"]/calling-join-button/button').click()
        t.sleep(2)

        video_toggle = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
        mic_toggle = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')

        if video_toggle.get_attribute('title') == 'Turn camera off':
            video_toggle.click()
        if mic_toggle.get_attribute('title'):  
            mic_toggle.click()
        
        t.sleep(2)
        driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button').click()
    else:
        print('Invalid Option')    
    return schedule.CancelJob    

def main():
    
    # Initialize parser 
    parser = argparse.ArgumentParser() 
    
    # Adding optional argument 
    parser.add_argument("--today", action='store_true', help = "Schedule classses today") 
    parser.add_argument("--tomorrow", action='store_true', help = "Schedule classses tomorrow") 
    
    # Read arguments from command line 
    args = parser.parse_args() 
    
    if not (args.tomorrow or args.today):
        parser.error('No action requested, add --today or --tomorrow')
    if args.tomorrow and args.today:
        parser.error('Both actions requested, add either --today or --tomorrow')
   
    today = datetime.datetime.now().strftime("%A").lower()
    tomorrow = ""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    for i in range(len(days)):
        if(today == days[i]):
            tomorrow = days[(i+1) % 7]


    
    # returns JSON object as  
    # a dictionary 
    slots = json.load(f) 
    your_slots = json.load(g)

    for your_slot in your_slots: 
        
        slot_name = your_slot['slot_name']
        course_name = your_slot['course_name']
        meeting_type = your_slot['meeting_type']
        meeting_link = your_slot['meeting_link']

        periods = slots[slot_name]

        required_day = ""
        for period in periods:
            if args.today:
                required_day = today
            if args.tomorrow:
                required_day = tomorrow
           
            day = period['day']
            time = period['time']
            if day == required_day:
                print("Scheduling {} at slot {} on {} at {}. Meeting type is {}".format(course_name, slot_name, day, time, meeting_type))
                schedule.every().day.at(time).do(start_meeting, meeting_link=meeting_link, meeting_type=meeting_type)
            
    while True: 
        # Checks whether a scheduled task  
        # is pending to run or not 
        schedule.run_pending() 
        t.sleep(58) 		
        
    # Closing file 
    f.close() 

if __name__ == "__main__":
    login()
    main()