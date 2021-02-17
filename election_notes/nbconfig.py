from nbhelper import base_config
import os

c = get_config()
x = base_config(c, os.path.dirname(__file__))
x.TemplateExporter.exclude_input = True