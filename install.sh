#!/usr/bin/bash
apt-get install python3
apt-get install git
pip install git+https://github.com/Simatwa/undetected-chromedriver.git
python3 setup.py install
echo 'betika installed successfully!'
betika -v && betika -h