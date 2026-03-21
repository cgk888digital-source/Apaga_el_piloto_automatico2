import os
import glob
import re
import unicodedata

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '_', value)
    return value

def rename_chapters():
    base_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\capitulos"
    
    files = sorted(glob.glob(os.path.join(base_dir, "capitulo_*.md")))
    
    for filepath in files:
        filename = os.path.basename(filepath)
        
        # Ignorar front matter especial si no queremos renombrarlos
        if "portadilla" in filename or "derechos" in filename or "dedicatoria" in filename or "prefacio" in filename or "titulo" in filename:
            continue
            
        # Solo renombramos si el archivo todavia tiene el nombre generico 'capitulo_XX.md'
        if re.match(r'^capitulo_\d{2}\.md$', filename) or "glosario" in filename or "bibliografia" in filename or "autor" in filename:
            raw_title = ""
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.strip().startswith('---'):
                        raw_title = line.strip()
                        if raw_title.startswith('# '):
                            raw_title = raw_title[2:]
                        break
            
            if raw_title:
                # Quitamos indicadores de capitulo del texto si existen
                raw_title = re.sub(r'^Capítulo \d+:\s*', '', raw_title, flags=re.IGNORECASE)
                
                slug = slugify(raw_title)
                slug = '_'.join(slug.split('_')[:6]) # Max 6 palabras
                
                # Determinamos el prefijo (ej: capitulo_01)
                prefix_match = re.match(r'^(capitulo_\d+)', filename)
                prefix = prefix_match.group(1) if prefix_match else filename.replace('.md', '')
                
                new_filename = f"{prefix}_{slug}.md"
                
                # Evitar doble nombre si ya esta slugified o es el mismo
                if new_filename == filename:
                    continue
                    
                new_filepath = os.path.join(base_dir, new_filename)
                
                try:
                    os.rename(filepath, new_filepath)
                    print(f"Renamed: {filename} -> {new_filename}")
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")

if __name__ == '__main__':
    rename_chapters()
