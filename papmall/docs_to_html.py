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
# pypandoc.download_pandoc() // download pandoc from imported code
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SERVICE_ACCOUNT_FILE = "./service_account_key.json"
# Pass your copy of Google Docs link here
DOCUMENT_URL = 'https://docs.google.com/document/d/1dywOFu1tkCGlF6f_qaOQwbIqeOE6Fi3RMUUWneF9Cqo/edit'
DOCUMENT_ID = re.search(r'/document/d/([\w-]+)/', DOCUMENT_URL).group(1)


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

    # url_regex = r'(http[s]?\:\/\/[^\s]+)'
    # # Replace URLs with HTML links
    # markdown = re.sub(url_regex, r'<a href="\1">\1</a>', markdown)
    # print(markdown)
    return markdown


def convert_to_html(markdown):
    html = pypandoc.convert_text(
        markdown, 'html', format='md')
    # Replace the plain <a> tags with ones with title and target attributes
    # html = re.sub(r'<a href="(.*?)">(.*?)</a>', link_replace, html)
    return html


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


def process_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the ol tags and loop through them
    for ol_tag in soup.find_all('ol'):
        # Extract the text from the li tag
        li_tag = ol_tag.find('li')
        li_text = li_tag.text.strip()

        # Get the start attribute if it exists, or default to 1
        start_attr = ol_tag.get('start', '1')
        # Get the type attribute if it exists, or default to 1
        type_attr = ol_tag.get('type', '1')

        # Create a new h2 tag and insert it before the ol tag
        h2_tag = soup.new_tag('h2')
        h2_tag.string = f"{start_attr}. {li_text}"
        ol_tag.insert_before(h2_tag)
        ol_tag.extract()  # Remove the ol tag
    # Add target and title attributes to all a tags
    a_tags = soup.find_all('a')
    for a in a_tags:
        a['title'] = a.text
        a['target'] = '_blank'
        a['class'] = 'text-link'

    # Find the content div and extract its HTML
    content_div = soup.find('div', id='content')
    content_html = str(content_div)
    return content_html


def read_file_html(filename):
    content = ''
    try:
        with open(filename, 'r', encoding='ISO-8859-1') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found")
    return content

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
