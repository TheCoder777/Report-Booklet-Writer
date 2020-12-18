# system modules
import os
import shutil
import subprocess
import sys
import time

# internal modules
from .defines.configs import SECRET_KEY_SIZE
from .defines.colors import BOLD, ERROR, RESET, SUCCESS, WARNING
from .defines.paths import DIRECTORIES, FILES, NGINX_FILES, SECRET_KEY

console = BOLD + "[CHECKUP] " + RESET
intend = console + BOLD + WARNING + "=> " + RESET
setup = BOLD + "[SETUP] " + RESET
intend_setup = setup + BOLD + WARNING + "=> " + RESET


def _is_root():
    return os.geteuid() == 0


def _gen_secret_key():
    with open(SECRET_KEY, "wb") as f:
        f.write(os.urandom(SECRET_KEY_SIZE))


def _secret_key_check():
    print(console + f"Checking for secret key: '{SECRET_KEY}' ...", end="", file=sys.stderr)
    if not os.path.isfile(SECRET_KEY):
        print(WARNING + "not found!" + RESET, file=sys.stderr)
        print(intend + f"Secret key doesn't exist, generating...", end="", file=sys.stderr)
        try:
            _gen_secret_key()
            print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)
        except PermissionError as e:
            print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
            raise PermissionError(e.strerror
                                  + BOLD
                                  + ERROR
                                  + f"\nUnable to write secret key to '{SECRET_KEY.absolute()}'!\n"
                                  + "Application is unusable without a secret key, check your read/write policies!"
                                  + RESET)
        # except anything else (has to be some IO stuff):
        except Exception:
            print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
            raise IOError(BOLD
                          + ERROR
                          + f"\nUnable to write secret key to '{SECRET_KEY.absolute()}'!\n"
                          + "Application is unusable without a secret key, check your read/write policies!"
                          + RESET)
    else:
        print(BOLD + SUCCESS + "OK!" + RESET, file=sys.stderr)


def checkup():
    start_time = time.time()

    print("\n" + console + "--- CHECKUP START ---\n", file=sys.stderr)

    # DIRECTORIES
    for directory in DIRECTORIES:
        print(console + f"Checking directory: '{directory}' ...", end="", file=sys.stderr)
        if not os.path.isdir(directory):
            print(WARNING + f"doesn't exist!" + RESET, file=sys.stderr)
            print(intend + "Creating directory ...", end="", file=sys.stderr)
            try:
                os.makedirs(directory, exist_ok=True)
                print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)
            except PermissionError as e:
                print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                raise PermissionError(e.strerror
                                      + BOLD
                                      + ERROR
                                      + f"\nUnable to create directory at '{directory.absolute()}'!"
                                      + "\nPlease check your read/write policies!"
                                      + RESET)
            except Exception:
                print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                raise IOError(BOLD
                              + ERROR
                              + f"\nUnable to create directory at '{directory.absolute()}'!"
                              + "\nPlease check your read/write policies!"
                              + RESET)
        else:
            print(BOLD + SUCCESS + "OK!" + RESET, file=sys.stderr)

    # FILES
    for file_pair in FILES:
        print(console + f"Checking file: '{file_pair[1]}' ...", end="", file=sys.stderr)
        if not os.path.exists(file_pair[1]):
            print(WARNING + f"doesn't exist!" + RESET, file=sys.stderr)
            print(intend + f"Copying file ...", end="", file=sys.stderr)
            try:
                shutil.copy2(file_pair[0], file_pair[1])
                print(BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)
            except PermissionError as e:
                print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                raise PermissionError(e.strerror
                                      + BOLD
                                      + ERROR
                                      + f"\nUnable to copy file from"
                                      + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                                      + "\nPlease check your read/write policies!"
                                      + RESET)
            except Exception:
                print(BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                raise IOError(BOLD
                              + ERROR
                              + f"\nUnable to copy file from"
                              + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                              + "\nPlease check your read/write policies!"
                              + RESET)
        else:
            print(BOLD + SUCCESS + "OK!" + RESET, file=sys.stderr)

    _secret_key_check()

    time_difference = time.time() - start_time
    print(console + BOLD + SUCCESS + f"Checkup finished successfully in {time_difference:.4f} seconds!\n" + RESET,
          file=sys.stderr)

    print(console + "--- CHECKUP END ---\n", file=sys.stderr)
    print(setup + "--- SETUP START ---\n", file=sys.stderr)

    # NGINX CHECKS

    # check for root access
    is_already_sudo = False
    if _is_root():
        print(setup + "Detected root access!", file=sys.stderr)
        print(intend_setup + "Disabling root request!")
        sudo = ""
        is_already_sudo = True
    else:
        print(setup + "No root access detected!", file=sys.stderr)
        print(intend_setup + "Scheduling request for later!", file=sys.stderr)
        sudo = "sudo"

    # check if nginx is installed
    if not shutil.which("nginx"):
        raise FileNotFoundError("Looks like Nginx is not installed on this system :(\n\
                                Please install it to run Report-Booklet-Writer!")

    else:
        print(setup + "Nginx installation found!", file=sys.stderr)

    # copy config file for nginx
    for file_pair in NGINX_FILES:
        # TODO: do sth to unify this block with the other 3 very similar ones!
        print(setup + "Enabling Report-Booklet-Writer in nginx config:", file=sys.stderr)
        print(intend_setup + f"Checking file: '{file_pair[1]}' ...", end="", file=sys.stderr)
        if not os.path.exists(file_pair[1]):
            print(WARNING + f"doesn't exist!" + RESET, file=sys.stderr)
            if not _is_root():
                print(intend_setup + "Requesting root access!", file=sys.stderr)
                is_already_sudo = True
            else:
                print(intend_setup + "Skipping root request!")
            print(intend_setup + f"Copying file ...", file=sys.stderr)
            try:
                subprocess.Popen(f"{sudo} cp {file_pair[0]} {file_pair[1]}".split()).wait()
                print(intend_setup + BOLD + SUCCESS + "done!" + RESET, file=sys.stderr)
            except PermissionError as e:
                print(intend_setup + BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                raise PermissionError(e.strerror
                                      + BOLD
                                      + ERROR
                                      + f"\nUnable to copy file from"
                                      + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                                      + "\nPlease check your read/write policies!"
                                      + RESET)
            except Exception:
                print(intend_setup + BOLD + ERROR + "failed!" + RESET, file=sys.stderr)
                raise IOError(BOLD
                              + ERROR
                              + f"\nUnable to copy file from"
                              + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                              + "\nPlease check your read/write policies!"
                              + RESET)
        else:
            print(BOLD + SUCCESS + "enabled!" + RESET, file=sys.stderr)

    # checking if nginx is running (reloading the config)
    print(setup + "Checking status of nginx: ", end="", file=sys.stderr)
    if subprocess.Popen(f"systemctl is-active --quiet nginx".split()).wait() > 0:
        print(BOLD + "inactive!" + RESET, file=sys.stderr)
        # starting if not running
        print(intend_setup + "starting nginx!", file=sys.stderr)
        try:
            subprocess.Popen(f"{sudo} systemctl start nginx".split()).wait()
        except Exception:
            raise PermissionError("Failed to start Nginx!")
    else:
        print(BOLD + "active!" + RESET, file=sys.stderr)
        # restarting if already running
        print(intend_setup + "restarting nginx!", file=sys.stderr)
        try:
            subprocess.Popen(f"{sudo} systemctl restart nginx".split()).wait()
        except Exception:
            raise PermissionError("Failed to restart Nginx!")

    print("\n" + setup + "--- SETUP END ---\n", file=sys.stderr)

    # is_already_sudo is False, if user has not executed his password yet!
    if is_already_sudo:
        print("Requesting root access to execute server:", file=sys.stderr)
        # here continues the __init__ file!


checkup()
