from PIL import Image, ImageDraw, ImageFont
import os

def generate_banner_image():
    # The banner image from the screenshots looks like just text on white or plain background
    # But since the user often uses the same background, I'll take the sky area of the cover as background for it, OR just white.
    # Looking at the user's second screenshot, it's black text on a light background.
    
    w, h = 1000, 250 # Typical banner size
    img = Image.new('RGB', (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        # Bold font for banner
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 36)
    except:
        font = ImageFont.load_default()
        
    # As requested: Add "vuelo" (or Vuelo) and change "o" to "y"
    text = "Tu manual de Vuelo para Tomar el Control de tu vida y de tu mente."
    # Break into two lines to match the screenshot provided
    words = text.split()
    line1 = " ".join(words[:7]) # "Tu manual de Vuelo para Tomar el"
    line2 = " ".join(words[7:]) # "Control de tu vida y de tu mente."
    
    y_text = 60
    for line in [line1, line2]:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        tx = (w - tw) // 2
        draw.text((tx, y_text), line, font=font, fill=(10, 10, 10)) # Very dark Gray
        y_text += 55

    # Save to a dedicated banner file
    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\banner_vuelo.png"
    img.save(out_path)
    print(f"Banner FIXED and saved to {out_path}")

if __name__ == "__main__":
    generate_banner_image()
