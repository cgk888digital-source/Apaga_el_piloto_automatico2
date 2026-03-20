from PIL import Image
import os
img_dir = 'imagenes'
for f in os.listdir(img_dir):
    try:
        path = os.path.join(img_dir, f)
        with Image.open(path) as img:
            print(f"{f}: {img.size}")
    except:
        pass
