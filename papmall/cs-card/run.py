from paycec.paycec import Paycec
import os
import time
try:
    with Paycec() as bot:
        bot.land_first_page()
        bot.login_dashboard()
        bot.redirect_blog()
        bot.add_blog_post()
        bot.upload_faqs()
        time.sleep(5)
except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise
