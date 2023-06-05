from paycec.paycec import Paycec
import os
import time
try:
    with Paycec() as bot:
        bot.land_first_page()
        bot.login_dashboard()
        # function to optimize the original images that good for SEO content and website performance
        bot.optimize_image()
        # function to convert a doc link into html format
        # bot.convert_html()
        # function to upload html format into each faqs into dashboard
        # bot.upload_faqs()
        # Upload all the images in the img_optimized into paycec upload file
        bot.upload_images()
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
