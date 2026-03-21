import os
import glob
from PIL import Image

def dhash(image, hash_size=8):
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)

def match_image():
    brain_dir = r"C:\Users\edwar\.gemini\antigravity\brain\4fb22dd5-e78b-40e9-91ff-dce60add8d1d"
    media_files = sorted(glob.glob(os.path.join(brain_dir, "media_*.png")), key=os.path.getmtime)
    
    # Exclude the test image I just made
    media_files = [f for f in media_files if "media_with_text" not in f]
    
    if not media_files:
        print("No media files found")
        return
        
    target_img = media_files[-1]
    
    try:
        t_img = Image.open(target_img)
        t_hash = dhash(t_img)
        print(f"Target: {target_img} (Hash: {t_hash})")
    except Exception as e:
        print(f"Error opening target: {e}")
        return
        
    img_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes"
    candidates = glob.glob(os.path.join(img_dir, "capitulo_*.png")) + glob.glob(os.path.join(img_dir, "capitulo_*.jpg"))
    
    best_match = None
    best_dist = float('inf')
    
    for cand in candidates:
        try:
            c_img = Image.open(cand)
            c_hash = dhash(c_img)
            
            # Compute hamming distance
            dist = sum(c1 != c2 for c1, c2 in zip(t_hash, c_hash))
            
            if dist < best_dist:
                best_dist = dist
                best_match = cand
        except:
            continue
            
    print(f"Best match: {best_match} (Hamming dist {best_dist})")

if __name__ == '__main__':
    match_image()
