import time as t

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1280,720")

options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block 
    "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block 
    "profile.default_content_setting_values.geolocation": 1,          # 1:allow, 2:block 
    "profile.default_content_setting_values.notifications": 2         # 1:allow, 2:block 
  })


driver = webdriver.Chrome('./chromedriver', chrome_options=options)


def start_meeting(meeting_link):
    driver.get(meeting_link)
    
    driver.find_element_by_xpath('//*[@id="openTeamsClientInBrowser"]').click()
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="i0116"]').send_keys('ramkumar.rahul@vitap.ac.in')
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="i0118"]').send_keys('acer@8055')
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    t.sleep(2)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
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

   
def main():
    start_meeting('https://teams.microsoft.com/l/team/19%3aa53d5da6fcc342a7b78184d31681030e%40thread.tacv2/conversations?groupId=0c1415d8-a303-4996-8738-09770a03271f&tenantId=ff335ba2-bb68-489a-bbdd-f49ab4319838')        

if __name__ == "__main__":
   main()
