if [ ! -e words.txt ]; then
	echo 'ERROR: Missing file words.txt'
	exit 1
fi
cp -f words.txt tlh_Latn.dic
