from PIL import Image, ImageDraw, ImageFont
import os

def update_cover_image():
    img_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\imagen_portada.png"
    out_path = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\imagenes\imagen_portada_v2.png"
    
    if not os.path.exists(img_path):
        print("Image not found")
        return
        
    img = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Subtitle area estimation
    # Based on the (640, 598) size and the crop provided
    # Title is around y=240, Subtitle around y=310
    sub_y = 310
    sub_h = 35
    
    # Let's "clean" the area by sampling pixels from just above and below the subtitle
    # to create a vertical gradient to fill the text area.
    # We'll do this for slices to respect horizontal variation (like the pillar)
    
    clean_y_top = sub_y - 5
    clean_y_bottom = sub_y + sub_h + 5
    
    for x in range(w):
        c_top = img.getpixel((x, clean_y_top))
        c_bottom = img.getpixel((x, clean_y_bottom))
        
        # Fill the vertical column with a simple linear interpolation
        for y in range(clean_y_top, clean_y_bottom + 1):
            ratio = (y - clean_y_top) / (clean_y_bottom - clean_y_top)
            # Simple linear interp
            r = int(c_top[0] * (1 - ratio) + c_bottom[0] * ratio)
            g = int(c_top[1] * (1 - ratio) + c_bottom[1] * ratio)
            b = int(c_top[2] * (1 - ratio) + c_bottom[2] * ratio)
            img.putpixel((x, y), (r, g, b))
            
    # Now draw the new text
    # The font in the original looks like a light sans-serif (maybe Roboto or similar)
    try:
        font_size = 22
        # Trying a standard Windows font
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
        
    text = "Tu manual para Tomar el Control de tu vida o de tu mente."
    
    # Get text size to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    tx = (w - tw) // 2
    ty = sub_y + (sub_h - th) // 2
    
    # Draw text with a very subtle shadow (as the original has some glow/shadow)
    draw.text((tx+1, ty+1), text, font=font, fill=(0, 0, 0, 100))
    draw.text((tx, ty), text, font=font, fill=(230, 230, 230)) # Off-white like original
    
    img.save(out_path)
    # Also overwrite the original to make sure PDF generation picks it up
    img.save(img_path)
    print(f"Updated cover image at {out_path} and {img_path}")

if __name__ == '__main__':
    update_cover_image()
