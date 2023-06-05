from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from docs_to_html import *
from login_auto import *
from get_FAQ_links_dashboard import *
import requests
import chardet
from update_faqs import *
def main():
    load_dotenv()
    username = os.getenv("USERNAME1")
    password = os.getenv("PASSWORD")
    dashboard_url = 'https://www.paycec.com/dashboard/login'
    parsed_url = urlparse(dashboard_url)
    link = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    login_dashboard(username, password, dashboard_url)

    #1. doc link -> file_test -> format
    def change_to_docs():
        markdown = get_google_doc_contents()
        html = convert_to_html(markdown)
        html = "<div id='content'>" + html + "</div>"
        html = process_html(html)
        file_name = 'file_test.txt'
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(html)
    #2. format file_test -> faqs
    def upload_faqs():
        file_name = 'file_test.txt'
        faq_name = process_faqs(file_name)[0]
        faq_content = process_faqs(file_name)[1]
        num_of_faqs = len(process_faqs(file_name)[0])
        faq_type = "Google Pay"
        for i in range(num_of_faqs):
            input_faq(faq_name[i], faq_content[i], faq_type)

        get_faqs_links(num_of_faqs)
        get_dashboard_links(num_of_faqs)
    # change_to_docs()
    # upload_faqs()
    # edit faq type
    faq_urls = [
        "https://www.paycec.com/dashboard/edit-article?id=2214&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2215&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2216&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2217&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2218&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2219&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2220&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2221&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2222&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2223&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2224&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2225&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2226&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2227&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2228&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2229&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2230&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2231&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2232&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2233&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2234&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2235&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2236&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2237&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2238&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2239&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2240&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2241&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2242&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2243&slcLocationCountry=GX&slcLang=en",
        "https://www.paycec.com/dashboard/edit-article?id=2244&slcLocationCountry=GX&slcLang=en"
    ]

    type_faqs_name = 'Online payment'
    old_faqs_type_name = 'Google Pay'
    change_type_faqs(faq_urls, old_faqs_type_name , type_faqs_name)
    driver.quit()

if __name__ == "__main__":
    main()
