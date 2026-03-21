import os
import glob
from PIL import Image, ImageDraw, ImageFont

def draw_test_text():
    brain_dir = r"C:\Users\edwar\.gemini\antigravity\brain\4fb22dd5-e78b-40e9-91ff-dce60add8d1d"
    media_files = sorted(glob.glob(os.path.join(brain_dir, "media_*.png")), key=os.path.getmtime)
    
    if not media_files:
        print("No media files found")
        return
        
    latest_media = media_files[-1]
    print(f"Loading {latest_media}")
    
    img = Image.open(latest_media)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # We don't know the exact coordinates of the boxes, but we can guess them.
    # The image is a face on the left, boxes on the right.
    w, h = img.size
    
    box_x = int(w * 0.65)
    box_w = int(w * 0.3)
    box_h = int(h * 0.22)
    
    y_start = int(h * 0.15)
    spacing = int(h * 0.05)
    
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", int(h*0.03))
    except:
        font = ImageFont.load_default()

    texts = ["Primer Texto\n(Demostración)", "Segundo Texto\n(Demostración)", "Tercer Texto\n(Demostración)"]
    
    for i in range(3):
        y = y_start + i * (box_h + spacing)
        
        # Center text in the guessed box
        text = texts[i]
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        tx = box_x + box_w/2 - tw/2
        ty = y + box_h/2 - th/2
        
        draw.multiline_text((tx, ty), text, fill=(255, 255, 255), font=font, align="center")
        
    out_path = os.path.join(brain_dir, "media_with_text.png")
    img.save(out_path)
    print(f"Saved test image to {out_path}")

if __name__ == '__main__':
    draw_test_text()
