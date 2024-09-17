# import time
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By



options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

URL = 'https://sxxxxx-r04esx38-idrac.xxxx.com/'

driver.get(URL)

driver.save_screenshot("/Users/vinoths/Desktop/SDDC Automation/Selenium/ss.jpg")
driver.find_element(By.XPATH, "/html/body").click()


driver.quit()
