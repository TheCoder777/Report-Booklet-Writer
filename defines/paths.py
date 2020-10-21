
"""
Global config for Filepaths and Directories
"""

DB_PATH                 = "./db"
USER_DB_PATH            = f"{DB_PATH}/user.db"

TMP_PATH                = "./tmp/"
COOKIE_PATH             = "./cookie"
USER_PATH               = f"{DB_PATH}/users"

TEMPLATE_PREFIX         = "./templates/default/"
PDF_TEMPLATE_PATH       = f"{TEMPLATE_PREFIX}Berichtsheft_template.pdf"
TODOLIST_TEMPLATE_PATH  = f"{TEMPLATE_PREFIX}todolist_template.json"

# relative from user directory:
CONTENT_DB_PATH         = f"content.db"
TODOLIST_PATH           = f"todolist.json"
