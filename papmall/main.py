from login_auto import login_dashboard
from login_auto import input_faq

def main():
    # Input FAQs for Paycec
    dashboard_url = 'https://www.paycec.com/dashboard/login'
    login_dashboard(username, password, dashboard_url)
    faq_name = process_faqs()[0]
    faq_content = process_faqs()[1]
    for i in range(len(process_faqs()[0])):
        input_faq(faq_name[i], faq_content[i], "Amex")
    


if __name__ == "__main__":
    main()
