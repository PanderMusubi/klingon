if [ ! -e klingon-assistant-master ]; then
	echo 'ERROR: Missing directory klingon-assistant-master'
	exit 1
fi
if [ -e words.txt ]; then
	rm -f words.txt
fi
for i in klingon-assistant-master/KlingonAssistant/data/mem*.xml; do
	grep '<column name="entry_name">' $i| \
	awk -F '>' '{print $2}'| \
	awk -F '<' '{print $1}' | \
	sort | uniq >> words.txt
done 
#TODO strip, no 0, no empty lines, no only space, etc
