from login_auto import *


def change_type_faqs(faq_urls, old_faqs_type_name, type_faqs_name):
    for url in faq_urls:
        driver.get(url)

        typeFaq = Select(driver.find_element(By.ID, "slcType"))
        selected_option = typeFaq.first_selected_option
        selected_option_text = selected_option.text
        # Deselect the option with the text "Option 2"
        for option in typeFaq.options:
            if old_faqs_type_name in option.text:
                typeFaq.deselect_by_visible_text(option.text)
        typeFaq2 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'slcType')))
        typeOption = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//option[contains(text(),'" + type_faqs_name + "')]")))
        typeOption.click()
        
        save_changes_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'submit_create')))
        save_changes_btn.click()
