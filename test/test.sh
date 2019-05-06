#!/bin/sh
cp ../api_key api_key
cp inputfile_daily.json inputfile.json
python ../collect.py
cp inputfile_hourly.json inputfile.json
python ../collect.py
rm inputfile.json
rm api_key
