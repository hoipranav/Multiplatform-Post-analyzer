from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

def scrape_platform():
    '''Scrape all the required data from the Paltform Post/Video'''
    # display = Display(visible=0, size=(800, 600))
    # display.start()
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://www.youtube.com/watch?v=3OUdeW4HmgE&list=RD3OUdeW4HmgE&start_radio=1")
    sleep(3)

    driver.execute_script("window.scrollTo(0, 400);")

    for i in range(5):
        sleep(3)
        driver.execute_script("window.scrollTo(0, 10000);")
    sleep(3)

    driver.quit()

scrape_platform()
