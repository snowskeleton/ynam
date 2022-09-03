#!/usr/bin/env bash
#this needs to be run from the PARENT DIRECTORY, not the src/ directory

git clone https://github.com/snowskeleton/ynam.git
cd ynam
./install.sh
python3 src/ynam/quickstart.py
