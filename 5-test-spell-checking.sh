if [ ! -e tlh_Latn.aff -a ! -e tlh_Latn.dic -a ! tests.txt ]; then
	echo 'ERROR: Missing files tlh_Latn.aff, tlh_Latn.dic or tests.txt'
	exit 1
fi
echo 'INFO: Testing '`wc -l tests.txt`' number of words'
echo 'INFO: '`hunspell -d tlh_Latn -a tests.txt | grep '^#' | wc -l`' test words are incorrect'
#FIXME let apostrophe be recognized as a word character
