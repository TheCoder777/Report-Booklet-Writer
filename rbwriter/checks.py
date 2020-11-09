# system modules
import os
import sys
import time

# internal modules
from .defines import paths
from .defines.colors import BOLD, ERROR, SUCCESS, RESET, WARNING


def checkup():
    """
    Global checkup for all files and dirs
    If this doesn't succeed, the server will NOT start!
    """

    start_time = time.time()
    console = BOLD + "[CHECKUP] " + RESET
    print()

    if not os.path.isdir(paths.TMP_PATH):
        print(console + f"Temporary save directory {paths.TMP_PATH} doesn't exist...", end="")
        os.mkdir(paths.TMP_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "Temporary directory found!" + RESET)

    if not os.path.isdir(paths.COOKIE_PATH):
        print(console + f"Cookie directory {paths.COOKIE_PATH} doesn't exist...", end="")
        os.mkdir(paths.COOKIE_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "Cookie directory found!" + RESET)

    if not os.path.isdir(paths.DB_PATH):
        print(console + f"DB directory {paths.DB_PATH} doesn't exist...", end="")
        os.mkdir(paths.DB_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "DB directory found!" + RESET)

    if not os.path.isdir(paths.USER_PATH):
        print(console + f"User directory {paths.USER_PATH} doesn't exist...", end="")
        os.mkdir(paths.USER_PATH)
        print(SUCCESS + "created!" + RESET)
    else:
        print(console + SUCCESS + "User directory found!" + RESET)

    if not os.path.exists(paths.PDF_TEMPLATE_PATH):
        print(console + ERROR + "PDF Template not found! Please add a pdf template!" + RESET)
        sys.exit(1)
    else:
        print(console + SUCCESS + "PDF Template found!" + RESET)

    if not os.path.exists(paths.TODOLIST_TEMPLATE_PATH):
        print(console + ERROR + "Todolist template not found! Please add a todolist template!" + RESET)
        sys.exit(1)
    else:
        print(console + SUCCESS + "Todolist template found!" + RESET)

    # garbage cleaning (delete all pdf in tmp file)
    filelist = [f for f in os.listdir(paths.TMP_PATH) if f.endswith(".pdf")]
    if filelist:
        print(console + "Cleaning cache...")
        for f in filelist:
            print(WARNING + "\tremoving: " + os.path.join(paths.TMP_PATH, f) + "..." + RESET, end="")
            os.remove(os.path.join(paths.TMP_PATH, f))
            print(SUCCESS + "done!" + RESET)
    else:
        print(console + SUCCESS + "Cache is clean!" + RESET)

    # Calculate time difference (just because we can)
    diff = time.time() - start_time

    print(console + BOLD + SUCCESS + f"Checkup finished successfully in {diff:.4f} seconds!\n" + RESET)