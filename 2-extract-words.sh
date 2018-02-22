if [ ! -e klingon-assistant-master ]; then
	echo 'ERROR: Missing directory klingon-assistant-master'
	exit 1
fi
cp -f tlh_Latn.aff.template tlh_Latn.aff
cat klingon-assistant-master/KlingonAssistant/data/mem*.xml > data.xml
python3 2-extract-words.py
