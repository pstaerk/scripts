import os
import glob
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', type=str, help='File to be compiled.')
args = parser.parse_args()

def make_html_link(match):
    """Turn match of vimwiki link to html link.

    """
    print(f'Found {match.group()}')
    return match.group() + '.html'

def bind_note_links(f):
    """Change the note links to resemble the correct path to other notes
    for pandoc to link correctly.

    """
    with open(f, 'r') as ct:
        t = ct.read()
    t = re.sub('\[[^\]]*\]\(\d+', make_html_link, t)
    with open(f+'_tmp', 'w') as ct:
        ct.write(t)

f = args.c
bind_note_links(f)
base = f.replace('.md', '')
os.system(f'pandoc -f markdown+task_lists -s --mathjax --bibliography ~/Documents/Uni/MSem3-4/msc_thesis_pm/tex/zotero.bib --lua-filter=zotero.lua --metadata=zotero_scannable_cite:true -c style.css {f}_tmp pandoc_options.yaml -o ../markdown_html/{base}.html')
os.system(f'rm {f}_tmp')

# for f in glob.glob('*.md'):
#     bind_note_links(f)
#     base = f.replace('.md', '')
#     os.system(f'pandoc -f markdown+task_lists -s --mathjax --bibliography ~/Documents/Uni/MSem3-4/msc_thesis_pm/tex/zotero.bib --lua-filter=zotero.lua --metadata=zotero_scannable_cite:true -c style.css {f}_tmp pandoc_options.yaml -o ../markdown_html/{base}.html')
#     os.system(f'rm {f}_tmp')
