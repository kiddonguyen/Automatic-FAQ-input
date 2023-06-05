from dotenv import load_dotenv
from urllib.parse import urlparse
import os
from login_auto import *
import requests
import chardet
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import re

def main():
    username = "thanhnguyen@mobcec.com"
    password = "0967614208nN@"
    dashboard_url = 'https://backoffice.papmall.com'
    login_dashboard(username, password, dashboard_url)
    # Maximize the browser window
    driver.maximize_window()
    driver.get('https://backoffice.papmall.com/common/papmall_faq_article')

    # Locate the page selector field
    time.sleep(3)
    def read_file_html(filename):
        content = ''
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print("File not found")
        return content
    def input_faq(faq_name, faq_content, faq_order):
        # cur_page_field = driver.find_element(By.ID, "current-page-selector")
        add_faq_btn = driver.find_element(By.ID, "add_jqGrid")
        add_faq_btn.click()
        time.sleep(3)
        # Find the select2-faq_pap_category_id-container element and click on it
        container_element = driver.find_element(
            By.ID, 'select2-faq_pap_category_id-container')
        container_element.click()

        # input_element = driver.find_element(By.CSS_SELECTOR, '.select2-search__field')
        # input_element.clear()
        # input_element.send_keys('test')
        # input_element.send_keys(Keys.RETURN)

        # Find the select element
        select_element = driver.find_element(By.ID, 'faq_type_id')

        # Create a Select object
        select = Select(select_element)

        # Select the desired option by its visible partial text
        desired_text = "Family & Genealogy"
        options = select.options
        for option in options:
            if desired_text in option.text:
                select.select_by_visible_text(option.text)
                break
        faq_name_input = select_element = driver.find_element(By.ID, 'faq_name')
        faq_name_input.send_keys(faq_name)
        time.sleep(3)
        sourceBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.cke_button.cke_button__source')))
        sourceBtn.click()
        time.sleep(3)
        # # Locate the textarea element by its class name
        faqContentTextarea = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'cke_source')))
        
        # Send keys to the textarea element
        faqContentTextarea.send_keys(faq_content)
        faqOrderInput = driver.find_element(By.ID, "faq_order")
        faqOrderInput.send_keys(faq_order + 1)
        faqActiveInput = driver.find_element(By.ID, 'faq_active')

        # Find the radio button element with value="Y" using XPath
        radio_button = faqActiveInput.find_element(By.XPATH,
                                                '//input[@type="radio" and @value="Y"]')

        # Click the radio button to select it
        radio_button.click()
        submit_btn = driver.find_element(By.ID, "sData")
        submit_btn.click()
        # Wait for 3 seconds
        time.sleep(5)

    def process_faqs(filename):
        content = read_file_html(filename)
        # Regular expression to match content inside <h2></h2> tags, including newlines
        pattern = re.compile(r"<h2>(.*?)</h2>", re.DOTALL)
        # Remove all <strong> tags inside <h2> tags

        def remove_strong_tags(match):
            return re.sub(r"<strong>(.*?)</strong>", r"\1", match.group(1))
        # List comprehension to extract content inside <h2> tags and remove <strong> tags
        h2_list = [remove_strong_tags(match)
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
    def upload_faqs():
        file_name = 'file_test.txt'
        faq_name = process_faqs(file_name)[0]
        faq_content = process_faqs(file_name)[1]
        num_of_faqs = len(process_faqs(file_name)[0])
        # print(faq_content)
        for i in range(num_of_faqs):
            input_faq(faq_name[i], faq_content[i], i)
    upload_faqs()


if __name__ == "__main__":
    main()
