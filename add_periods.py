import os
import glob
import re

def add_periods_to_line(line):
    stripped = line.strip()
    if not stripped:
        return line
    if stripped == '---':
        return line
    if stripped.startswith('#') or stripped.startswith('!['):
        return line
    if stripped.startswith('|') and stripped.endswith('|'):
        return line
        
    # Check heuristic header
    is_list_item = bool(re.match(r'^([*_]*)(\d+\.)\s+|^([-*]\s+)', stripped))
    if not is_list_item and len(stripped) < 120 and len(stripped) > 0:
        c = stripped[0]
        if (c.isupper() or c in "¿¡" or c.isdigit()) and not stripped.endswith('.') and not stripped.startswith('- ') and not stripped.startswith('* '):
            return line # Preserve heuristic header without period
            
    # Remove formatting characters to see actual end character
    clean_line = stripped.rstrip('*_"\'\]\)>')
    if not clean_line:
        return line
        
    last_char = clean_line[-1]
    if last_char in ['.', ':', '?', '!', ',', ';', '…', '-']:
        return line
        
    # Line needs a period. We only capture trailing asterisks/underscores
    # so that the bold/italic regex matches correctly at the very end of the line.
    match = re.search(r'([*_]+)$', line.rstrip())
    if match:
        trailing_fmt = match.group(1)
        core = line.rstrip()[:-len(trailing_fmt)]
        new_line = core + '.' + trailing_fmt + '\n'
    else:
        new_line = line.rstrip() + '.' + '\n'
        
    return new_line

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue
            
        new_line = add_periods_to_line(line)
        new_lines.append(new_line)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def main():
    capitulos_dir = r"d:\cesar\dev\libros\Apaga_el_piloto_automatico2\capitulos"
    count = 0
    for file in glob.glob(os.path.join(capitulos_dir, "*.md")):
        process_file(file)
        count += 1
    print(f"Processed {count} files.")

if __name__ == '__main__':
    main()
