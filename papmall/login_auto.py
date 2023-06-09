import os
from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time
# Get the screen width using the Tkinter module
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("Chrome/111.0.0.0")
# Set the option to keep the browser window open after the driver is closed
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# Create a Service object with the path to the ChromeDriver executable
chrome_driver_path = os.path.abspath("C:/bin/chromedriver.exe")
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def login_dashboard(username, password, dashboard_url):
    # Navigate to the login page
    driver.get(dashboard_url)
    # Find the username and password fields and enter your login information
    username_field = driver.find_element(By.ID, "email")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    # Submit the login form
    time.sleep(3)
    # submit_button = driver.find_element(By.ID, "btn-login")
    # submit_button = driver.find_element(By.CLASS_NAME, "submit")
    submit_button = driver.find_element(By.ID, "btn-login")
    submit_button.click()
    # input_article_name, src_textarea_content


def input_faq(faq_name, faq_content, faq_type):
    add_new_article = driver.find_element(By.ID, "create_article")
    add_new_article.click()
    time.sleep(1)
    # Locate the dropdown menu element
    typeFaq = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'slcType')))
    # find the option with visible text containing "Google Pay"
    # typeOption = typeFaq.find_element(
    #     By.XPATH, "//option[contains(text(),'" + faq_type + "')]")
    typeOption = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//option[contains(text(),'" + faq_type + "')]")))
    typeOption.click()
    nameFaq = driver.find_element(By.ID, "txtName")
    # name
    nameFaq.send_keys(faq_name)
    time.sleep(3)
    nameFaq.send_keys(Keys.TAB)
    contentFaq = driver.find_element(By.ID, "txtContent")
    contentFaq.send_keys(faq_content)

    submitForm = driver.find_element(By.ID,
                                     "submit_create")
    submitForm.click()


def input_faq_papmall(faq_name, faq_content, faq_order):
    add_new_article = driver.find_element(
        By.CLASS_NAME, "ui-icon.ui-icon-plus")
    add_new_article.click()
    time.sleep(1)
    # papCategoryID = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.ID, 'faq_pap_category_id')))
    # papCategoryID = driver.find_element(By.ID, "faq_pap_category_id")
    # papCategoryID.select_by_visible_text('AR Filters')
    papCategoryID = driver.find_element(
        By.CSS_SELECTOR, '#faq_pap_category_id + .select2')
    papCategoryID.click()
    wait = WebDriverWait(driver, 3)
    papCategoryIDSearchField = driver.find_element(
        By.CLASS_NAME, "select2-search__field")
    papCategoryIDSearchField.send_keys('AR Filters')
    papCategoryIDSearchField.send_keys(Keys.ENTER)

    nameFaq = driver.find_element(By.ID, "faq_name")
    nameFaq.send_keys(faq_name)
    time.sleep(3)
    nameFaq.send_keys(Keys.TAB)
    # todo: input content into the content iframe file, choose the order from 1 => 6 for each the input
    # question by order and choose faq active = 'active' => click submit button
    sourceBtn = driver.find_element(By.ID, "cke_35")
    sourceBtn.click()
    # Locate the textarea element by its class name
    faqContentTextarea = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'cke_source')))
    # Send keys to the textarea element
    faqContentTextarea.send_keys(faq_content)
    faqOrderInput = driver.find_element(By.ID, "faq_order")
    faqOrderInput.send_keys(faq_order)
    # Locate the span element by its ID
    faq_active_span = driver.find_element(By.ID, "faq_active")
    # Locate the input element with ID "active" under the faq_active_span
    active_input_element = faq_active_span.find_element(By.ID, "active")
    # Click on the active input element (or perform any other action on it)
    active_input_element.click()
    submitBtn = driver.find_element(By.ID, 'sData')
    submitBtn.click()


def input_articles(input_article_name, src_textarea_content):
    article_name_input = driver.find_element(By.ID, "txt_article")
    article_name_input.send_keys("Vietnam")
    article_name_input.send_keys(Keys.ENTER)

    table = driver.find_element(By.CLASS_NAME, "bootstrap-datatable")
    # locate the td element with the text "Check Requirements"
    check_requirement_cell = table.find_element(
        By.XPATH, "//td[contains(text(), 'Check Requirement')]"
    )
    # locate the nearest a element with id="edit_account"
    edit_account_btn = check_requirement_cell.find_element(
        By.XPATH, "following-sibling::td//a[@id='edit_account']"
    )
    edit_account_btn.click()
    country_dropdown = driver.find_element(By.ID, "select_country_chzn")
    country_dropdown.click()
    # Select Country name option
    # Find the li element with the text "Vietnam"
    country_name_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//li[contains(text(),'Vietnam')]"))
    )
    # country_id = driver.find_element(By.ID, "select_country_chzn_o_249")
    country_name_option.click()
    # print(input_article_name, src_textarea_content)
    # send s3 meta link into meta and icon input
    s3_meta_link = 'https://dwukht46mtp9x.cloudfront.net/uploads/located-in-toronto-the-royal-ontario-museum-is-one-of-the-largest-museums-in-canada-meta-1920x960-1678929973.jpg'
    icon_image_input = driver.find_element(By.ID, "icon")
    icon_image_input.send_keys(s3_meta_link)
    meta_image_input = driver.find_element(By.ID, "meta_image")
    meta_image_input.send_keys(s3_meta_link)
    # scroll to bottom of page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait = WebDriverWait(driver, 10)
    # Wait for the summary source button to be clickable and click it
    summary_iframe = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "summary___Frame"))
    )
    driver.switch_to.frame(summary_iframe)
    summary_change_src_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@title='Source' and @class='TB_Button_Off']")
        )
    )
    summary_change_src_button.click()
    summary_textarea = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "SourceField"))
    )
    # Open the local HTML file and read its contents
    with open('articles-content-with-summary.html', 'r') as file:
        html_articles_content = file.read()
    soup = BeautifulSoup(html_articles_content, "html.parser")
    first_p = soup.find('p').text
    first_sentence = ''
    for i, sentence in enumerate(first_p.split('. ')):
        if i == 0:
            first_sentence += sentence
            if '</p>' in sentence:
                break
        else:
            first_sentence += '. ' + sentence
            if '</p>' in sentence:
                break
    summary_content_with_p_tags = f"<p>{first_sentence}</p>"
    summary_textarea.clear()
    summary_textarea.send_keys(summary_content_with_p_tags)
    driver.switch_to.default_content()
    # Wait for the content source button to be clickable and click it version 2
    content_iframe = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "content___Frame"))
    )
    driver.switch_to.frame(content_iframe)
    content_change_src_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@title='Source' and @class='TB_Button_Off']")
        )
    )
    content_change_src_button.click()
    content_textarea = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "SourceField"))
    )
    content_textarea.clear()
    # content_textarea.send_keys('this is an example content')

    # Send the HTML content as keys to the input field

    content_textarea.send_keys(html_articles_content)


def process_doc():
    driver.get(
        'https://docs.google.com/document/d/1QC8zhagXpM9Gk5-a90aUuVcy1Zvs4QUbK4PERiu7Aog/edit')
    username_field = driver.find_element(By.NAME, 'identifier')
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)
    password_field = driver.find_element(By.NAME, 'Passwd')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)
    content = driver.page_source
    print(content)
