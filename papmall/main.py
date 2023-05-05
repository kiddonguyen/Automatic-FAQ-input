from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from docs_to_html import *
from login_auto import *


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
    # get dashboard + faq links
    cell_array = driver.find_elements(By.CSS_SELECTOR,".bootstrap-datatable > tbody > tr > td:nth-child(2)")
    def get_faqs_title_and_slug(selector):
        cell_title_array = []
        cell_title_slug_array = []
        for i in range(num_of_faqs):
            cell_item = selector[i].text
            cell_item_array = cell_item.split("\n")
            cell_title = cell_item_array[0]
            cell_title_slug = cell_item_array[1]
            cell_title_array.append(cell_title)
            cell_title_slug_array.append(cell_title_slug)
        cell_title_array_result = cell_title_array[::-1]
        cell_title_slug_array_result = cell_title_slug_array[::-1]
        return [cell_title_array_result, cell_title_slug_array_result]

    title_arr, sug_title_arr = get_faqs_title_and_slug(cell_array)
    # Make a GET request to the webpage
    response = requests.get(dashboard_url)
    # Create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in sug_title_arr:
        print(item)
    for item in sug_title_arr:
        print(item)
    sug_title_str = '\n'.join(sug_title_arr)
    print(sug_title_str)
    inputArray = sug_title_str.split("\n")
    for value in inputArray:
        print(f"https://www.paycec.com/faq/{value}")
    # get all dashboard link faq
    btn = soup.select(".btn.btn-info")
    for i in range(num_of_faqs - 1, -1, -1):
        print(btn[i]['href'])



if __name__ == "__main__":
    main()
