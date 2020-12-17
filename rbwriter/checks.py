# system modules
import os
import shutil
import sys
import time

# internal modules
from .defines.configs import SECRET_KEY_SIZE
# available colors are BOLD, ERROR, SUCCESS, RESET, WARNING
from .defines.colors import BOLD, ERROR, SUCCESS, RESET, WARNING
from .defines.paths import DIRECTORIES, FILES, SECRET_KEY

console = BOLD + "[CHECKUP] " + RESET
intend = console + BOLD + WARNING + "=> " + RESET


def _gen_secret_key():
    with open(SECRET_KEY, "wb") as f:
        f.write(os.urandom(SECRET_KEY_SIZE))


def _secret_key_check():
    print(console + f"Checking for secret key: '{SECRET_KEY}' ...", end="", file=sys.stderr)
    if not os.path.isfile(SECRET_KEY):
        print(WARNING + "not found!" + RESET, file=sys.stderr)
        print(intend + f"Secret key doesn't exist, generating...", end="", file=sys.stderr)
        _gen_secret_key()
        # TODO: add proper error catching
        if not os.path.isfile(SECRET_KEY):
            print(ERROR + "failed!" + RESET, file=sys.stderr)
            print(console + ERROR + f"Unable to write secret key to {SECRET_KEY.absolute()}!" + RESET, file=sys.stderr)
            print(console + ERROR + "Application is unusable without a secret key, check your read/write policies!",
                  file=sys.stderr)
            sys.exit(1)
        else:
            print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)


def checkup():

    start_time = time.time()

    print("\n" + console + "--- START ---\n", file=sys.stderr)

    # DIRECTORIES
    for directory in DIRECTORIES:
        print(console + f"Checking directory: '{directory}' ...", end="", file=sys.stderr)
        if not os.path.isdir(directory):
            print(WARNING + f"doesn't exist!" + RESET, file=sys.stderr)
            print(intend + "Creating directory ...", end="", file=sys.stderr)
            os.makedirs(directory, exist_ok=True)
            # recheck after creating
            if not os.path.isdir(directory):
                print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                # TODO: display a proper help msg
                sys.exit(1)
            else:
                print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)
        else:
            print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)

    # FILES
    for file_pair in FILES:
        print(console + f"Checking file: '{file_pair[1]}' ...", end="", file=sys.stderr)
        if not os.path.exists(file_pair[1]):
            print(WARNING + f"doesn't exist!" + RESET, file=sys.stderr)
            print(intend + f"Copying file ...", end="", file=sys.stderr)
            shutil.copy2(file_pair[0], file_pair[1])
            # TODO: add proper error catching for copy process
            # recheck after copying
            if not os.path.exists(file_pair[1]):
                print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                sys.exit(1)
            else:
                print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)
        else:
            print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)

    _secret_key_check()

    time_difference = time.time() - start_time
    print(console + BOLD + SUCCESS + f"Checkup finished successfully in {time_difference:.4f} seconds!\n" + RESET,
          file=sys.stderr)

    print(console + "--- END ---\n", file=sys.stderr)
