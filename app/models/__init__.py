"""

Related reading:
    https://buildmedia.readthedocs.org/media/pdf/flask-sqlalchemy/stable/flask-sqlalchemy.pdf
"""

import os
import sys
import importlib

# despite being globally defined the db object is context aware (use with app.app_context(): to use interactively)
from app.common.extensions import db
db = db


for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or not module.endswith('.py'):
        continue
    module_name = module[:-3]
    cls = getattr(importlib.import_module('.' + module_name, package=__package__), module_name)
    setattr(sys.modules[__name__], module_name, cls)
