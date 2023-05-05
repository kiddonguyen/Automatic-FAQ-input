from PIL import Image
import os
import shutil

input_folder = "/img"
output_folder = "/img_optimized"


for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        with Image.open(os.path.join(input_folder, filename)) as img:
            img_format = img.format
            img_size = img.size
            img_quality = 65

            # Set different quality level for images smaller than 1920x960 pixels
            if img_size[0] < 1920 and img_size[1] < 960:
                img_quality = 80

            img = img.convert('RGB')
            img.save(os.path.join(output_folder, filename),
                     optimize=True, format=img_format, quality=img_quality)
    else:
        shutil.copy(os.path.join(input_folder, filename),
                    os.path.join(output_folder, filename))
