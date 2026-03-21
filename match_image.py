import os
import glob
from PIL import Image

def get_average_color(img_path):
    try:
        img = Image.open(img_path).resize((50, 50)).convert('RGB')
        pixels = list(img.getdata())
        r = sum(p[0] for p in pixels) / len(pixels)
        g = sum(p[1] for p in pixels) / len(pixels)
        b = sum(p[2] for p in pixels) / len(pixels)
        return (r, g, b)
    except Exception as e:
        return (0, 0, 0)

def match_image():
    brain_dir = r"C:\Users\edwar\.gemini\antigravity\brain\4fb22dd5-e78b-40e9-91ff-dce60add8d1d"
    media_files = sorted(glob.glob(os.path.join(brain_dir, "media_*.png")), key=os.path.getmtime)
    
    # Exclude the test image I just made
    media_files = [f for f in media_files if "media_with_text" not in f]
    
    if not media_files:
        print("No media files found")
        return
        
    target_img = media_files[-1]
    print(f"Target: {target_img}")
    target_color = get_average_color(target_img)
    
    img_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes"
    candidates = glob.glob(os.path.join(img_dir, "capitulo_*.png")) + glob.glob(os.path.join(img_dir, "capitulo_*.jpg"))
    
    best_match = None
    best_dist = float('inf')
    
    for cand in candidates:
        c = get_average_color(cand)
        dist = sum((a-b)**2 for a, b in zip(target_color, c))
        if dist < best_dist:
            best_dist = dist
            best_match = cand
            
    print(f"Best match: {best_match} (dist {best_dist})")

if __name__ == '__main__':
    match_image()
