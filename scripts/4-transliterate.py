#!/usr/bin/env python3

from unicodedata import category, name

# Transliteration table:
# 0 Latin script
# 1 Klingon script
# 2 Latin script uppercase???
# 3 Unicode codepoint
# 4 glyph name
# 5 Klingon spelling 
transliteration = {
	'a': ('', 'A', 'f8d0', 'Klingon letter a', 'at'),
	'b': ('', 'B', 'f8d1', 'Klingon letter b', 'bay'),
	'ch': ('', 'C', 'f8d2', 'Klingon letter ch', 'chay'),
	'D': ('', 'D', 'f8d3', 'Klingon letter D', 'Day'),
	'e': ('', 'E', 'f8d4', 'Klingon letter E', 'et'),
	'gh': ('', 'G', 'f8d5', 'Klingon letter gh', 'ghay'),
	'H': ('', 'H', 'f8d6', 'Klingon letter H', 'Hay'),
	'I': ('', 'I', 'f8d7', 'Klingon letter I', 'It'),
	'j': ('', 'J', 'f8d8', 'Klingon letter j', 'jay'),
	'l': ('', 'L', 'f8d9', 'Klingon letter l', 'lay'),
	'm': ('', 'M', 'f8da', 'Klingon letter m', 'may'),
	'n': ('', 'N', 'f8db', 'Klingon letter n', 'nay'),
	'ng': ('', 'F', 'f8dc', 'Klingon letter ng', 'ngay'),
	'o': ('', 'O', 'f8dd', 'Kliongon letter o', 'ot'),
	'p': ('', 'P', 'f8de', 'Klingon letter p', 'pay'),
	'q': ('', 'K', 'f8df', 'Klingon letter q', 'qay'),
	'Q': ('', 'Q', 'f8e0', 'Klingon letter Q', 'Qay'),
	'r': ('', 'R', 'f8e1', 'Klingon letter r', 'ray'),
	'S': ('', 'S', 'f8e2', 'Klingon letter S', 'Say'),
	't': ('', 'T', 'f8e3', 'Klingon letter t', 'tay'),
	'tlh': ('', 'X', 'f8e4', 'Klingon letter tlh', 'tlhay'),
	'u': ('', 'U', 'f8e5', 'Klingon letter u', 'ut'),
	'v': ('', 'V', 'f8e6', 'Klingon letter v', 'vay'),
	'w': ('', 'W', 'f8e7', 'Klingon letter w', 'way'),
	'y': ('', 'Y', 'f8e8', 'Klingon letter y', 'yay'),
	'\'': ('', '\'', 'f8e9', 'Klingon letter glottal stop', 'qaghwI'),
	'0': ('', '0', 'f8f0', 'Klingon digit zero', ''),
	'1': ('', '1', 'f8f1', 'Klingon digit one', ''),
	'2': ('', '2', 'f8f2', 'Klingon digit two', ''),
	'3': ('', '3', 'f8f3', 'Klingon digit three', ''),
	'4': ('', '4', 'f8f4', 'Klingon digit four', ''),
	'5': ('', '5', 'f8f5', 'Klingon digit five', ''),
	'6': ('', '6', 'f8f6', 'Klingon digit six', ''),
	'7': ('', '7', 'f8f7', 'Klingon digit seven', ''),
	'8': ('', '8', 'f8f8', 'Klingon digit eight', ''),
	'9': ('', '9', 'f8f9', 'Klingon digit nine', ''),
	',': ('', ',', 'f8fd', 'Klingon comma', ''),
	'.': ('', '.', 'f8fe', 'Klingon full stop', ''),
	'☠️': ('', '', 'f8ff', 'Klingon mummification glyph', ''),
	}

max_length = 0
for key in transliteration:
	length = len(key)
	if length > max_length:
		max_length = length

def transliterate(string):
	for length in reversed(range(1, max_length + 1)):
		for key, value in sorted(transliteration.items()):
			if len(key) != length:
				continue
			string = string.replace(key, value[0])
	return string

# word list
latin = open('../generated/klingon-latin')
klingon = open('../generated/klingon', 'w')
for line in latin:
	klingon.write('{}\n'.format(transliterate(line[:-1])))

# test words
latin = open('../test/test_words-latin.txt')
klingon = open('../test/test_words.txt', 'w')
for line in latin:
	klingon.write('{}\n'.format(transliterate(line[:-1])))

# affix file
latin = open('../generated/tlh_Latn.aff')
klingon = open('../generated/tlh.aff', 'w')
options = set()
for line in latin:
	line = line[:-1]
	# omit keyboard related options
	if line.startswith('KEY ') or line.startswith('ICONV '):
		continue
	if line.startswith('TRY ') or line.startswith('WORDCHARS '):
		for key in ('TRY ', 'WORDCHARS '):
			if line.startswith(key): 
				klingon.write('{}{}\n'.format(key, transliterate(line[len(key):])))
				continue
	elif line.startswith('PFX ') or line.startswith('SFX '):
		for key in ('PFX ', 'SFX '):
			if line.startswith(key):
				keylabel = key + line.split(' ')[1]
				if keylabel in options:
					values = line[len(key):].split(' ')
					values[2] = transliterate(values[2])
					klingon.write('{}{}\n'.format(key, ' '.join(values)))
				else: 
					klingon.write('{}\n'.format(line))
					options.add(keylabel)
				continue
	else:
		klingon.write('{}\n'.format(line))
	
#dictionary file
latin = open('../generated/tlh_Latn.dic')
klingon = open('../generated/tlh.dic', 'w')
first = True
for line in latin:
	line = line[:-1]
	# do not transliterate number of words
	if first:
		klingon.write('{}\n'.format(line))
		first = False
		continue
	flags = None
	if '/' in line:
		line, flags = line.split('/')
	if flags:
		klingon.write('{}/{}\n'.format(transliterate(line), flags))
	else:
		klingon.write('{}\n'.format(transliterate(line)))
