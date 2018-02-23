if [ ! -e build ]; then
	mkdir build
fi
cd build

if [ -e master.zip ]; then
	rm -f master.zip
fi
wget https://github.com/De7vID/klingon-assistant/archive/master.zip
if [ -e klingon-assistant-master ]; then
	rm -rf klingon-assistant-master
fi
unzip -q master.zip
if [ -e klingon-assistant-master ]; then
	rm -f master.zip
fi

cd ..
