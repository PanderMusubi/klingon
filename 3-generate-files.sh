if [ ! -e build ]; then
	echo 'ERROR: Missing build directory'
	exit 1
fi
cd build

if [ ! -e data.xml ]; then
	echo 'ERROR: Missing directory klingon-assistant-master'
	exit 1
fi
python3 ../3-generate-files.py

cd ..
