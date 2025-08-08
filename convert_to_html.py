import re
import html
import os
from pathlib import Path

# Chemins des fichiers
input_file = r"C:\Users\ariin\Desktop\buka_a_moromona\livre_mormon_tahitien.txt"
output_dir = r"C:\Users\ariin\Desktop\buka_a_moromona"
index_file = os.path.join(output_dir, "index.html")
chapters_dir = os.path.join(output_dir, "chapters")

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
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

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
                'file': f"chapters/{book_abbrev}_chapitre_{chapter_number}.html"
            }
            current_book['chapters'].append(current_chapter)
    elif verse_pattern.match(line) and current_chapter:
        # Supprimer "TE BUKA A MOROMONA" au début du verset
        cleaned_verse = re.sub(r'^TE BUKA A MOROMONA\s+', '', line, flags=re.IGNORECASE)
        current_chapter['verses'].append(cleaned_verse)
    elif not current_book and not chapter_pattern.match(line):
        introduction.append(line)

if current_book:
    books.append(current_book)

# Créer une liste ordonnée de toutes les pages (introduction + chapitres)
page_sequence = []
if introduction:
    page_sequence.append({'file': 'chapters/introduction.html', 'title': 'Introduction'})
for book in books:
    for chapter in book['chapters']:
        page_sequence.append({
            'file': chapter['file'],
            'title': f"{book['name']} - Chapitre {chapter['number']}"
        })

# Style CSS commun (chaque ligne entourée de guillemets)
css = [
    'body { font-family: "Georgia", serif; margin: 40px; line-height: 1.6; color: #333; background-color: #f8f9fa; }',
    'h1, h2 { color: #1a3c6c; }',
    'h1 { font-size: 2.2em; text-align: center; margin-bottom: 10px; }',
    'h2 { font-size: 1.8em; margin-bottom: 15px; }',
    '#toc { background-color: #fff; padding: 20px; border-radius: 8px; border: 1px solid #d1d8e0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 600px; margin: 20px auto; position: sticky; top: 20px; z-index: 100; }',
    '#toc h1 { font-size: 1.6em; margin-bottom: 15px; text-align: left; }',
    '#toc details { margin-bottom: 10px; }',
    '#toc summary { cursor: pointer; padding: 8px; font-weight: 500; color: #2b6cb0; transition: color 0.3s ease; list-style: none; position: relative; }',
    '#toc summary:hover { color: #1a4971; }',
    '#toc summary::before { content: "\\25B6"; display: inline-block; margin-right: 8px; font-size: 0.9em; transition: transform 0.3s ease; }',
    '#toc details[open] summary::before { transform: rotate(90deg); }',
    '#toc ul { list-style-type: none; padding-left: 20px; margin-top: 5px; }',
    '#toc li { margin-bottom: 8px; }',
    '#toc a { text-decoration: none; color: #2b6cb0; transition: color 0.3s ease; }',
    '#toc a:hover { color: #1a4971; text-decoration: underline; }',
    '.toc-item::before { content: "\\2022"; color: #2b6cb0; margin-right: 8px; }',
    '.verse { margin-bottom: 12px; font-size: 1em; }',
    '.introduction { margin-bottom: 20px; font-style: italic; color: #555; }',
    '.nav-container { margin-top: 20px; display: flex; justify-content: space-between; align-items: center; }',
    '.nav-prev, .nav-toc, .nav-next { flex: 1; text-align: center; }',
    '.nav-prev { text-align: left; }',
    '.nav-next { text-align: right; }',
    '.nav-prev a, .nav-toc a, .nav-next a { color: #2b6cb0; text-decoration: none; font-size: 1em; transition: color 0.3s ease; }',
    '.nav-prev a:hover, .nav-toc a:hover, .nav-next a:hover { color: #1a4971; text-decoration: underline; }',
    '@media (max-width: 600px) {',
    '  #toc { position: static; max-width: 100%; }',
    '  body { margin: 20px; }',
    '  h1 { font-size: 1.8em; }',
    '  h2 { font-size: 1.5em; }',
    '  #toc h1 { font-size: 1.4em; }',
    '  .nav-container { margin-top: 15px; flex-direction: column; gap: 10px; }',
    '  .nav-prev, .nav-toc, .nav-next { text-align: left; flex: none; }',
    '}'
]

# JavaScript commun
js = [
    '<script>',
    '  document.addEventListener("DOMContentLoaded", function() {',
    '    const details = document.querySelectorAll("#toc details");',
    '    details.forEach(detail => {',
    '      detail.addEventListener("toggle", function() {',
    '        if (this.open) {',
    '          details.forEach(other => {',
    '            if (other !== this) other.open = false;',
    '          });',
    '        }',
    '      });',
    '    });',
    '  });',
    '</script>'
]

# Générer le fichier principal (index.html) - uniquement la table des matières
index_content = [
    '<!DOCTYPE html>',
    '<html lang="tah">',
    '<head>',
    '  <meta charset="UTF-8">',
    '  <meta name="description" content="Te Buka a Moromona - Tahitien">',
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '  <title>Te Buka a Moromona</title>',
    '  <style>',
    *css,
    '  </style>',
    *js,
    '</head>',
    '<body>',
    '  <header>',
    '    <h1>TE BUKA A MOROMONA</h1>',
    '    <h2>Te Tahi Faahou Ite No Iesu Mesia</h2>',
    '  </header>',
    '  <nav id="toc" aria-label="Tableau des matières">',
    '    <h1>Tableau des Matières</h1>'
]

# Ajouter l'introduction à la table des matières
if introduction:
    index_content.append('    <div class="toc-item"><a href="chapters/introduction.html">Introduction</a></div>')

# Ajouter les livres et chapitres à la table des matières
for book in books:
    index_content.append(f'    <details aria-label="{html.escape(book["name"])}">')
    index_content.append(f'      <summary>{html.escape(book["name"])}</summary>')
    index_content.append('      <ul>')
    for chapter in book['chapters']:
        index_content.append(f'        <li class="toc-item"><a href="{chapter["file"]}">Chapitre {chapter["number"]}</a></li>')
    index_content.append('      </ul>')
    index_content.append('    </details>')

index_content.extend([
    '  </nav>',
    '</body>',
    '</html>'
])

# Écrire index.html
with open(index_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(index_content))

# Générer un fichier HTML pour l'introduction
if introduction:
    intro_content = [
        '<!DOCTYPE html>',
        '<html lang="tah">',
        '<head>',
        '  <meta charset="UTF-8">',
        '  <meta name="description" content="Introduction à Te Buka a Moromona">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <title>Te Buka a Moromona - Introduction</title>',
        '  <style>',
        *css,
        '  </style>',
        '</head>',
        '<body>',
        '  <header>',
        '    <h1>TE BUKA A MOROMONA</h1>',
        '    <h2>Introduction</h2>',
        '  </header>',
        '  <section id="introduction" aria-label="Introduction">',
        '    <div class="introduction">'
    ]
    for line in introduction:
        intro_content.append(f'      <p>{html.escape(line)}</p>')
    intro_content.extend([
        '    </div>',
        '  </section>',
        '  <div class="nav-container">',
        '    <div class="nav-prev"></div>',
        '    <div class="nav-toc"><a href="../index.html" aria-label="Retour à la table des matières">Retour à la table des matières</a></div>'
    ])
    if len(page_sequence) > 1:
        intro_content.append(f'    <div class="nav-next"><a href="{page_sequence[1]["file"]}" aria-label="Page suivante">Page suivante</a></div>')
    else:
        intro_content.append('    <div class="nav-next"></div>')
    intro_content.extend([
        '  </div>',
        '</body>',
        '</html>'
    ])
    intro_file = os.path.join(chapters_dir, "introduction.html")
    with open(intro_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(intro_content))

# Générer un fichier HTML pour chaque chapitre
for book_idx, book in enumerate(books):
    for chap_idx, chapter in enumerate(book['chapters']):
        page_index = (sum(len(b['chapters']) for b in books[:book_idx]) + chap_idx + 1) if introduction else (sum(len(b['chapters']) for b in books[:book_idx]) + chap_idx)
        
        chapter_content = [
            '<!DOCTYPE html>',
            '<html lang="tah">',
            '<head>',
            '  <meta charset="UTF-8">',
            f'  <meta name="description" content="Chapitre {chapter["number"]} de {html.escape(book["name"])}">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'  <title>{html.escape(book["name"])} - Chapitre {chapter["number"]}</title>',
            '  <style>',
            *css,
            '  </style>',
            '</head>',
            '<body>',
            '  <header>',
            f'    <h1>TE BUKA A MOROMONA</h1>',
            f'    <h2>{html.escape(book["name"])} - Chapitre {chapter["number"]}</h2>',
            '  </header>',
            f'  <section id="{chapter["id"]}" aria-label="Chapitre {chapter["number"]}">'
        ]
        for verse in chapter['verses']:
            chapter_content.append(f'    <p class="verse">{html.escape(verse)}</p>')
        chapter_content.extend([
            '  </section>',
            '  <div class="nav-container">'
        ])
        prev_link = page_sequence[page_index - 1]['file'] if page_index > 0 else None
        next_link = page_sequence[page_index + 1]['file'] if page_index < len(page_sequence) - 1 else None
        if prev_link:
            chapter_content.append(f'    <div class="nav-prev"><a href="{prev_link}" aria-label="Page précédente">Page précédente</a></div>')
        else:
            chapter_content.append('    <div class="nav-prev"></div>')
        chapter_content.append('    <div class="nav-toc"><a href="../index.html" aria-label="Retour à la table des matières">Retour à la table des matières</a></div>')
        if next_link:
            chapter_content.append(f'    <div class="nav-next"><a href="{next_link}" aria-label="Page suivante">Page suivante</a></div>')
        else:
            chapter_content.append('    <div class="nav-next"></div>')
        chapter_content.extend([
            '  </div>',
            '</body>',
            '</html>'
        ])
        chapter_file = os.path.join(chapters_dir, f"{chapter['id']}.html")
        with open(chapter_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(chapter_content))

print(f"Fichier principal généré : {index_file}")
print(f"Fichiers de contenu générés dans : {chapters_dir}")