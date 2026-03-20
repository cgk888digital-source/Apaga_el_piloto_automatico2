from PIL import Image
import glob
import os

folder = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes"
files = glob.glob(os.path.join(folder, "*.png")) + glob.glob(os.path.join(folder, "*.jpg"))

for file in files:
    try:
        with Image.open(file) as img:
            width, height = img.size
            if height > 200:
                # We crop the bottom 45 pixels
                cropped = img.crop((0, 0, width, height - 42))
                # For safety, save it to RGB
                rgb_img = cropped.convert('RGB')
                
        # save separately to avoid file lock
        rgb_img.save(file)
        print(f"Cropped {os.path.basename(file)} from {height} to {height-42}")
    except Exception as e:
        print(f"Error processing {file}: {e}")
