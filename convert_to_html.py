import re
import html
import os
from pathlib import Path

# Chemins des fichiers
input_file = r"C:\Users\ariin\Desktop\buka_a_moromona\livre_mormon_tahitien.txt"
output_dir = r"C:\Users\ariin\Desktop\buka_a_moromona"
index_file = os.path.join(output_dir, "index.html")
chapters_dir = os.path.join(output_dir, "chapters")
css_file = os.path.join(output_dir, "styles.css")
js_file = os.path.join(output_dir, "script.js")

# Créer le dossier chapters s'il n'existe pas
os.makedirs(chapters_dir, exist_ok=True)

# Structure pour stocker le contenu
books = []
current_book = None
current_chapter = None
introduction = []

# Modèles pour identifier les livres, chapitres et versets
book_pattern = re.compile(r'^Te Buka.*$', re.IGNORECASE)
chapter_pattern = re.compile(r'^===\s*(.*)\s*Chapitre\s*(\d+)\s*===$')
verse_pattern = re.compile(r'^\d+\s+.*$')

# Lire le fichier texte
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Erreur : Le fichier {input_file} n'existe pas. Vérifiez le chemin.")
    exit(1)

# Analyser le contenu
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
    elif verse_pattern.match(line) and current_chapter:
        cleaned_verse = re.sub(r'^TE BUKA A MOROMONA\s+', '', line, flags=re.IGNORECASE)
        current_chapter['verses'].append(cleaned_verse)
    elif not current_book and not chapter_pattern.match(line):
        introduction.append(line)

if current_book:
    books.append(current_book)

# Créer une liste ordonnée de toutes les pages
page_sequence = []
if introduction:
    page_sequence.append({'file': 'chapters/introduction.html', 'title': 'Introduction'})
for book in books:
    for chapter in book['chapters']:
        page_sequence.append({
            'file': chapter['file'],
            'title': chapter['title']
        })

# CSS (adapté de l'exemple)
css = [
    'body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; background-color: #f8f9fa; }',
    'h1, h2 { color: #1a3c6c; }',
    'h1 { font-size: 2.2em; text-align: center; margin-bottom: 10px; }',
    'h2 { font-size: 1.8em; margin-bottom: 15px; }',
    '.accordion { max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; border: 1px solid #d1d8e0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }',
    '.accordion-item { margin-bottom: 10px; }',
    '.accordion-button { background-color: #f4f4f4; color: #333; cursor: pointer; padding: 10px; width: 100%; text-align: left; border: none; outline: none; font-size: 16px; transition: background-color 0.3s ease; }',
    '.accordion-button:hover { background-color: #e0e0e0; }',
    '.accordion-content { display: none; padding: 10px; }',
    '.accordion-content.show { display: block; }',
    '.accordion-content ul { list-style-type: none; padding-left: 20px; }',
    '.accordion-content li { margin-bottom: 8px; }',
    '.accordion-content a { text-decoration: none; color: #2b6cb0; }',
    '.accordion-content a:hover { text-decoration: underline; color: #1a4971; }',
    '.verse-container { margin-bottom: 12px; }',
    '.verse-container.introduction { background-color: #f9f9f9; font-style: italic; }',
    'nav { margin-top: 20px; display: flex; justify-content: space-between; align-items: center; }',
    'nav a { color: #2b6cb0; text-decoration: none; font-size: 1em; }',
    'nav a:hover { color: #1a4971; text-decoration: underline; }',
    '@media (max-width: 600px) {',
    '  body { margin: 20px; }',
    '  h1 { font-size: 1.8em; }',
    '  h2 { font-size: 1.5em; }',
    '  .accordion { max-width: 100%; }',
    '  nav { flex-direction: column; gap: 10px; text-align: left; }',
    '}'
]

# JavaScript (adapté de l'exemple)
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
    '});'
]

# Écrire styles.css
with open(css_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(css))

# Écrire script.js
with open(js_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(js))

# Générer index.html
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
    '  <h1>TE BUKA A MOROMONA</h1>',
    '  <h2>Te Tahi Faahou Ite No Iesu Mesia</h2>',
    '  <div class="accordion">'
]

# Ajouter l'introduction à la table des matières
if introduction:
    index_content.append('    <div class="accordion-item">')
    index_content.append('      <button class="accordion-button">Introduction</button>')
    index_content.append('      <div class="accordion-content">')
    index_content.append('        <ul>')
    index_content.append('          <li><a href="chapters/introduction.html">Introduction</a></li>')
    index_content.append('        </ul>')
    index_content.append('      </div>')
    index_content.append('    </div>')

# Ajouter les livres et chapitres
for book_idx, book in enumerate(books, 1):
    index_content.append('    <div class="accordion-item">')
    index_content.append(f'      <button class="accordion-button">{html.escape(book["name"])}</button>')
    index_content.append('      <div class="accordion-content">')
    index_content.append('        <ul>')
    for chap_idx, chapter in enumerate(book['chapters'], 1):
        index_content.append(f'          <li><a href="{chapter["file"]}">{chapter["title"]}</a></li>')
    index_content.append('        </ul>')
    index_content.append('      </div>')
    index_content.append('    </div>')

index_content.extend([
    '  </div>',
    '</body>',
    '</html>'
])

# Écrire index.html
with open(index_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(index_content))

# Modèle pour les pages de chapitres
chapter_template = '''
<!DOCTYPE html>
<html lang="tah">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="{chapter_title} - Te Buka a Moromona">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chapter_title}</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <h1>TE BUKA A MOROMONA</h1>
    <h2>{chapter_title}</h2>
    {verses_html}
    <nav>
        {prev_link}
        <a href="../index.html">Retour à la table des matières</a>
        {next_link}
    </nav>
</body>
</html>
'''

# Générer un fichier HTML pour l'introduction
if introduction:
    verses_html = ''.join(f'<div class="verse-container introduction"><p>{html.escape(line)}</p></div>' for line in introduction)
    prev_link = ''
    next_link = f'<a href="{page_sequence[1]["file"]}">Page suivante</a> | ' if len(page_sequence) > 1 else ''
    intro_html = chapter_template.format(
        chapter_title="Introduction",
        verses_html=verses_html,
        prev_link=prev_link,
        next_link=next_link
    )
    intro_file = os.path.join(chapters_dir, "introduction.html")
    with open(intro_file, 'w', encoding='utf-8') as f:
        f.write(intro_html)

# Générer un fichier HTML pour chaque chapitre
for book_idx, book in enumerate(books, 1):
    for chap_idx, chapter in enumerate(book['chapters'], 1):
        page_index = (sum(len(b['chapters']) for b in books[:book_idx-1]) + chap_idx) if introduction else (sum(len(b['chapters']) for b in books[:book_idx-1]) + chap_idx - 1)
        verses_html = ''.join(f'<div class="verse-container"><p>{html.escape(verse)}</p></div>' for verse in chapter['verses'])
        prev_link = f'<a href="{page_sequence[page_index-1]["file"]}">Page précédente</a> | ' if page_index > 0 else ''
        next_link = f'<a href="{page_sequence[page_index+1]["file"]}">Page suivante</a> | ' if page_index < len(page_sequence)-1 else ''
        chapter_html = chapter_template.format(
            chapter_title=chapter['title'],
            verses_html=verses_html,
            prev_link=prev_link,
            next_link=next_link
        )
        chapter_file = os.path.join(chapters_dir, f"{chapter['id']}.html")
        with open(chapter_file, 'w', encoding='utf-8') as f:
            f.write(chapter_html)

print(f"Fichier principal généré : {index_file}")
print(f"Fichiers de contenu générés dans : {chapters_dir}")
print(f"Fichiers de style et script générés : {css_file}, {js_file}")