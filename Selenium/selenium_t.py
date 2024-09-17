from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time



# Replace with your iDRAC IP address
idrac_ip = "xxxxx-r04esx38-idrac.xxxxx.com"

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Navigate to iDRAC login page
driver.get(f"https://{idrac_ip}")

# Find username and password fields and enter credentials
username_field = driver.find_element(By.NAME, "Username:")
password_field = driver.find_element(By.NAME, "password")

# Replace with your iDRAC username and password
username = "user"
password = "xxxxxx"

username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)


# Wait for login and any page transitions to complete
time.sleep(5)

# Navigate to the page you want to capture a screenshot of
# For example:
# driver.get("https://your_idrac_ip/#/overview")

# Capture a screenshot and save it as "screenshot.png"
screenshot_filename = "screenshot.png"
driver.save_screenshot(screenshot_filename)

# Close the browser
driver.quit()


# options = webdriver.ChromeOptions()
# options.headless = True
# driver = webdriver.Chrome(options=options)

# # Navigate to the iDRAC login page
# idrac_url = 'https:/xxx-r04esx38-idracxxx.com'
# driver.get(idrac_url)

# # Find the username and password input fields and enter your credentials
# username_field = driver.find_element("name",'Username:')  # Adjust based on actual ID
# password_field = driver.find_element("name",'Password:')  # Adjust based on actual ID

# username_field.send_keys('xxx')
# password_field.send_keys('xxx')

# # Submit the login form
# password_field.send_keys(Keys.RETURN)

# # Wait for a few seconds for the page to load and authentication to complete
# time.sleep(5)

# # Assuming you're on the iDRAC interface page, capture a screenshot
# screenshot_path = '//Users/vinoths/Desktop/SDDC Automation/Selenium/screenshot.png'
# driver.save_screenshot(screenshot_path)

# # Close the browser window
# driver.quit()
