#!/usr/bin/bash
apt-get install python3
python3 setup.py install
echo 'betika installed successfully!'
betika -v && betika -h