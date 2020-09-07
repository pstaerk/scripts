import os
import glob
import re

def make_html_link(match):
    """Turn match of vimwiki link to html link.

    """
    return match.group() + '.html'

def bind_note_links(f):
    """Change the note links to resemble the correct path to other notes
    for pandoc to link correctly.

    """
    with open(f, 'r') as ct:
        t = ct.read()
    t = re.sub('\[.*\]\(\d+', make_html_link, t)
    with open(f+'_tmp', 'w') as ct:
        ct.write(t)

for f in glob.glob('*.md'):
    bind_note_links(f)
    base = f.replace('.md', '')
    os.system(f'pandoc -f markdown+task_lists -s -c style.css {f}_tmp -o ../markdown_html/{base}.html')
