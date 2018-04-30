if [ ! -e build ]; then
	echo 'ERROR: Missing build directory'
	exit 1
fi
cd build

if [ ! -e klingon-assistant-data-master ]; then
	echo 'ERROR: Missing directory klingon-assistant-master'
	exit 1
fi
cat klingon-assistant-data-master/mem*.xml > data.xml

cd ..
