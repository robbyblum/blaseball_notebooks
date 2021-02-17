import os
import nbformat
from nbconvert import HTMLExporter
import urllib.parse
from pathlib import Path


def make_notebook(file_info, outdir_root='', binder_base=None, github_base=None):
    fname, _ = os.path.splitext(os.path.basename(file_info['file']))
    outname = fname + '.html'

    book = nbformat.read(file_info['file'], as_version=4)
    # TODO: do title better
    book["metadata"]["title"] = fname
    if github_base:
        book["metadata"]["github_url"] = github_base + file_info['file']
    if binder_base:
        escaped = urllib.parse.quote(file_info['file'])
        book["metadata"]["binder_url"] = binder_base + escaped

    e = HTMLExporter(config=file_info['config'])
    (body, resources) = e.from_notebook_node(book)

    outfile = os.path.join(outdir_root, file_info['outdir'], outname)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)

    with open(outfile, 'w', encoding='utf8') as fp:
        fp.write(body)


template_dir = ".jupyter/templates"
binder_url_base = "https://mybinder.org/v2/gh/Edgarware/blaseball_notebooks/main?filepath="
github_url_base = "https://github.com/Edgarware/blaseball_notebooks/blob/main/"

configs = [
    {
        'files': '*.ipynb',
        'outdir': '',
        'config': {
            'TemplateExporter': {
                'extra_template_basedirs': [template_dir],
                'template_name': 'notes'
            },
            'HTMLExporter': {
                'anchor_link_text': ' '
            }
        }
    },
    {
        'files': 'election_notes/*.ipynb',
        'outdir': 'election_notes',
        'config': {
            'TemplateExporter': {
                'extra_template_basedirs': [template_dir],
                'template_name': 'notes',
                'exclude_input': True
            },
            'HTMLExporter': {
                'anchor_link_text': ' '
            }
        }
    },
    {
        'files': 'misc_notebooks/*.ipynb',
        'outdir': '',
        'config': {
            'TemplateExporter': {
                'extra_template_basedirs': [template_dir],
                'template_name': 'lab-narrow',
                'exclude_input': True
            }
        }
    }
]
for config_info in configs:
    p = Path('.')
    files = [x.as_posix() for x in p.glob(config_info['files']) if '.ipynb_checkpoints' not in x.as_posix()]

    for file in files:
        file_info = config_info
        file_info['file'] = file
        make_notebook(file_info, outdir_root='docs', github_base=github_url_base, binder_base=binder_url_base)
        print(f"Converted {file}")
