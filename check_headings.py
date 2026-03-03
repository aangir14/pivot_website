import glob
import re

files = glob.glob('**/*.html', recursive=True)
files = [f for f in files if '404.html' not in f and 'assets' not in f]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find heading sizes
    matches = re.findall(r'<h([1-6])[^>]*class=[\'\"]([^\'\"]*)[\'\"]', content)
    
    if matches:
        print(f'\n--- {file} ---')
        for match in set(matches):
            tag = 'h' + match[0]
            classes = match[1]
            sizes = re.findall(r'text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)', classes)
            if sizes:
                print(f'{tag}:', ', '.join(sizes))
            else:
                print(f'{tag} NO SIZE:', classes)
