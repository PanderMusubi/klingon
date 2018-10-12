if [ ! -e ../download ]; then
	echo 'ERROR: Missing download directory'
	exit 1
fi
cd ../download

if [ ! -e klingon-assistant-data-master ]; then
	echo 'ERROR: Missing directory klingon-assistant-master'
	exit 1
fi
cat klingon-assistant-data-master/mem*.xml > data.xml

cd ../scripts
