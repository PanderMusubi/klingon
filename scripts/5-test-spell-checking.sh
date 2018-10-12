if [ ! -e ../generated ]; then
	echo 'ERROR: Missing generated directory'
	exit 1
fi
cd ../generated

if [ ! -e ../test ]; then
	mkdir ../test
fi

if [ ! -e tlh_Latn.aff -a ! -e tlh_Latn.dic -a ! -e tlh.aff -a ! -e tlh.dic -a ! ../test/test_words.txt ]; then
	echo 'ERROR: Missing files tlh_Latn.aff, tlh_Latn.dic tlh.aff, tlh.dic or test_words.txt'
	exit 1
fi

echo 'INFO: Testing '`wc -l klingon-latin | awk '{print $1}'`' words from ../generated/klingon-latin'
hunspell -d ./tlh_Latn -a klingon-latin | grep '^#' > ../test/words-latin_incorrect.txt
echo 'INFO: '`wc -l ../test/words-latin_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/words-latin_incorrect.txt'

echo 'INFO: Testing '`wc -l klingon | awk '{print $1}'`' words from ../generated/klingon'
hunspell -d ./tlh -a klingon | grep '^#' > ../test/words_incorrect.txt
echo 'INFO: '`wc -l ../test/words_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/words_incorrect.txt'

echo 'INFO: Testing '`wc -l ../test/test_words-latin.txt | awk '{print $1}'`' words from ../test/test_words-latin.txt'
hunspell -d ./tlh_Latn -a ../test/test_words-latin.txt | grep '^#' > ../test/tests-latin_incorrect.txt
echo 'INFO: '`wc -l ../test/tests-latin_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/tests-latin_incorrect.txt'

echo 'INFO: Testing '`wc -l ../test/test_words.txt | awk '{print $1}'`' words from ../test/test_words.txt'
hunspell -d ./tlh -a ../test/test_words.txt | grep '^#' > ../test/tests_incorrect.txt
echo 'INFO: '`wc -l ../test/tests_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/tests_incorrect.txt'

#FIXME let apostrophe be recognized as a word character, via word chars or -1

cd ../scripts
