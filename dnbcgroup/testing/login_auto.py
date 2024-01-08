import os
from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time

# test from here
from selenium.webdriver.common.action_chains import ActionChains


# Get the screen width using the Tkinter module
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("Chrome/111.0.0.0")
# Set the option to keep the browser window open after the driver is closed
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# Create a Service object with the path to the ChromeDriver executable
chrome_driver_path = os.path.abspath("C:/bin/chromedriver.exe")
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


def login_dashboard(username, password, dashboard_url):
    # Navigate to the login page
    driver.get(dashboard_url)
    # Find the username and password fields and enter your login information
    username_field = driver.find_element(By.ID, "user_login")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "user_pass")
    password_field.send_keys(password)
    # Submit the login form
    time.sleep(3)
    submit_button = driver.find_element(By.ID, "wp-submit")
    # submit_button = driver.find_element(By.CLASS_NAME, "submit")
    # submit_button = driver.find_element(By.ID, "btn-login")
    submit_button.click()
    # input_article_name, src_textarea_content
