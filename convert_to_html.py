import re
import html
import os
from pathlib import Path

# File paths
input_file = r"C:\Users\ariin\Desktop\buka_a_moromona\livre_mormon_tahitien.txt"
output_dir = r"C:\Users\ariin\Desktop\buka_a_moromona"
index_file = os.path.join(output_dir, "index.html")
chapters_dir = os.path.join(output_dir, "chapters")
css_file = os.path.join(output_dir, "styles.css")
js_file = os.path.join(output_dir, "script.js")

# Create chapters directory
os.makedirs(chapters_dir, exist_ok=True)
print(f"Created/verified directory: {chapters_dir}")

# Data structures
books = []
current_book = None
current_chapter = None
introduction = []

# Regex patterns
book_pattern = re.compile(r'^Te Buka.*$', re.IGNORECASE)
chapter_pattern = re.compile(r'^===\s*(.*)\s*Chapitre\s*(\d+)\s*===$')
verse_pattern = re.compile(r'^\d+\s+.*$')

# Read input file
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"Successfully read {input_file} with {len(lines)} lines")
except FileNotFoundError:
    print(f"Error: File {input_file} not found. Please verify the path.")
    exit(1)

# Parse content
for line in lines:
    line = line.strip()
    if not line:
        continue
    if book_pattern.match(line):
        if current_book:
            books.append(current_book)
        current_book = {
            'name': line,
            'abbrev': line.lower().replace(' ', '_').replace('’', ''),
            'chapters': []
        }
        current_chapter = None
        print(f"Found book: {line}")
    elif chapter_pattern.match(line):
        match = chapter_pattern.match(line)
        book_abbrev, chapter_number = match.group(1).strip().lower().replace(' ', '_'), match.group(2)
        if current_book:
            current_chapter = {
                'number': chapter_number,
                'verses': [],
                'id': f"{book_abbrev}_chapitre_{chapter_number}",
                'file': f"chapters/{book_abbrev}_chapitre_{chapter_number}.html",
                'title': f"{match.group(1).strip()} Chapitre {chapter_number}"
            }
            current_book['chapters'].append(current_chapter)
            print(f"Found chapter: {current_chapter['title']}")
    elif verse_pattern.match(line) and current_chapter:
        cleaned_verse = re.sub(r'^TE BUKA A MOROMONA\s+', '', line, flags=re.IGNORECASE)
        current_chapter['verses'].append(cleaned_verse)
    elif not current_book and not chapter_pattern.match(line):
        introduction.append(line)

if current_book:
    books.append(current_book)

# Create ordered list of all pages
page_sequence = []
if introduction:
    page_sequence.append({'file': 'chapters/introduction.html', 'title': 'Introduction'})
for book_idx, book in enumerate(books):
    for chapter in book['chapters']:
        page_sequence.append({
            'file': chapter['file'],
            'title': chapter['title'],
            'book_idx': book_idx + 1
        })

print(f"Page sequence created with {len(page_sequence)} pages:")
for i, page in enumerate(page_sequence):
    print(f"  {i}: {page['file']} - {page['title']}")

# CSS (unchanged from previous script)
css = [
    'body { font-family: "Georgia", serif; margin: 0; padding: 20px; line-height: 1.6; color: #333; background-color: #f4f4f4; }',
    '.container { max-width: 800px; margin: 0 auto; background: #fff; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.2); }',
    '.page { background: #fff; padding: 20px; border-radius: 5px; box-shadow: -5px 0 10px rgba(0,0,0,0.1), 5px 0 10px rgba(0,0,0,0.1); }',
    'h1, h2 { color: #1a3c6c; text-align: center; }',
    'h1 { font-size: 2.2em; margin-bottom: 10px; }',
    'h2 { font-size: 1.8em; margin-bottom: 20px; }',
    '.accordion { max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; }',
    '.accordion-item { margin-bottom: 10px; }',
    '.accordion-button { background-color: #f8f1e9; color: #333; cursor: pointer; padding: 12px; width: 100%; text-align: left; border: none; outline: none; font-size: 16px; transition: background-color 0.3s ease; border-radius: 5px; }',
    '.accordion-button:hover { background-color: #e0d8c3; }',
    '.accordion-content { display: none; padding: 10px 20px; }',
    '.accordion-content.show { display: block; }',
    '.accordion-content ul { list-style-type: none; padding-left: 20px; }',
    '.accordion-content li { margin-bottom: 8px; }',
    '.accordion-content a { text-decoration: none; color: #2b6cb0; transition: color 0.3s ease; }',
    '.accordion-content a:hover { color: #1a4971; text-decoration: underline; }',
    '.verse-container { margin-bottom: 12px; font-size: 1.1em; }',
    '.verse-container.introduction { background-color: #f9f9f9; font-style: italic; padding: 10px; border-left: 4px solid #d1d8e0; }',
    'nav { margin-top: 30px; display: flex; justify-content: space-between; align-items: center; padding: 10px; background: #f8f1e9; border-radius: 5px; }',
    'nav a { color: #2b6cb0; text-decoration: none; font-size: 1em; padding: 8px 15px; transition: all 0.3s ease; border-radius: 5px; }',
    'nav a:hover { background: #e0d8c3; color: #1a4971; }',
    '.nav-prev, .nav-next { flex: 1; }',
    '.nav-prev { text-align: left; }',
    '.nav-toc { text-align: center; }',
    '.nav-next { text-align: right; }',
    '@media (max-width: 600px) {',
    '  body { padding: 10px; }',
    '  .container { padding: 20px; }',
    '  h1 { font-size: 1.8em; }',
    '  h2 { font-size: 1.5em; }',
    '  .accordion { max-width: 100%; }',
    '  nav { flex-direction: column; gap: 15px; text-align: center; }',
    '  .nav-prev, .nav-toc, .nav-next { text-align: center; flex: none; }',
    '}'
]

# JavaScript (unchanged from previous script)
js = [
    'document.addEventListener("DOMContentLoaded", function() {',
    '  const buttons = document.querySelectorAll(".accordion-button");',
    '  buttons.forEach(button => {',
    '    button.addEventListener("click", function() {',
    '      const content = this.nextElementSibling;',
    '      const isOpen = content.classList.contains("show");',
    '      document.querySelectorAll(".accordion-content").forEach(c => c.classList.remove("show"));',
    '      if (!isOpen) content.classList.add("show");',
    '    });',
    '  });',
    '  const navLinks = document.querySelectorAll("nav a");',
    '  navLinks.forEach(link => {',
    '    link.addEventListener("click", function(e) {',
    '      e.preventDefault();',
    '      document.body.style.opacity = "0";',
    '      setTimeout(() => { window.location.href = this.href; }, 300);',
    '    });',
    '  });',
    '  document.body.style.transition = "opacity 0.3s ease";',
    '  document.body.style.opacity = "1";',
    '});'
]

# Write styles.css
with open(css_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(css))
print(f"Generated {css_file}")

# Write script.js
with open(js_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(js))
print(f"Generated {js_file}")

# Generate index.html
index_content = [
    '<!DOCTYPE html>',
    '<html lang="tah">',
    '<head>',
    '  <meta charset="UTF-8">',
    '  <meta name="description" content="Te Buka a Moromona - Tahitien">',
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '  <title>Te Buka a Moromona</title>',
    '  <link rel="stylesheet" href="styles.css">',
    '  <script src="script.js"></script>',
    '</head>',
    '<body>',
    '  <div class="container">',
    '    <h1>TE BUKA A MOROMONA</h1>',
    '    <h2>Te Tahi Faahou Ite No Iesu Mesia</h2>',
    '    <div class="accordion">'
]

if introduction:
    index_content.append('      <div class="accordion-item">')
    index_content.append('        <button class="accordion-button">Introduction</button>')
    index_content.append('        <div class="accordion-content">')
    index_content.append('          <ul>')
    index_content.append('            <li><a href="chapters/introduction.html">Introduction</a></li>')
    index_content.append('          </ul>')
    index_content.append('        </div>')
    index_content.append('      </div>')

for book_idx, book in enumerate(books, 1):
    index_content.append('      <div class="accordion-item">')
    index_content.append(f'        <button class="accordion-button">{html.escape(book["name"])}</button>')
    index_content.append('        <div class="accordion-content">')
    index_content.append('          <ul>')
    for chap_idx, chapter in enumerate(book['chapters'], 1):
        index_content.append(f'            <li><a href="{chapter["file"]}">{chapter["title"]}</a></li>')
    index_content.append('          </ul>')
    index_content.append('        </div>')
    index_content.append('      </div>')

index_content.extend([
    '    </div>',
    '  </div>',
    '</body>',
    '</html>'
])

# Write index.html
with open(index_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(index_content))
print(f"Generated {index_file}")

# Chapter template
chapter_template = '''
<!DOCTYPE html>
<html lang="tah">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="{chapter_title} - Te Buka a Moromona">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chapter_title}</title>
    <link rel="stylesheet" href="../styles.css">
    <script src="../script.js"></script>
</head>
<body>
    <div class="container">
        <div class="page">
            <h1>TE BUKA A MOROMONA</h1>
            <h2>{chapter_title}</h2>
            {verses_html}
            <nav>
                {prev_link}
                <div class="nav-toc"><a href="../index.html">Retour à la table des matières</a></div>
                {next_link}
            </nav>
        </div>
    </div>
</body>
</html>
'''

# Generate introduction.html
if introduction:
    verses_html = ''.join(f'<div class="verse-container introduction"><p>{html.escape(line)}</p></div>' for line in introduction)
    prev_link = '<div class="nav-prev"></div>'
    next_link = f'<div class="nav-next"><a href="{page_sequence[1]["file"]}">Page suivante</a></div>' if len(page_sequence) > 1 else '<div class="nav-next"></div>'
    intro_html = chapter_template.format(
        chapter_title="Introduction",
        verses_html=verses_html,
        prev_link=prev_link,
        next_link=next_link
    )
    intro_file = os.path.join(chapters_dir, "introduction.html")
    with open(intro_file, 'w', encoding='utf-8') as f:
        f.write(intro_html)
    print(f"Generated {intro_file}")

# Generate chapter files
generated_files = []
for book_idx, book in enumerate(books, 1):
    for chap_idx, chapter in enumerate(book['chapters'], 1):
        page_index = (sum(len(b['chapters']) for b in books[:book_idx-1]) + chap_idx) if introduction else (sum(len(b['chapters']) for b in books[:book_idx-1]) + chap_idx - 1)
        verses_html = ''.join(f'<div class="verse-container"><p>{html.escape(verse)}</p></div>' for verse in chapter['verses'])
        prev_link = f'<div class="nav-prev"><a href="{page_sequence[page_index-1]["file"]}">Page précédente</a></div>' if page_index > 0 else '<div class="nav-prev"></div>'
        next_link = f'<div class="nav-next"><a href="{page_sequence[page_index+1]["file"]}">Page suivante</a></div>' if page_index < len(page_sequence)-1 else '<div class="nav-next"></div>'
        chapter_html = chapter_template.format(
            chapter_title=chapter['title'],
            verses_html=verses_html,
            prev_link=prev_link,
            next_link=next_link
        )
        chapter_file = os.path.join(chapters_dir, f"{chapter['id']}.html")
        with open(chapter_file, 'w', encoding='utf-8') as f:
            f.write(chapter_html)
        generated_files.append(chapter_file)
        print(f"Generated {chapter_file}")

print(f"Total files generated: {len(generated_files) + (1 if introduction else 0) + 2} (index.html, styles.css, script.js, and chapters)")