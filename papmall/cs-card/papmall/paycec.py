import paycec.constants as const
import os

from paycec.paycec_converter import PaycecConverter
from paycec.paycec_read_file import PaycecReadFile
from paycec.paycec_optimized_images import PaycecOptimizedImages

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
class Paycec(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\bin"):
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Paycec, self).__init__(options=options)
        self.implicitly_wait(30)
        self.maximize_window()
    def land_first_page(self):
        self.get(const.BASE_URL)
    
    def login_dashboard(self):
        load_dotenv()
        USERNAME = os.getenv('USERNAME1')
        PASSWORD = os.getenv('PASSWORD')
        username_input = self.find_element(By.ID, "email")
        username_input.send_keys(USERNAME)
        password_input = self.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        submit_btn = self.find_element(By.ID, 'btn-login')
        submit_btn.click()
    
    def input_faq(self, faq_name, faq_content, faq_type):
        add_new_article = self.find_element(By.ID, "create_article")
        add_new_article.click()
        time.sleep(1)
        typeFaq = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.ID, 'slcType')))
        typeOption = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//option[contains(text(),'" + faq_type + "')]")))
        typeOption.click()
        nameFaq = self.find_element(By.ID, "txtName")
        nameFaq.send_keys(faq_name)
        time.sleep(3)
        nameFaq.send_keys(Keys.TAB)
        contentFaq = self.find_element(By.ID, "txtContent")
        contentFaq.send_keys(faq_content)
        submitForm = self.find_element(By.ID,
                                        "submit_create")
        submitForm.click()
    
    def convert_html(self):
        convert = PaycecConverter(driver=self)
        markdown = convert.get_google_doc_contents()
        html = convert.convert_to_html(markdown)
        html = "<div id='content'>" + html + "</div>"
        html = convert.process_html(html)
        file_name = 'output.txt'
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(html)
   
    def optimize_image(self, icon_img_pos):
        optimizer = PaycecOptimizedImages(driver=self)
        optimizer.save_for_web()
        file_path = 'output.txt'
        # icon_img_pos =
        with open(file_path, 'r') as file:
            contents = file.read()

        # Parse the HTML contents using BeautifulSoup
        soup = BeautifulSoup(contents, 'html.parser')

        # Extract the image titles
        image_titles = []
        for img_tag in soup.find_all('img'):
            title = img_tag.get('title')
            if title:
                image_titles.append(title)

        # Remove stopwords from the image titles and slugify
        image_titles = [slugify(optimizer.check_stopwords(title)) for title in image_titles]
        print(image_titles)

        # Get the list of image files in the img_optimized folder
        image_files = [filename for filename in os.listdir(
            'img_optimized') if filename.endswith(('.jpg', '.png', '.jpeg'))]

        # Rename the image files based on the extracted titles
        for i, filename in enumerate(image_files):
            original_title, extension = os.path.splitext(filename)
            
            if (i == icon_img_pos):
                new_title = image_titles[icon_img_pos]
                i -= 1
                print(new_title)
            else:
                new_title = image_titles[i]

            # Check if the original filename contains "-meta"
            if "-meta" in original_title:
                new_title += "-meta"

            new_filename = f"{slugify(new_title)}{extension}"
            os.rename(os.path.join('img_optimized', filename),
                    os.path.join('img_optimized', new_filename))

    def upload_faqs(self):
        uploader = PaycecReadFile(driver=self)
        faq_name = uploader.process_faqs(const.file_name)[0]
        faq_content = uploader.process_faqs(const.file_name)[1]
        num_of_faqs = len(uploader.process_faqs(const.file_name)[0])
        for i in range(num_of_faqs):
            self.input_faq(faq_name[i], faq_content[i], const.faq_type)
        uploader.get_faqs_links(num_of_faqs)
        uploader.get_dashboard_links(num_of_faqs)
    def upload_images(self):
        uploader = PaycecReadFile(driver=self)
        uploader.update_image_links('output.txt')
