import os
import re

def remove_headers():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chapters_dir = os.path.join(current_dir, "capitulos")
    
    if not os.path.exists(chapters_dir):
        print(f"Directory not found: {chapters_dir}")
        return

    files = [f for f in os.listdir(chapters_dir) if f.startswith("capitulo_") and f.endswith(".md")]
    
    print(f"Found {len(files)} chapters to process.")

    for filename in files:
        file_path = os.path.join(chapters_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        modified = False
        
        for line in lines:
            # Check if line starts with header markers
            if re.match(r'^#+\s+', line):
                # Remove the markers but keep the text
                clean_line = re.sub(r'^#+\s+', '', line)
                new_lines.append(clean_line)
                modified = True
            else:
                new_lines.append(line)
                
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Processed: {filename}")
        else:
            print(f"No headers found/changed in: {filename}")

if __name__ == "__main__":
    remove_headers()
