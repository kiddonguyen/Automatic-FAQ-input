#This file will include a class with instance methods.
#That will be responsible to interact convert
#HTML from google docs file and output into text file.
from selenium.webdriver.remote.webdriver import WebDriver
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup
from tkinter import Tk
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from bs4 import BeautifulSoup, Tag
from typing import List
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pypandoc
import pandocfilters as pf
import os
from slugify import slugify
from difflib import SequenceMatcher
class PaycecReadFile:
    def __init__(self, driver:WebDriver):
        super().__init__()
        self.driver = driver
    def read_file_html(self, filename):
        content = ''
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print("File not found")
        return content
    
    def remove_strong_tags(self, match):
            return re.sub(r"<strong>(.*?)</strong>", r"\1", match.group(1))
        
    def process_faqs(self, filename):
        content = self.read_file_html(filename)
        pattern = re.compile(r"<h2>(.*?)</h2>", re.DOTALL)
        h2_list = [self.remove_strong_tags(match)
                for match in pattern.finditer(content)]
        # List comprehension to split the string into two lists: content inside and outside <h2> tags
        non_h2_list = [item.strip()
                    for item in re.split(pattern, content) if item.strip()]
        # Remove duplicate whitespace and newline characters from both lists
        h2_list = [' '.join(item.split()) for item in h2_list]
        non_h2_list = [' '.join(item.split()) for item in non_h2_list]
        # Remove the first item from non_h2_list (it should be empty due to leading <h2> tag)
        non_h2_list = non_h2_list[1:]
        # Remove items from non_h2_list that match any items in h2_list
        non_h2_list = [x for x in non_h2_list if x not in h2_list]
        # Remove sequence numbers from h2_list
        h2_list = [item.split('. ')[-1] for item in h2_list]
        return h2_list, non_h2_list


    def get_faqs_links(self, num_of_faqs):
        cell_array = driver.find_elements(
            By.CSS_SELECTOR, ".bootstrap-datatable > tbody > tr > td:nth-child(2)")
        title_arr, sug_title_arr = get_faqs_title_and_slug(
            cell_array, num_of_faqs)
        sug_title_str = '\n'.join(sug_title_arr)
        inputArray = sug_title_str.split("\n")
        for value in inputArray:
            print(f"https://www.paycec.com/faq/{value}")


    def get_dashboard_links(self, num_of_faqs):
        # get all dashboard link faq
        edit_btn = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-info")
        for i in range(num_of_faqs - 1, -1, -1):
            print(edit_btn[i].get_attribute("href"))

    # def upload_files(self):
    #     self.driver.get('https://www.paycec.com/dashboard/cloud-upload')
    #     file_input = self.driver.find_element(By.ID, 'upload-files')
    #     # Get the list of image files from the "img_optimized" folder
    #     image_files = [filename for filename in os.listdir(
    #         'img_optimized') if filename.endswith(('.jpg', '.png', '.jpeg'))]

    #     # Upload files
    #     for file_name in image_files:
    #         file_path = os.path.abspath(os.path.join('img_optimized', file_name))
    #         file_input.send_keys(file_path)

    #     # Submit the form
    #     upload_button = self.driver.find_element(By.CLASS_NAME, 'btn-primary')
    #     upload_button.click()

    #     # Wait for the upload to complete and check the success message
    #     success_message_locator = (By.ID, 'order-form-message')
    #     WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
    #         success_message_locator, 'All files are uploaded successfully!'))

    #     print('Files uploaded successfully!')

    #     # Extract the href values from the uploaded images
    #     uploaded_image_links = []
    #     success_message_divs = self.driver.find_elements(
    #         By.CLASS_NAME, 'alert-success')
    #     for success_message_div in success_message_divs:
    #         soup = BeautifulSoup(success_message_div.get_attribute(
    #             'innerHTML'), 'html.parser')
    #         link_tags = soup.find_all('a')
    #         for link_tag in link_tags:
    #             href = link_tag['href']
    #             uploaded_image_links.append(href)

    #     # Print the uploaded image links
    #     print('Uploaded Image Links:')
    #     for link in uploaded_image_links:
    #         if '-meta' not in link:
    #             print(link)
    #     return uploaded_image_links

    def update_image_links(self, output_file):
        content = self.read_file_html(output_file)
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        # uploaded_image_links = self.upload_files()
        uploaded_image_links = [
            'https://d31sr5l700dp6b.cloudfront.net/uploads/what-type-of-saudi-e-visa-for-canadian-citizens-1678355058.jpg',
            'https://d31sr5l700dp6b.cloudfront.net/uploads/what1-type-of-saudi-e-visa-for-canadian-citizens-meta-1678355058.jpg',
            'https://d31sr5l700dp6b.cloudfront.net/uploads/get-saudi-e-visa-from-canada-with-simple-steps-1678355057.jpg',
            'https://d31sr5l700dp6b.cloudfront.net/uploads/how-much-saudi-e-visa-price-for-canadian-citizens-1678355058.jpg',
        ]
        def find_longest_common_substring(str1, str2):
            matcher = SequenceMatcher(None, str1, str2)
            match = matcher.find_longest_match(0, len(str1), 0, len(str2))
            longest_substring = str1[match.a: match.a + match.size]
            return longest_substring
        for img_tag in img_tags:
            title = img_tag.get('title')
            if title:
                slugified_title = slugify(title)
                longest_substring = ''
                matching_link = None
                for link in uploaded_image_links and '-meta' not in link:
                    print(link)
                    current_substring = find_longest_common_substring(
                        link, slugified_title)
                    if len(current_substring) > len(longest_substring):
                        longest_substring = current_substring
                        matching_link = link

                if matching_link is not None:
                    img_tag['src'] = matching_link

        updated_content = soup.prettify()
        with open('output.txt', 'w') as file:
            file.write(updated_content)
