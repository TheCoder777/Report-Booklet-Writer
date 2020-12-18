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
    print(console + f"Checking for secret key: '{SECRET_KEY}' ...", end="")
    if not os.path.isfile(SECRET_KEY):
        print(WARNING + "not found!" + RESET)
        print(intend + f"Secret key doesn't exist, generating...", end="")
        try:
            _gen_secret_key()
            print(BOLD + SUCCESS + "done!" + RESET)
        except PermissionError as e:
            print(BOLD + ERROR + "failed!" + RESET)
            raise PermissionError(e.strerror
                                  + BOLD
                                  + ERROR
                                  + f"\nUnable to write secret key to '{SECRET_KEY.absolute()}'!\n"
                                  + "Application is unusable without a secret key, check your read/write policies!"
                                  + RESET)
        # except anything else (has to be some IO stuff):
        except Exception:
            print(BOLD + ERROR + "failed!" + RESET)
            raise IOError(BOLD
                          + ERROR
                          + f"\nUnable to write secret key to '{SECRET_KEY.absolute()}'!\n"
                          + "Application is unusable without a secret key, check your read/write policies!"
                          + RESET)
    else:
        print(BOLD + SUCCESS + "OK!" + RESET)


def checkup():
    """
    This checkup makes sure that everything is in place when the server starts
    and also fixes it, if anything goes wrong!
    """
    checkup_start_time = time.time()

    # DIRECTORIES
    for directory in DIRECTORIES:
        print(console + f"Checking directory: '{directory}' ...", end="")
        if not os.path.isdir(directory):
            print(WARNING + f"doesn't exist!" + RESET)
            print(intend + "Creating directory ...", end="")
            try:
                os.makedirs(directory, exist_ok=True)
                print(BOLD + SUCCESS + "done!" + RESET)
            except PermissionError as e:
                print(BOLD + ERROR + "failed!" + RESET)
                raise PermissionError(e.strerror
                                      + BOLD
                                      + ERROR
                                      + f"\nUnable to create directory at '{directory.absolute()}'!"
                                      + "\nPlease check your read/write policies!"
                                      + RESET)
            except Exception:
                print(BOLD + ERROR + "failed!" + RESET)
                raise IOError(BOLD
                              + ERROR
                              + f"\nUnable to create directory at '{directory.absolute()}'!"
                              + "\nPlease check your read/write policies!"
                              + RESET)
        else:
            print(BOLD + SUCCESS + "OK!" + RESET)

    # FILES
    for file_pair in FILES:
        print(console + f"Checking file: '{file_pair[1]}' ...", end="")
        if not os.path.exists(file_pair[1]):
            print(WARNING + f"doesn't exist!" + RESET)
            print(intend + f"Copying file ...", end="")
            try:
                shutil.copy2(file_pair[0], file_pair[1])
                print(BOLD + SUCCESS + "done!" + RESET)
            except PermissionError as e:
                print(BOLD + ERROR + "failed!" + RESET)
                raise PermissionError(e.strerror
                                      + BOLD
                                      + ERROR
                                      + f"\nUnable to copy file from"
                                      + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                                      + "\nPlease check your read/write policies!"
                                      + RESET)
            except Exception:
                print(BOLD + ERROR + "failed!" + RESET)
                raise IOError(BOLD
                              + ERROR
                              + f"\nUnable to copy file from"
                              + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                              + "\nPlease check your read/write policies!"
                              + RESET)
        else:
            print(BOLD + SUCCESS + "OK!" + RESET)

    _secret_key_check()

    checkup_time_difference = time.time() - checkup_start_time
    print(console + BOLD + SUCCESS + f"Checkup finished successfully in {checkup_time_difference:.4f} seconds!\n" + RESET,
          file=sys.stderr)

    # NGINX CHECKS
    setup_start_time = time.time()

    # check for root access
    is_already_sudo = False
    if _is_root():
        print(setup + "Detected root access!")
        print(intend_setup + "Disabling root request!")
        sudo = ""
        is_already_sudo = True
    else:
        print(setup + "No root access detected!")
        print(intend_setup + "Scheduling request for later!")
        sudo = "sudo"

    # check if Nginx is installed
    if not shutil.which("nginx"):
        raise FileNotFoundError("Looks like Nginx is not installed on this system :(\n\
                                Please install it to run Report-Booklet-Writer!")

    else:
        print(setup + "Nginx installation found!")

    # copy config file for nginx
    for file_pair in NGINX_FILES:
        # TODO: do sth to unify this block with the other 3 very similar ones!
        print(setup + "Enabling Report-Booklet-Writer in Nginx configuration:")
        print(intend_setup + f"Checking file: '{file_pair[1]}' ...", end="")
        if not os.path.exists(file_pair[1]):
            print(WARNING + f"doesn't exist!" + RESET)
            if not _is_root():
                print(intend_setup + "Requesting root access!")
                is_already_sudo = True
            else:
                print(intend_setup + "Skipping root request!")
            print(intend_setup + f"Copying file ...")
            try:
                subprocess.Popen(f"{sudo} cp {file_pair[0]} {file_pair[1]}".split()).wait()
                print(intend_setup + BOLD + SUCCESS + f"Successfully copied file: '{file_pair[1]}'!" + RESET)
            except PermissionError as e:
                raise PermissionError(e.strerror
                                      + BOLD
                                      + ERROR
                                      + f"\nUnable to copy file from"
                                      + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                                      + "\nPlease check your read/write policies!"
                                      + RESET)
            except Exception:
                raise IOError(BOLD
                              + ERROR
                              + f"\nUnable to copy file from"
                              + f"'{file_pair[0].absolute()}' to '{file_pair[1].absolute()}'!"
                              + "\nPlease check your read/write policies!"
                              + RESET)
        else:
            print(BOLD + SUCCESS + "enabled!" + RESET)

    # checking if Nginx is running (reloading the config)
    print(setup + "Checking status of Nginx: ", end="")
    if subprocess.Popen(f"systemctl is-active --quiet nginx".split()).wait() > 0:
        print(BOLD + "inactive!" + RESET)
        # starting if not running
        print(intend_setup + "Starting Nginx!")
        try:
            subprocess.Popen(f"{sudo} systemctl start nginx".split()).wait()
        except Exception:
            raise PermissionError("Failed to start Nginx!")
    else:
        print(BOLD + "active!" + RESET)
        # restarting if already running
        print(intend_setup + "Restarting Nginx!")
        try:
            subprocess.Popen(f"{sudo} systemctl restart nginx".split()).wait()
        except Exception:
            raise PermissionError("Failed to restart Nginx!")

    setup_time_difference = time.time() - setup_start_time
    print(setup + BOLD + SUCCESS + f"Setup finished successfully in {setup_time_difference:.4f} seconds!\n" + RESET,
          file=sys.stderr)

    complete_time_difference = checkup_time_difference + setup_time_difference

    print(BOLD + f"Everything took about {complete_time_difference:.4f} seconds!" + RESET)

    if complete_time_difference < 0.04:
        print(BOLD + SUCCESS + "Wow, that was a split second! Did you even see that?" + RESET)

    print("\n" + BOLD + SUCCESS + "=> Ready to go :D" + RESET + "\n")

    print(BOLD + "You can now checkout http://localhost:80 to use Report-Booklet-Writer!" + RESET + "\n")

    # is_already_sudo is False, if user has not executed his password yet!
    # TODO: doesn't work when user is in 'sudo timeout mode'
    # (user has already entered his password for sth else a few minutes ago)
    if not _is_root() and is_already_sudo:
        print("Requesting root access to execute server:")
        # here continues the __init__ file!


checkup()
