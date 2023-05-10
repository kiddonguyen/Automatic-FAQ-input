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
class PaycecConverter:
    def __init__(self, driver:WebDriver):
        self.driver = driver
    def get_google_doc_contents(self):
        credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('docs', 'v1', credentials=credentials)
        doc = service.documents().get(documentId=DOCUMENT_ID).execute()
        content = doc.get('body').get('content')
        markdown = ''
        for element in content:
            if 'paragraph' in element:
                paragraph = element.get('paragraph')
                for run in paragraph.get('elements'):
                    if 'textRun' in run:
                        text_run = run.get('textRun')
                        text = text_run.get('content')
                        if 'textStyle' in text_run and 'link' in text_run.get('textStyle'):
                            link_url = text_run.get(
                                'textStyle').get('link').get('url')
                            markdown += f"[{text}]({link_url})" + '\n'
                        else:
                            markdown += text + '\n'
            elif 'table' in element:
                table = element.get('table')
                table_html = '<table>\n'
                for row in table.get('tableRows'):
                    table_html += '<tr>\n'
                    for cell in row.get('tableCells'):
                        table_html += '<td>'
                        for content in cell.get('content'):
                            if 'paragraph' in content:
                                for run in content.get('paragraph').get('elements'):
                                    if 'textRun' in run:
                                        text_run = run.get('textRun')
                                        text = text_run.get('content')
                                        if 'textStyle' in text_run and 'link' in text_run.get('textStyle'):
                                            link_url = text_run.get(
                                                'textStyle').get('link').get('url')
                                            table_html += f"[{text}]({link_url})"
                                        else:
                                            table_html += text
                            elif 'table' in content:
                                # recursive call to handle nested tables
                                table_html += get_table_html(content.get('table'))
                        table_html += '</td>'
                    table_html += '</tr>\n'
                table_html += '</table>\n'
                markdown += table_html
        html = pypandoc.convert_text(
        markdown, 'html', format='md')
        return html
    def process_html(self):
        html = self.get_google_doc_contents()
        soup = BeautifulSoup(html, 'html.parser')
        for ol_tag in soup.find_all('ol'):
            li_tag = ol_tag.find('li')
            li_text = li_tag.text.strip()
            start_attr = ol_tag.get('start', '1')
            type_attr = ol_tag.get('type', '1')
            h2_tag = soup.new_tag('h2')
            h2_tag.string = f"{start_attr}. {li_text}"
            ol_tag.insert_before(h2_tag)
            ol_tag.extract()
        a_tags = soup.find_all('a')
        for a in a_tags:
            a['title'] = a.text
            a['target'] = '_blank'
            a['class'] = 'text-link'
        content_div = soup.find('div', id='content')
        content_html = str(content_div)
        return content_html
        