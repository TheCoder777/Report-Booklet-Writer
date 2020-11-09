
"""
Global config for files/paths and directories
TODO: move paths into defines/configs.py
"""

import pathlib

# two times parent because we're two levels down in code
# (rbwriter/defines/paths.py)
ROOT = pathlib.Path(__name__).parent.parent

# this is relative from executing direcory
DB_PATH = pathlib.Path("./db")
USER_DB_PATH = DB_PATH / "user.db"

COOKIE_PATH = pathlib.Path("./cookie")
USER_PATH = DB_PATH / "users"

TEMPLATE_PREFIX = pathlib.Path("templates/default/")

# absolute paths
PDF_TEMPLATE_ORIGIN_PATH = ROOT / TEMPLATE_PREFIX / "report_booklet_template_de.pdf"
TODOLIST_TEMPLATE_ORIGIN_PATH = ROOT / TEMPLATE_PREFIX / "todolist_template.json"

# relative paths
PDF_TEMPLATE_PATH = "./" / TEMPLATE_PREFIX / "report_booklet_template_de.pdf"
TODOLIST_TEMPLATE_PATH = "./" / TEMPLATE_PREFIX / "todolist_template.json"

# relative from user directory:
CONTENT_DB_PATH = "content.db"
TODOLIST_PATH = "todolist.json"
