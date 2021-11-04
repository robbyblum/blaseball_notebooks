import os
import nbformat
from nbconvert import HTMLExporter
import urllib.parse
from pathlib import Path


def get_title(cell, fallback=''):
    out = fallback
    data = cell["source"].split('\n')
    for line in data:
        if line.startswith('#'):
            out = line.lstrip('# ')
            break
    return out


def make_notebook(file_info, build_dir='', binder_base=None, github_base=None):
    fname, _ = os.path.splitext(os.path.basename(file_info['file']))
    outname = fname + '.html'

    book = nbformat.read(file_info['file'], as_version=4)
    title = get_title(book.cells[0], fname)
    book["metadata"]["title"] = title
    if github_base:
        book["metadata"]["github_url"] = github_base + file_info['file']
    if binder_base:
        escaped = urllib.parse.quote(file_info['file'])
        book["metadata"]["binder_url"] = binder_base + escaped

    e = HTMLExporter(config=file_info['config'])
    (body, resources) = e.from_notebook_node(book)

    out_file = Path(file_info['outdir'], outname)
    build_file = Path(build_dir).joinpath(out_file)
    os.makedirs(os.path.dirname(build_file), exist_ok=True)

    with open(build_file, 'w', encoding='utf8') as fp:
        fp.write(body)

    return out_file, title


template_dir = ".jupyter/templates"
# binder_url_base = "https://mybinder.org/v2/gh/Edgarware/blaseball_notebooks/main?filepath="
binder_url_base = None
github_url_base = "https://github.com/robbyblum/blaseball_notebooks/blob/main/"
github_pages_url_base = "https://robbyblum.github.io/blaseball_notebooks/"
build_dir = "docs"

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

output_files = []
for config_info in configs:
    p = Path('.')
    files = [x.as_posix() for x in p.glob(config_info['files']) if '.ipynb_checkpoints' not in x.as_posix()]

    for file in files:
        file_info = config_info
        file_info['file'] = file
        out_file = make_notebook(file_info, build_dir=build_dir, github_base=github_url_base, binder_base=binder_url_base)
        output_files.append(out_file)
        print(f"Converted {file} -> {out_file[0].as_posix()}")


# Generate redirect to Election Results Google Sheet
with open(os.path.join(build_dir, 'election_results.html'), 'w', encoding='utf8') as fp:
    fp.write("<head><meta http-equiv=\"refresh\" content=\"0;url=http://docs.google.com/spreadsheets/d/1v_1e2cxKoHvVejxXk4xHHC-YpPfKJXww15WIZ6nU7RU\"></head><body>Redirecting</body>")
output_files.append((Path("election_results.html"), "Election Vote Totals"))
print("Wrote election_results.html")

HTML_start = """<!DOCTYPE html>
<html>
<body style="line-height:2;font-size:18px;font-weight:400;font-family:sans-serif;">
<div style="width:1000px; margin:auto;">
<h1>Blaseball Notebooks</h1>
<p>Directory of files:</p>
"""

HTML_end = """</div>
</body>
</html>"""

links = ""
for file, title in output_files:
    file = github_pages_url_base + file.as_posix()
    links += f"<a href={file}>{title}</a></br>\n"

HTML = HTML_start + links + HTML_end
with open(os.path.join(build_dir, 'index.html'), 'w', encoding='utf8') as fp:
    fp.write(HTML)
print("Wrote index.html")
