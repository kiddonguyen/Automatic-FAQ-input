from dotenv import load_dotenv
from urllib.parse import urlparse
import os
from login_auto import *
import requests
import chardet
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def main():
    username = "admin"
    password = "RWx%d1Dye#BkYi6)Gn"
    dashboard_url = 'https://sandboxwp.dnbcgroup.com/wp-admin/'
    login_dashboard(username, password, dashboard_url)

    # Maximize the browser window
    driver.maximize_window()
    # Go to the post edit page
    driver.get('https://sandboxwp.dnbcgroup.com/wp-admin/edit.php')

    # Locate the page selector field
    time.sleep(3)
    cur_page_field = driver.find_element(By.ID, "current-page-selector")

    # Enter and submit the page number
    cur_page_field.clear()
    cur_page_field.send_keys("22")
    cur_page_field.send_keys(Keys.ENTER)

    # Find all tr elements within the tbody
    table_post = driver.find_element(By.ID, "the-list")
    tr_elements = table_post.find_elements(By.TAG_NAME, "tr")

    
    def get_blog_link():
        # Iterate over each tr element and perform actions
        blog_links = []
        
        for index, tr in enumerate(tr_elements, start=1):
            title_element = tr.find_element(By.CLASS_NAME, "row-title")
            # Get the text of the title
            title = title_element.text
            print(f"Title {index}: {title}")
            # Find the edit button within row-actions
            row_actions = tr.find_element(By.CLASS_NAME, 'row-actions')
            edit_span_element = row_actions.find_element(By.CLASS_NAME, "edit")
            a_element = edit_span_element.find_element(By.TAG_NAME, "a")

            # Get the blog link
            blog_link = a_element.get_attribute('href')
            blog_links.append(blog_link)
        return blog_links
    link_items = get_blog_link()
    for link_item in link_items:
        # Perform actions on the blog page
        driver.get(link_item)
        side_bar_setting = driver.find_element(By.ID, "custom_sidebar")
        side_bar_setting_option = side_bar_setting.find_element(
            By.ID, "2right")
        side_bar_setting_option.click()
        publish_btn = driver.find_element(By.ID, "publish")
        # Scroll to the element
        driver.execute_script("arguments[0].scrollIntoView(true);", publish_btn)
        # Click the element
        publish_btn.click()
        # Go back to the previous page
        driver.back()
        time.sleep(5)


if __name__ == "__main__":
    main()
