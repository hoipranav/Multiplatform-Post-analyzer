from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

def get_comments(url, driver):
    '''Used to scrape comments from the web'''
    driver.get(url)
    sleep(1)
    driver.execute_script("window.scrollTo(0, 7000);")
    sleep(1)
    for i in range(5):
        tags = []
        driver.execute_script("window.scrollTo(0, 1000000);")
        for i in driver.find_elements(By.XPATH, '//*[@id="content-text"]/span'):
            tags.append(i.text)
        sleep(0.1)
    return tags

def scrape_platform(url):
    '''Set up Selenium & virtual display for automation'''
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    tags = get_comments("https://www.youtube.com/watch?v=3OUdeW4HmgE&list=RD3OUdeW4HmgE&start_radio=1", driver)
    driver.quit()
    display.stop()
    return tags
