from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from docs_to_html import *
from login_auto import *
from get_FAQ_links_dashboard import *
import requests

def main():
    # Load the environment variables from .env file
    load_dotenv()
    # Get the username and password from environment variables
    username = os.getenv("USERNAME1")
    password = os.getenv("PASSWORD")
    dashboard_url = 'https://www.paycec.com/dashboard/login'
    parsed_url = urlparse(dashboard_url)
    link = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    login_dashboard(username, password, dashboard_url)
    # markdown = get_google_doc_contents()
    # html = convert_to_html(markdown)
    # #  Wrapping the HTML content with a div tag
    # html = "<div id='content'>" + html + "</div>"
    # html = process_html(html)
    # # html = process_link(link, html)
    # file_name = 'file_test.txt'
    # with open(file_name, "w") as file:
    #     file.write(html)
    # faq_name = process_faqs(file_name)[0]
    # faq_content = process_faqs(file_name)[1]
    # num_of_faqs = len(process_faqs(file_name)[0])
    # faq_type = "Amex"
    # for i in range(num_of_faqs):
    #     input_faq(faq_name[i], faq_content[i], faq_type)
    num_of_faqs = 7
    get_faqs_links(num_of_faqs)
    get_dashboard_links(num_of_faqs)


if __name__ == "__main__":
    main()
