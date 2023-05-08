# get dashboard + faq links
from login_auto import *

def get_faqs_title_and_slug(selector, num_of_faqs):
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

def get_faqs_links(num_of_faqs):
    cell_array = driver.find_elements(By.CSS_SELECTOR,".bootstrap-datatable > tbody > tr > td:nth-child(2)")
    title_arr, sug_title_arr = get_faqs_title_and_slug(cell_array, num_of_faqs)
    sug_title_str = '\n'.join(sug_title_arr)
    inputArray = sug_title_str.split("\n")
    for value in inputArray:
        print(f"https://www.paycec.com/faq/{value}")
def get_dashboard_links(num_of_faqs):
    # get all dashboard link faq
    edit_btn = driver.find_elements(By.CSS_SELECTOR,".btn.btn-info")
    for i in range(num_of_faqs - 1, -1, -1):
        print(edit_btn[i].get_attribute("href"))
