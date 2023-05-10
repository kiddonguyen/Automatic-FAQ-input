import paycec.constants as const
from paycec.paycec_converter import PaycecConverter
import os
from paycec.paycec_optimized_images import PaycecOptimizedImages
from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from prettytable import PrettyTable
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
class Paycec(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\bin"):
        self.driver_path = driver_path
        # self.teardown = teardowns
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Paycec, self).__init__(options=options)
        self.implicitly_wait(30)
        self.maximize_window()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if self.teardown:
    #         self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
    
    def login_dashboard(self):
        load_dotenv()
        # USERNAME = os.getenv('USERNAME')
        USERNAME = 'thanhnguyen@mobcec.com'
        PASSWORD = os.getenv('PASSWORD')
        username_input = self.find_element(By.ID, "email")
        username_input.send_keys(USERNAME)
        password_input = self.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        submit_btn = self.find_element(By.ID, 'btn-login')
        submit_btn.click()
    
    def input_faq(faq_name, faq_content, faq_type):
        add_new_article = driver.find_element(By.ID, "create_article")
        add_new_article.click()
        time.sleep(1)
        typeFaq = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'slcType')))
        typeOption = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//option[contains(text(),'" + faq_type + "')]")))
        typeOption.click()
        nameFaq = driver.find_element(By.ID, "txtName")
        nameFaq.send_keys(faq_name)
        time.sleep(3)
        nameFaq.send_keys(Keys.TAB)
        contentFaq = driver.find_element(By.ID, "txtContent")
        contentFaq.send_keys(faq_content)
        submitForm = driver.find_element(By.ID,
                                        "submit_create")
        submitForm.click()
    
    def convert_html(self):
        convert = PaycecConverter(driver=self)
        convert.process_html()
    def optimize_image(self):
        optimizer = PaycecOptimizedImages(driver=self)
        optimizer.save_for_web()
