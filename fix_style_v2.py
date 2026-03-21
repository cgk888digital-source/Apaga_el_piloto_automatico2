import os
import glob
import re

def fix_content(content):
    lines = content.split('\n')
    new_lines = []
    
    in_numbered_list = False
    current_num = 0
    list_indent = ""
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            continue
            
        # 1. Numeración Sequential Fix
        num_match = re.match(r'^(\s*)(\d+)\.\s*(.*)$', line)
        if num_match:
            indent, num_str, rest = num_match.groups()
            num = int(num_str)
            if not in_numbered_list or indent != list_indent:
                in_numbered_list = True
                current_num = num
                list_indent = indent
            else:
                # If it's a sequence, we increment
                # Unless it's a nested list restart
                if num == 1:
                    current_num = 1
                else:
                    current_num += 1
            line = f"{indent}{current_num}. {rest}"
        elif stripped.startswith('#') or stripped.startswith('---'):
            in_numbered_list = False
            current_num = 0
            list_indent = ""

        # 2. Punctuation Fix
        line_to_process = line.rstrip()
        
        # Detectadores
        is_header = stripped.startswith('#')
        is_bullet = stripped.startswith('- ') or stripped.startswith('* ')
        is_numbered = bool(re.match(r'^\d+\.', stripped))
        is_metadata = stripped.startswith('[[') or stripped.startswith('!') or stripped.startswith('|') or stripped.startswith('---')
        ends_with_punctuation = bool(re.search(r'[.:;?!]\s*(\*\*)?$', stripped))
        ends_with_closure = bool(re.search(r'[)\]}>]\s*(\*\*)?$', stripped))
        
        # Condición para añadir punto:
        # - Es párrafo normal o bullet o número
        # - NO es un header grande
        # - NO es metadato
        # - NO termina ya en puntuación (:;?!)
        # - Si termina en closure ), puede que falte el punto final.
        
        should_add_dot = False
        if not is_header and not is_metadata and not ends_with_punctuation:
            # Bullet/Numbered lists o párrafos
            if is_bullet or is_numbered or (len(stripped) > 3): 
                # Evitar títulos heurísticos cortos tipo "FASE 1" o "OBJETIVO" si no tienen punto?
                # No, el usuario quiere puntos al final de los párrafos.
                if not (stripped.isupper() and len(stripped) < 20):
                    should_add_dot = True

        if should_add_dot:
            # Check for trailing bold markers
            if line_to_process.endswith('**'):
                # Si termina en **, ¿hay puntuación justo antes?
                if not re.search(r'[.:;?!]\*\*$', line_to_process):
                    line_to_process += "."
            else:
                line_to_process += "."
                
        new_lines.append(line_to_process)
        
    return '\n'.join(new_lines)

def process_files():
    base_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\capitulos"
    files = sorted(glob.glob(os.path.join(base_dir, "*.md")))
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        fixed = fix_content(content)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(fixed)
        print(f"Processed {os.path.basename(f)}")

if __name__ == "__main__":
    process_files()
