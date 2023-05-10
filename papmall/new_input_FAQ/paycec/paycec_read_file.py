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
from selenium.webdriver.common.by import By  # Import the By class
from selenium import webdriver
import time
from bs4 import BeautifulSoup, Tag
from typing import List
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pypandoc
import pandocfilters as pf
class PaycecReadFile:
    def __init__(self, driver:WebDriver):
        self.driver = driver
    def read_file_html(filename):
        content = ''
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print("File not found")
        return content
    
    def remove_strong_tags(match):
            return re.sub(r"<strong>(.*?)</strong>", r"\1", match.group(1))
        
    def process_faqs(filename):
        content = read_file_html(filename)
        pattern = re.compile(r"<h2>(.*?)</h2>", re.DOTALL)
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
