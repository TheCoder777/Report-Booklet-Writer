
"""
Global config for files/paths and directories
TODO: move paths into defines/configs.py
"""

from pathlib import Path

# two times parent because we're two levels down in code
# (rbwriter/defines/paths.py)
ROOT = Path(__file__).parent.parent

# prefix for everything
GLOBAL_PREFIX = Path("rbwriter")

# this is relative from executing directory
DB_PREFIX = Path(GLOBAL_PREFIX / "./db")
USER_DB_PATH = DB_PREFIX / "user.db"

COOKIE_PATH = Path(GLOBAL_PREFIX / "./cookie")
USER_PATH = DB_PREFIX / "users"

# this will only be used in path generation for templates/todolists
TEMPLATE_PREFIX = Path("templates/default/")

# from this, the local folder will be created
TEMPLATE_DIRECTORY = GLOBAL_PREFIX / TEMPLATE_PREFIX

# absolute paths
PDF_TEMPLATE_ORIGIN_PATH = Path(ROOT / TEMPLATE_PREFIX / "report_booklet_template_de.pdf").absolute()
TODOLIST_TEMPLATE_ORIGIN_PATH = Path(ROOT / TEMPLATE_PREFIX / "todolist_template.json").absolute()

# relative paths
PDF_TEMPLATE_PATH = GLOBAL_PREFIX / TEMPLATE_PREFIX / "report_booklet_template_de.pdf"
TODOLIST_TEMPLATE_PATH = GLOBAL_PREFIX / TEMPLATE_PREFIX / "todolist_template.json"

# relative from user directory:
CONTENT_DB_PATH = "content.db"
TODOLIST_PATH = "todolist.json"

# Server prefix directory
SERVER_PREFIX = Path("templates/config/")

# Server config files
NGINX_CONFIG_NAME = "nginx.conf"
UWSGI_CONFIG_NAME = "rbwriter_uwsgi.ini"

# absolute paths
NGINX_CONFIG_ORIGIN = Path(ROOT / SERVER_PREFIX / NGINX_CONFIG_NAME).absolute()
UWSGI_CONFIG_ORIGIN = Path(ROOT / SERVER_PREFIX / UWSGI_CONFIG_NAME).absolute()

# relative paths
NGINX_CONFIG_DEST = Path("/etc/nginx/") / NGINX_CONFIG_NAME
UWSGI_CONFIG_DEST = GLOBAL_PREFIX / UWSGI_CONFIG_NAME


# SECRET_KEY path
SECRET_KEY = Path(GLOBAL_PREFIX / "secret.key")

# lists for checkup
DIRECTORIES = [
    GLOBAL_PREFIX,
    DB_PREFIX,
    USER_PATH,
    COOKIE_PATH,
    TEMPLATE_DIRECTORY
]

FILES = [
    # (ORIGIN, DESTINATION)
    (PDF_TEMPLATE_ORIGIN_PATH, PDF_TEMPLATE_PATH),
    (TODOLIST_TEMPLATE_ORIGIN_PATH, TODOLIST_TEMPLATE_PATH),
    (UWSGI_CONFIG_ORIGIN, UWSGI_CONFIG_DEST)
]

NGINX_FILES = [
    # (ORIGIN, DESTINATION)
    (NGINX_CONFIG_ORIGIN, NGINX_CONFIG_DEST)
]
