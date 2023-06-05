
# This file will include a class with instance methods.
# That will be responsible convert images file extension: .jpg, png, jpeg to save for web images
from slugify import slugify
from PIL import Image
import os
import shutil
import nltk
from nltk.corpus import stopwords
from selenium.webdriver.remote.webdriver import WebDriver
nltk.download('punkt')

class PaycecOptimizedImages:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def empty_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    def save_for_web(self):
        input_folder = "img"
        output_folder = "img_optimized"
        self.empty_folder(output_folder)
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_folder):
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                with Image.open(os.path.join(input_folder, filename)) as img:
                    img_format = img.format
                    img_size = img.size
                    img_quality = 65
                    if img_size[0] < 1920 and img_size[1] < 960:
                        img_quality = 80

                    img = img.convert('RGB')
                    # Define the output path
                    output_path = os.path.join(output_folder, filename)
                    img.save(output_path, optimize=True,
                            format=img_format, quality=img_quality)

                    # Calculate optimization percentage
                    original_size = os.path.getsize(
                        os.path.join(input_folder, filename))
                    optimized_size = os.path.getsize(output_path)
                    optimized_percent = (
                        1 - (optimized_size / original_size)) * 100
                    if img_size[0] == 1920:
                        title = os.path.splitext(filename)[0]
                        title = slugify(title)
                        new_filename = f"{title}-meta{os.path.splitext(filename)[1]}"
                        new_filepath = os.path.join(output_folder, new_filename)
                        counter = 1
                        while os.path.exists(new_filepath):
                            new_filename = f"{title}-meta_{counter}{os.path.splitext(filename)[1]}"
                            new_filepath = os.path.join(
                                output_folder, new_filename)
                            counter += 1
                        os.rename(output_path, new_filepath)
                        print(
                            f"{filename} optimized by {optimized_percent:.2f}% and renamed to {new_filename}")
                    else:
                        print(f"{filename} optimized by {optimized_percent:.2f}%")
            else:
                shutil.copy(os.path.join(input_folder, filename),
                            os.path.join(output_folder, filename))
    
    def check_stopwords(self, text):
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        words = nltk.word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in stop_words]
        filtered_text = ' '.join(filtered_words)
        return filtered_text
