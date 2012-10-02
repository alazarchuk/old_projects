#!/bin/sh

export MOZILLA_FIVE_HOME=/usr/lib/firefox-2.0.0.16/

python "gtkmozemb.py"

echo "

------------------
(program exited with code: $?)" 		


echo "Press return to continue"
#to be more compatible with shells like dash
dummy_var=""
read dummy_var
rm $0
