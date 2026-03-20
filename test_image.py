from PIL import Image
import os, glob

folder = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes"
for ext in ["*.png", "*.jpg", "*.jpeg"]:
    for file in glob.glob(os.path.join(folder, ext)):
        try:
            with Image.open(file) as img:
                print(os.path.basename(file), img.size, img.mode)
        except Exception as e:
            print("Error with", file, e)
