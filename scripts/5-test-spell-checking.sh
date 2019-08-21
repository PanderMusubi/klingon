#!/usr/bin/env sh

if [ ! `which hunspell` ]; then
	echo 'ERROR: Missing Hunspell, please install'
	exit 1
fi
#if [ ! `which nuspell` ]; then
#	echo 'ERROR: Missing Nuspell, please install'
#	exit 1
#fi

if [ ! -e ../generated ]; then
	echo 'ERROR: Missing generated directory'
	exit 1
fi
cd ../generated

if [ ! -e ../test ]; then
	mkdir ../test
fi

if [ ! -e tlh_Latn.aff -a ! -e tlh_Latn.dic -a ! -e tlh.aff -a ! -e tlh.dic -a ! ../test/test_words.txt ]; then
	echo 'ERROR: Missing files tlh_Latn.aff, tlh_Latn.dic, tlh.aff, tlh.dic or test_words.txt'
	exit 1
fi

echo 'INFO: Testing '`wc -l klingon-latin | awk '{print $1}'`' words from ../generated/klingon-latin'
hunspell -d tlh_Latn -a klingon-latin | grep '^#' > ../test/hunspell-words-latin_incorrect.txt
echo 'INFO: Hunspell '`wc -l ../test/hunspell-words-latin_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/hunspell-words-latin_incorrect.txt'
if [ `which nuspell` ]; then
	nuspell -d tlh_Latn klingon-latin 2>/dev/null | grep '^#' > ../test/nuspell-words-latin_incorrect.txt
	echo 'INFO: Nuspell '`wc -l ../test/nuspell-words-latin_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/nuspell-words-latin_incorrect.txt'
fi

echo 'INFO: Testing '`wc -l klingon | awk '{print $1}'`' words from ../generated/klingon'
hunspell -d tlh -a klingon | grep '^#' > ../test/hunspell-words_incorrect.txt
echo 'INFO: Hunspell '`wc -l ../test/hunspell-words_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/hunspell-words_incorrect.txt'
if [ `which nuspell` ]; then
	nuspell -d tlh klingon 2>/dev/null | grep '^#' > ../test/nuspell-words_incorrect.txt
	echo 'INFO: Nuspell '`wc -l ../test/nuspell-words_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/nuspell-words_incorrect.txt'
fi

echo 'INFO: Testing '`wc -l ../test/test_words-latin.txt | awk '{print $1}'`' words from ../test/test_words-latin.txt'
hunspell -d tlh_Latn -a ../test/test_words-latin.txt | grep '^#' > ../test/hunspell-tests-latin_incorrect.txt
echo 'INFO: Hunspell '`wc -l ../test/hunspell-tests-latin_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/hunspell-tests-latin_incorrect.txt'
if [ `which nuspell` ]; then
	nuspell -d tlh_Latn ../test/test_words-latin.txt 2>/dev/null | grep '^#' > ../test/nuspell-tests-latin_incorrect.txt
	echo 'INFO: Nuspell '`wc -l ../test/nuspell-tests-latin_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/nuspell-tests-latin_incorrect.txt'
fi

echo 'INFO: Testing '`wc -l ../test/test_words.txt | awk '{print $1}'`' words from ../test/test_words.txt'
hunspell -d tlh -a ../test/test_words.txt | grep '^#' > ../test/hunspell-tests_incorrect.txt
echo 'INFO: Hunspell '`wc -l ../test/hunspell-tests_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/hunspell-tests_incorrect.txt'
if [ `which nuspell` ]; then
	nuspell -d tlh ../test/test_words.txt 2>/dev/null | grep '^#' > ../test/nuspell-tests_incorrect.txt
	echo 'INFO: Nuspell '`wc -l ../test/nuspell-tests_incorrect.txt | awk '{print $1}'`' words are incorrect, see ../test/nuspell-tests_incorrect.txt'
fi

#FIXME let apostrophe be recognized as a word character, via word chars or -1

cd ../scripts
