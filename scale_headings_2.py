import glob
import re
import os

files = glob.glob('**/*.html', recursive=True)
files = [f for f in files if '404.html' not in f and 'assets' not in f]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    def replacer(match):
        full_tag = match.group(0)
        
        # we only care if it has text-xs, text-sm, text-base, text-lg, text-xl
        if re.search(r'text-(xs|sm|base|lg|xl)\b', full_tag):
            # Change it to text-2xl
            new_tag = re.sub(r'text-(xs|sm|base|lg|xl)\b', 'text-2xl', full_tag)
            
            # Make sure it's bolded if we upgraded it so it reads like a heading
            if 'font-' not in new_tag:
                if 'class="' in new_tag:
                    new_tag = new_tag.replace('class="', 'class="font-bold ')
                elif "class='" in new_tag:
                    new_tag = new_tag.replace("class='", "class='font-bold ")
            return new_tag
        return full_tag

    new_content = re.sub(r'<h[1-6][^>]*>', replacer, content)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed small headings in {os.path.basename(file)}')
