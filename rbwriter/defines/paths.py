
"""
Global config for files/paths and directories
TODO: move paths into defines/configs.py
"""

from pathlib import Path

# two times parent because we're two levels down in code
# (rbwriter/defines/paths.py)
ROOT = Path(__file__).parent.parent

# this is relative from executing directory
DB_PATH = Path("./db")
USER_DB_PATH = DB_PATH / "user.db"

COOKIE_PATH = Path("./cookie")
USER_PATH = DB_PATH / "users"

TEMPLATE_PREFIX = Path("templates/default/")

# absolute paths
PDF_TEMPLATE_ORIGIN_PATH = Path(ROOT / TEMPLATE_PREFIX / "report_booklet_template_de.pdf").absolute()
TODOLIST_TEMPLATE_ORIGIN_PATH = Path(ROOT / TEMPLATE_PREFIX / "todolist_template.json").absolute()

# relative paths
PDF_TEMPLATE_PATH = TEMPLATE_PREFIX / "report_booklet_template_de.pdf"
TODOLIST_TEMPLATE_PATH = TEMPLATE_PREFIX / "todolist_template.json"

# relative from user directory:
CONTENT_DB_PATH = "content.db"
TODOLIST_PATH = "todolist.json"

# Server prefix directory
SERVER_PREFIX = Path("templates/config")

# Server config files
NGINX_CONFIG_NAME = "nginx.conf"
UWSGI_CONFIG_NAME = "rbwriter_uwsgi.ini"

# absolute paths
NGINX_CONFIG_ORIGIN = Path(ROOT / SERVER_PREFIX / NGINX_CONFIG_NAME).absolute()
UWSGI_CONFIG_ORIGIN = Path(ROOT / SERVER_PREFIX / UWSGI_CONFIG_NAME).absolute()

# relative paths
NGINX_CONFIG_DEST = Path("/etc/nginx/") / NGINX_CONFIG_NAME
UWSGI_CONFIG_DEST = UWSGI_CONFIG_NAME


# SECRET_KEY path
SECRET_KEY = Path("secret.key")