import paycec.constants as const
import os

# from paycec.paycec_converter import PaycecConverter
from paycec.paycec_read_file import PaycecReadFile
# from paycec.paycec_optimized_images import PaycecOptimizedImages

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from urllib.parse import urlparse
import time
from bs4 import BeautifulSoup
from slugify import slugify
from selenium.webdriver.common.action_chains import ActionChains
# Open an incognito window
class Paycec(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\bin"):
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Paycec, self).__init__(options=options)
        self.implicitly_wait(30)
        self.maximize_window()
    
    
    def land_first_page(self):
        self.get(const.BASE_URL)
    def login_dashboard(self):
        load_dotenv()
        USERNAME = os.getenv('USERNAME1')
        PASSWORD = os.getenv('PASSWORD')
        # Select and input username and password
        username_input = self.find_element(By.ID, "username")
        username_input.send_keys(USERNAME)
        password_input = self.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        submit_btn = self.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        submit_btn.click()
    def redirect_blog(self):
        self.get(const.BLOG_URL)
    def add_blog_post(self):
        # Click add new blog post button
        add_blog_btn = self.find_element(By.CSS_SELECTOR, '.btn.cm-tooltip')
        add_blog_btn.click()
        # Wait for the <div> element to be present before interacting with it
        blog_parent_type_add = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pages_information_setting .choose-icon'))
        )
        # Find the <a> tag inside the <div> element
        blog_parent_type_add_btn = blog_parent_type_add.find_element(By.CSS_SELECTOR, '.add-on')
        # Click the <a> tag
        blog_parent_type_add_btn.click()
        # Wait for the input element to be present before interacting with it
        blog_search_type = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="text" and @name="q" and @size="20"]'))
        )
        # Once the input element is present, input the value "News"
        blog_search_type.send_keys(const.BLOG_SEARCH_TYPE_VALUE)
        blog_search_type_submit = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"][name="dispatch[pages.picker]"][value="Search"]'))
        )
        # Once the input element is clickable, click it
        blog_search_type_submit.click()
        time.sleep(3)
        # Wait for the radio input to be clickable before interacting with it
        blog_search_type_radio_input = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//table[1]//tr[1]//td[1]//input[@type="radio"]'))
        )
        # Once the radio input is clickable, click it
        blog_search_type_radio_input.click()
        time.sleep(3)
        actions = ActionChains(self)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(3)
        blog_name_input = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.ID, "elm_page_name"))
        )
        
        blog_name_input.send_keys(const.BLOG_NAME_INPUT_VALUE)
        # Input the blog description field
        blog_desc_input = self.find_element(By.ID, "elm_page_descr")
        blog_desc_input.send_keys(const.BLOG_DESC_VALUE)
        # Input the blog page title field
        blog_title_input = self.find_element(By.ID, "elm_page_title")
        blog_title_input.send_keys(const.BLOG_NAME_INPUT_VALUE)
        # Input the blog page meta description field
        blog_meta_desc_input = self.find_element(By.ID, "elm_page_meta_descr")
        blog_meta_desc_input.send_keys(const.BLOG_META_DESC_INPUT_VALUE)
        self.execute_script("window.scrollTo(0, 0);")
        track_tabs_list = self.find_element(By.CSS_SELECTOR, '.cm-track .nav.nav-tabs')
        # Find the li#addons element within ul_list and click it
        addons_element = track_tabs_list.find_element(By.CSS_SELECTOR, '#addons>a')
        addons_element.click()
        blog_image_btn = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="btn" and @onclick="Tygh.fileuploader.show_loader(this.id);" and contains(text(), "URL")]'))
        )
        # Once the element is present, you can interact with it
        blog_image_btn.click()  # For example, click the element
        # Wait for the alert to be present
        blog_image_alert = WebDriverWait(self, 10).until(EC.alert_is_present())
        # Switch to the alert
        # Assuming the alert has an input field, wait for it to be present
        blog_image_alert.send_keys(const.BLOG_IMAGE_ALERT_VALUE)
        # Submit the alert
        blog_image_alert.accept()
        blog_image_alt = self.find_element(By.ID, "alt_icon_blog_image_0")
        blog_image_alt.send_keys(const.BLOG_NAME_INPUT_VALUE)
        blog_seo_name = self.find_element(By.ID, "elm_seo_name")
        blog_seo_name.send_keys(const.BLOG_NAME_INPUT_VALUE)
        # Adjust timeout and other parameters as needed
        blog_create_button = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-ca-dispatch="dispatch[pages.update]" and @data-ca-target-form="page_update_form" and @class="btn btn-primary cm-submit btn-primary "]'))
        )
        # Once the element is present, click it
        blog_create_button.click()
        print(f"{const.BLOG_NAME_INPUT_VALUE} page created successfully!")
    def input_faq(self, faq_name, faq_content, faq_type):
        # add_new_article = self.find_element(By.ID, "create_article")
        # add_new_article.click()
        # time.sleep(1)
        # typeFaq = WebDriverWait(self, 10).until(
        #     EC.visibility_of_element_located((By.ID, 'slcType')))
        # typeOption = WebDriverWait(self, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, "//option[contains(text(),'" + faq_type + "')]")))
        # typeOption.click()
        # nameFaq = self.find_element(By.ID, "txtName")
        # nameFaq.send_keys(faq_name)
        # time.sleep(3)
        # nameFaq.send_keys(Keys.TAB)
        # contentFaq = self.find_element(By.ID, "txtContent")
        # contentFaq.send_keys(faq_content)
        # submitForm = self.find_element(By.ID,
        #                                 "submit_create")
        # submitForm.click()
        print("input_faq")
    def upload_faqs(self):
        
        uploader = PaycecReadFile(driver=self)
        # faq_name = uploader.process_faqs(const.file_name)[0]
        # faq_content = uploader.process_faqs(const.file_name)[1]
        # num_of_faqs = len(uploader.process_faqs(const.file_name)[0])
        # for i in range(num_of_faqs):
        #     self.input_faq(faq_name[i], faq_content[i], const.faq_type)
        # uploader.get_faqs_links(num_of_faqs)
        # uploader.get_dashboard_links(num_of_faqs)
