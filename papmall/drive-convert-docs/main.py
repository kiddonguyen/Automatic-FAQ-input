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
import os
from bs4 import BeautifulSoup, Tag
from typing import List
import pypandoc
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.colab import drive


SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SERVICE_ACCOUNT_FILE = "/service_account.json"
DOCUMENT_ID = '1qlVQL01Ezad_EYNkVSQ9o3RzK6l3K7sDUhxdkjPRQmc'


def get_google_doc_contents():
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
                                    table_html += text
                        elif 'table' in content:
                            # recursive call to handle nested tables
                            table_html += get_table_html(content.get('table'))
                    table_html += '</td>'
                table_html += '</tr>\n'
            table_html += '</table>\n'
            markdown += table_html
    return markdown


def get_table_html(table):
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
                            table_html += text
                elif 'table' in content:
                    # recursive call to handle nested tables
                    table_html += get_table_html(content.get('table'))
            table_html += '</td>'
        table_html += '</tr>\n'
    table_html += '</table>\n'
    return table_html

def convert_to_html(markdown):
    html = pypandoc.convert_text(
        markdown, 'html', format='md', extra_args=['--wrap=none'])
    return html


markdown = get_google_doc_contents()
html = convert_to_html(markdown)
print(html)

# Wrapping the HTML content with a div tag
html = "<div id='content'>" + html + "</div>"

print(html)


def process_link(link: str, html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    if not a_tags:
        return html
    for a in a_tags:
        a['title'] = a.text
        a['target'] = '_blank'
        href = a['href']
        if link in href:
            a['href'] = href.replace(link, '|||LANG|||')
    element = soup.find('div', id='content')
    content_html = str(element)
    element.string.replace_with(element.text.replace('&nbsp;', ''))
    strong_tags = element.find_all('strong')
    for strong in reversed(strong_tags):
        if len(strong.contents) == 1 and strong.contents[0].name == 'strong':
            inner_strong = strong.contents[0]
            strong.replace_with(inner_strong)
    return content_html


def trim_content_and_remove_strong_tag(h2_elements: List[Tag]) -> None:
    for h2 in h2_elements:
        h2_text = h2.text.strip().replace('\s+', ' ')
        temp_elem = BeautifulSoup(h2_text, 'html.parser')
        temp_elem.strong.extract()
        h2.string.replace_with(temp_elem.text.strip())


def get_image_titles(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img')
    image_titles = [img['title'] for img in images if 'title' in img.attrs]
    return '\r\n'.join(image_titles)


link = "https://www.paycec.com"
html = process_link(link, html)
print(html)


def process_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    # Find the ol tag and extract the text from the li tag
    ol_tag = soup.find('ol')
    li_tag = ol_tag.find('li')
    li_text = li_tag.text.strip()

    # Create a new h2 tag and insert it before the ol tag
    h2_tag = soup.new_tag('h2')
    h2_tag.string = f"{ol_tag['start']}. {li_text}"
    ol_tag.insert_before(h2_tag)
    ol_tag.extract()  # Remove the ol tag

    # Add target and title attributes to all a tags
    a_tags = soup.find_all('a')
    for a in a_tags:
        a['title'] = a.text
        a['target'] = '_blank'

    # Find the content div and extract its HTML
    content_div = soup.find('div', id='content')
    content_html = str(content_div)
    return content_html


html = process_html(html)

print(html)
