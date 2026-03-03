import glob
import re

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all headings with their inner text and subsequent content until the next heading or major tag
    # We use a somewhat heuristic approach: extract blocks of content starting with a heading
    
    # Split content by heading tags loosely
    parts = re.split(r'(<h[1-6][^>]*>)', content)
    
    if len(parts) <= 1:
        return # No headings
        
    new_content = parts[0]
    
    for i in range(1, len(parts), 2):
        heading_tag = parts[i]
        text_after_heading = parts[i+1] if i+1 < len(parts) else ""
        
        # Estimate the volume of content immediately following this heading
        # Strip out HTML tags to count actual text words before the next major section
        text_content_only = re.sub(r'<[^>]+>', ' ', text_after_heading)
        word_count = len(text_content_only.split())
        
        # Extract existing size classes
        original_tag = heading_tag
        size_classes = re.findall(r'text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)', heading_tag)
        
        target_size = 'text-2xl' # Base minimum for any heading (larger than 18px body text)
        
        # Logic to "take into account the size of the content under the heading"
        if word_count > 100:
            target_size = 'text-4xl' 
        elif word_count > 50:
            target_size = 'text-3xl'
            
        # Exception for h1/h2 which should generally remain large regardless of immediate text volume
        if '<h1' in heading_tag.lower():
            target_size = 'text-4xl' if word_count <= 50 else 'text-5xl'
        elif '<h2' in heading_tag.lower():
            target_size = 'text-3xl' if word_count <= 50 else 'text-4xl'
            
        # Apply the fix to the tag
        if size_classes:
            current_size = size_classes[0]
            
            # Simple size ranking
            sizes = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl', '7xl', '8xl', '9xl']
            try:
                current_idx = sizes.index(current_size.replace('text-', ''))
                target_idx = sizes.index(target_size.replace('text-', ''))
                
                if current_idx < target_idx:
                    heading_tag = heading_tag.replace(current_size, target_size)
            except ValueError:
                pass
        else:
            # If no size class exists but we have a class attribute
            if 'class=' in heading_tag:
                 heading_tag = re.sub(r'class=[\"\']', lambda m: m.group(0) + f'{target_size} ', heading_tag)
            else:
                 # No class attribute at all
                 tag_name = re.match(r'<h[1-6]', heading_tag).group(0)
                 heading_tag = heading_tag.replace(tag_name, f'{tag_name} class="{target_size} font-bold"')
                 
        new_content += heading_tag + text_after_heading

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated headings in {filepath}")

files = glob.glob('**/*.html', recursive=True)
files = [f for f in files if '404.html' not in f and 'assets' not in f]

for file in files:
    process_html_file(file)
print("Finished standardizing headings.")
