if [ ! -e build ]; then
	mkdir build
fi
cd build

if [ -e master.zip ]; then
	rm -f master.zip
fi
wget https://github.com/De7vID/klingon-assistant-data/archive/master.zip
if [ -e klingon-assistant-data-master ]; then
	rm -rf klingon-assistant-data-master
fi
unzip -q master.zip
if [ -e klingon-assistant-data-master ]; then
	rm -f master.zip
fi

cd ..
