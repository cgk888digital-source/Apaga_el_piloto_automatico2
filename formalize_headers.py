import os
import glob
import re

def formalize_headers(content):
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            continue
            
        # Heurística extendida: 1. Título (si es corto y no tiene punto final original)
        # O líneas capitalizadas cortas.
        
        is_numbered_candidate = bool(re.match(r'^\d+\.\s+[A-Z\u00C0-\u00DC].*$', stripped))
        
        # Si ya es un header o es metadato, saltar
        if stripped.startswith('#') or stripped.startswith('---') or stripped.startswith('!') or stripped.startswith('|'):
            new_lines.append(line)
            continue

        is_header = False
        if len(stripped) < 100 and not stripped.endswith('.') and not stripped.endswith(':'):
            if is_numbered_candidate or (stripped[0].isupper() and len(stripped.split()) > 1):
                is_header = True
        
        # Caso especial para Screenshot 2: "4. Tus padres y cuidadores"
        # Antes del fix_style no tenía punto.
        
        if is_header:
            new_lines.append(f"## {stripped}")
        else:
            new_lines.append(line)
            
    return '\n'.join(new_lines)

def process():
    base_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\capitulos"
    files = sorted(glob.glob(os.path.join(base_dir, "*.md")))
    for f in files:
        # Primero restauramos el contenido original para remover puntos mal puestos en headers si los hay
        # (Aunque el fix_style ya los puso, queremos que formalize_headers gane si no los tenía)
        # En realidad, si tiene punto ya no es match. 
        # Pero podemos ser más laxos.
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        fixed = formalize_headers(content)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(fixed)
        print(f"Formalized headers in {os.path.basename(f)}")

if __name__ == "__main__":
    process()
