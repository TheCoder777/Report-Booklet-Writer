#!/bin/env bash
# WARNING: This script has to be executed as root!
# Otherwise the server won't work
# (uWSGI can't set socket permissions if not root => nginx can't access the socket)

# for some colored warnings
RED='\033[91m'
BOLD='\033[1m'
NORMAL='\033[0m'


start_fail() {
  echo -e "\n${BOLD}${RED}Server failed to start!${NORMAL}"
  printf "\n\tHere is a little checklist that might help you!"
  printf "\n\t - Check the python dependencies"
  printf "\n\t - Check socket permissions (/tmp/rbwriter.sock)"
  printf "\n\t - Check your nginx installation"
  printf "\n\t - Check your nginx config (/etc/nginx/nginx.conf)"
  printf "\n\t - Check nginx status ('systemctl status nginx' / 'journalctl -xe')\n\n"
  return
}

init_fail() {
  echo -e "\n${BOLD}${RED}Failed to initialize server directory!${NORMAL}"
  printf "\nCheck your permissions in this folder and try again!\n"
  return
}


cd /app/files || exit

echo "Preparing server directory ['rbwriter init']"
rbwriter init || { init_fail; exit 1; }

echo "Starting Server ['rbwriter start']"
rbwriter start || { start_fail; exit 1; }
