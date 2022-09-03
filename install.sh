#!/usr/bin/env bash
DEST="/usr/local/bin/ynam"
LIB="/usr/lib/ynam"

pip install -r requirements.txt

while getopts u flag; do
  update=1
done
while getopts r flag; do
  remove=1
  update=1
done

# wipe old install
sudo rm -rf ${LIB}
sudo rm -rf ${DEST}

if [[ $remove -ne 1 ]]; then
  sudo cp -r $(pwd) ${LIB}
  sudo ln -s ${LIB}/src/ynam/main.py ${DEST}
  sudo chmod 755 ${DEST}
  echo Finished
fi
