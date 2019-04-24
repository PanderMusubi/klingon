#!/usr/bin/env sh

if [ ! -e ../download ]; then
	echo 'ERROR: Missing download directory'
	exit 1
fi
cd ../download

if [ ! -e data.xml ]; then
	echo 'ERROR: Missing XML data file'
	exit 1
fi

if [ ! -e ../generated ]; then
	mkdir ../generated
fi
if [ ! -e ../test ]; then
	mkdir ../test
fi
python3 ../scripts/3-generate-files.py

cd ../scripts
