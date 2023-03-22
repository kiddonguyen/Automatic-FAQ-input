import os
import time

from selenium import webdriver


from selenium.webdriver.common.by import By  # Import the By class


from selenium.webdriver.chrome.service import Service


from selenium.webdriver.support.ui import Select


from selenium.webdriver.support.ui import WebDriverWait


from selenium.webdriver.support import expected_conditions as EC


from tkinter import Tk


# Get the screen width using the Tkinter module


root = Tk()


screen_width = root.winfo_screenwidth()
root.destroy()


chrome_options = webdriver.ChromeOptions()


# Set the option to keep the browser window open after the driver is closed


chrome_options.add_experimental_option("detach", True)


# Replace these values with your login information


username = "thanhnguyen@mobcec.com"


password = "0967614208nN@"


# Set up the Selenium webdriver (make sure to replace the path with the location of your webdriver)


chrome_driver_path = os.path.abspath("C:/bin/chromedriver.exe")


# Create a Service object with the path to the ChromeDriver executable


service = Service(executable_path=chrome_driver_path)


driver = webdriver.Chrome(service=service, options=chrome_options)


driver.set_window_size(screen_width, 1080)


# Navigate to the login page


driver.get("https://www.thecanadianimmigration.org/dashboard/login")


# Find the username and password fields and enter your login information


username_field = driver.find_element(By.ID, 'email')


username_field.send_keys(username)


password_field = driver.find_element(By.ID, 'password')


password_field.send_keys(password)


# Submit the login form


submit_button = driver.find_element(By.ID, "btn-login")


submit_button.click()



driver.get("https://www.thecanadianimmigration.org/dashboard/list_article")


def input_faq(input_article_name, src_textarea_content):


    add_new_article = driver.find_element(By.ID, 'create_article')


    add_new_article.click()


    article_name = driver.find_element(By.ID, 'articlename')


    article_name.send_keys(input_article_name)


    # dropdown = Select(driver.find_element(By.ID, "select_type"))


    type_id_dropdown = driver.find_element(By.ID, 'select_type_chzn')


    type_id_dropdown.click()


    # Select FAQs option


    faq_type = driver.find_element(By.ID, 'select_type_chzn_o_3')


    faq_type.click()


    country_dropdown = driver.find_element(By.ID, 'select_country_chzn')


    country_dropdown.click()


    # Select FAQs option


    country_id = driver.find_element(By.ID, 'select_country_chzn_o_249')


    country_id.click()


    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    wait = WebDriverWait(driver, 10)


    iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "content___Frame")))
    driver.switch_to.frame(iframe)


    # Wait for the TB_Button_Text element to be clickable and click it


    change_src_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Source' and @class='TB_Button_Off']")))


    change_src_button.click()


    src_textarea = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "SourceField")))


    src_textarea.clear()


    src_textarea.send_keys(src_textarea_content)


    # Switch back to the main content
    driver.switch_to.default_content()
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    submit_button.click()
    time.sleep(3)
def main():
    with open('articles-name.txt', 'r') as articles_name_file:
        articles_name_list = [line.strip() for line in articles_name_file.readlines()]
    articles_name_file.close()
    with open('articles-content.txt', 'r') as articles_content_file:
        articles_content_list = [line.strip() for line in articles_content_file.readlines()]
    articles_content_file.close()
    for index in range(len(articles_name_list)):
        input_faq(articles_name_list[index], articles_content_list[index])
if __name__ == "__main__":
    main()
# Close the browser window
# driver.quit()


