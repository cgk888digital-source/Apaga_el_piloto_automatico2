from PIL import Image, ImageDraw, ImageFont
import os

def generate_banner_image():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 48)
        font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 26) 
        font_author = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 24)
    except:
        font_title = font_sub = font_author = ImageFont.load_default()
        
    # 1. Main Title
    title = "Apaga el Piloto Automático"
    bbox_t = draw.textbbox((0, 0), title, font=font_title)
    tx_t = (w - (bbox_t[2] - bbox_t[0])) // 2
    draw.text((tx_t, 60), title, font=font_title, fill=(0, 0, 0))
    
    # 2. Subtitle as ONE line "block" (Reduced font to fit)
    sub_text = "Tu Manual de vuelo para tomar el control de tu Vida y tu Mente"
    
    # Check if it fits on one line
    bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = bbox_s[2] - bbox_s[0]
    
    if sw < w * 0.9:
        tx_s = (w - sw) // 2
        draw.text((tx_s, 130), sub_text, font=font_sub, fill=(20, 20, 20))
    else:
        # If it doesn't fit, smaller font
        curr_size = 26
        while sw > w * 0.9 and curr_size > 14:
            curr_size -= 2
            font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", curr_size)
            bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
            sw = bbox_s[2] - bbox_s[0]
        tx_s = (w - sw) // 2
        draw.text((tx_s, 130), sub_text, font=font_sub, fill=(20, 20, 20))
        
    # 3. Horizontal marker
    draw.line([50, 280, 750, 280], fill=(40, 40, 40), width=18)
    
    # 4. Author
    author = "Silvio Vasconcelos"
    bbox_a = draw.textbbox((0, 0), author, font=font_author)
    tx_a = (w - (bbox_a[2] - bbox_a[0])) // 2
    draw.text((tx_a, 400), author, font=font_author, fill=(0, 0, 0))

    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\banner_vuelo.png"
    img.save(out_path)
    print(f"Banner ONE-LINE BLOCK saved to {out_path}")

if __name__ == "__main__":
    generate_banner_image()
