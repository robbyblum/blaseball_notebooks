from pathlib import Path

# Dynamically find files
p = Path()
files = [x.as_posix() for x in p.glob('**/*.ipynb') if '.ipynb_checkpoints' not in x.as_posix()]

c = get_config()

c.NbConvertApp.notebooks = files
c.NbConvertApp.export_format = "html"
c.HTMLExporter.exclude_input = True
c.FilesWriter.build_directory = 'docs'
c.TemplateExporter.template_name = 'notes'
c.TemplateExporter.extra_template_basedirs = ['.jupyter/templates/']
