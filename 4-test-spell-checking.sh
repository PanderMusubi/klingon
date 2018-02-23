if [ ! -e tlh_Latn.aff -a ! -e tlh_Latn.dic -a ! tests.txt ]; then
	echo 'ERROR: Missing files tlh_Latn.aff, tlh_Latn.dic or tests.txt'
	exit 1
fi
echo 'INFO: Testing '`wc -l klingon-latin | awk '{print $1}'`' words'
hunspell -d tlh_Latn -a klingon-latin | grep '^#' > tests_incorrext.txt
echo 'INFO: '`wc -l tests_incorrext.txt | awk '{print $1}'`' words are incorrect'
#FIXME let apostrophe be recognized as a word character
