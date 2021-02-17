from pathlib import Path

def base_config(c, path='.'):
    # Dynamically find files
    p = Path(path)
    files = [x.as_posix() for x in p.glob('*.ipynb') if '.ipynb_checkpoints' not in x.as_posix()]

    c.NbConvertApp.notebooks = files
    c.NbConvertApp.export_format = "html"
    c.FilesWriter.build_directory = 'docs'
    c.TemplateExporter.template_name = 'notes'
    c.TemplateExporter.extra_template_basedirs = ['.jupyter/templates/']
    c.HTMLExporter.anchor_link_text = ' '
    return c