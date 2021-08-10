'''Generates files.'''

from datetime import datetime
from operator import itemgetter
from os.path import isfile
import sys
from xml.etree import ElementTree
from unicodedata import name
from _operator import pos
#import PyGnuplot

pure_alphabet = ('a', 'b', 'c', 'e', 'g', 'h', 'j', 'l', 'm', 'n', 'o', 'p',
                 'q', 'r', 't', 'u', 'v', 'w', 'y', "'", 'D', 'H', 'I', 'Q',
                 'S')
alphabet = ('a', 'b', 'c', 'e', 'g', 'h', 'j', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 't', 'u', 'v', 'w', 'y', "'", 'D', 'H', 'I', 'Q', 'S', ' ')
encountered_alphabet = {}

def validate(word, pos=None, id=None, pure=True):
    '''Validates word.'''
    if pure:
        for char in word:
            if char not in pure_alphabet:
                print('WARNING: Skipping word {} of PoS {} with id {} with forbidden character {} ({}) in pure mode'.format(word, pos, id, char, name(char)))
                return False
            if char in encountered_alphabet:
                encountered_alphabet[char] += 1
            else:
                encountered_alphabet[char] = 1
    else:
        for char in word:
            if char not in alphabet:
                print('WARNING: Skipping word {} of PoS {} with id {} with forbidden character {} ({}) not in pure mode'.format(word, pos, id, char, name(char)))
                return False
            if char in encountered_alphabet:
                encountered_alphabet[char] += 1
            else:
                encountered_alphabet[char] = 1
    return True

def parse(sentence):
    '''Parses sentence.'''
    words = []
    for word in sentence.replace(',', ' ').replace('...', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').replace('X', ' ').split(' '):
        if word:
            if word[0] == '-':
                print('WARNING: Omitting word starting with hyphen {} from sentence {}'.format(word, sentence))
            else:
                for w in word.split('-'):
                    if w and w not in words:
                        words.append(w)
    return words

def histogram(data, name):
    '''Prints histogram.'''
    print(name)
    for value, count in sorted(data.items(), key=itemgetter(1)):
        print('{}\t{}'.format(count, value))

# def graph_pie(data, name):
# 	x = list(data.keys())
# 	y = list(data.values())
# 	print(x)
# 	print(y)
# 	sum = 0
# 	for i in range(len(y)):
# 		sum += y[i]
# 	for i in range(len(y)):
# 		y[i] /= sum
# 	print(y)
# 	PyGnuplot.s([x, y])
# 	PyGnuplot.s('plot "tmp.dat" ')
	# https://stackoverflow.com/questions/31896718/generation-of-pie-chart-using-gnuplot

def flag(word, words, dikt, pos, id, prefix_flags=[], suffix_flags=[]):
    '''Creates flag.'''
    if not validate(word, pos, id, pure=False):
        return dikt
    if word not in words:
        words.append(word)
    flags = []
    if word in dikt:
        flags = dikt[word]
    for flag in prefix_flags:
        if flag not in flags:
            flags += flag
    for flag in suffix_flags:
        if flag not in flags:
            flags += flag
    dikt[word] = flags

    parts = word.split(' ')
    if len(parts) > 1:
        for i in range(len(parts)):
            if not validate(parts[i], pure=False):
                continue
            flags = []
            if parts[i] in dikt:
                flags = dikt[parts[i]]
            if i == 0:
                for flag in prefix_flags:
                    if flag not in flags:
                        flags += flag
            if i == len(parts) - 1:
                for flag in suffix_flags:
                    if flag not in flags:
                        flags += flag
            dikt[parts[i]] = flags

    return dikt

if not isfile('data.xml'):
    print('ERROR: Missing file data.xml')
    sys.exit(1)

words = []
tests = []
dikt = {}
prefixes = {}
suffixes = {}
root = ElementTree.parse('data.xml').getroot()
source_version = root.attrib['version']
for table in root[0]: # only one database
    id = None
    word = None
    pos = None
    prefix_flags = []
    suffix_flags = []
    for column in table:
        if column.attrib['name'] == '_id':
            id = column.text
            pos = None
            word = None
        elif column.attrib['name'] == 'entry_name':
            word = column.text
        elif column.attrib['name'] == 'part_of_speech':
            pos = column.text.split(':')[0]
            if pos == 'n':
                if 'pref' in column.text:
                    print('ERROR: nou prefix not yet supported')
                    sys.exit(1)
                elif 'suff' in column.text:
                    pos = '{}_'.format(pos)
                else:
                    suffix_flags.append('N')# no: -pu' -Du' -mey
                    if 'plural' not in column.text and 'inhpl' not in column.text:
                        if 'body' in column.text:
                            suffix_flags.append('O') # -pu'
                        if 'being' in column.text:
                            suffix_flags.append('E') # -Du'
                        if 'place' in column.text:
                            suffix_flags.append('L') # -mey
            elif pos == 'v':
                if 'pref' in column.text:
                    pos = '_{}'.format(pos)
                elif 'suff' in column.text:
                    pos = '{}_'.format(pos)
                prefix_flags.append('v')
                suffix_flags.append('V')

    if pos in ('n', 'v', 'adv', 'conj', 'ques', 'excl'):
        if '-' in word:
            print('WARNING: Omitting word with hyphen {} with id {} and pos {}'.format(word, id, pos))
        else:
            if pos == 'excl' and word[-1] in ('!', '?'):
                word = word[:-1]
            if pos != 'excl' or ' ' not in word:
                flag(word, words, dikt, pos, id, prefix_flags=prefix_flags, suffix_flags=suffix_flags)
    elif pos == 'sen':
        for w in parse(word):
            if w not in tests:
                tests.append(w)
    elif pos == 'n_':
        if word[0] == '-':
            word = word[1:]
        validate(word, pos, id)
        if word == "pu'":
            if 'O' not in suffixes:
                suffixes['O'] = [word]
        elif word == "Du'":
            if 'E' not in suffixes:
                suffixes['E'] = [word]
        elif word == 'mey':
            if 'L' not in suffixes:
                suffixes['L'] = [word]
        else:
            if 'N' in suffixes:
                suffixes['N'].append(word)
            else:
                suffixes['N'] = [word]
    elif pos == 'v_':
        if word[0] == '-':
            word = word[1:]
        validate(word, pos, id)
        if 'V' in suffixes:
            if word not in suffixes['V']:
                suffixes['V'].append(word)
        else:
            suffixes['V'] = [word]
    elif pos == '_v':
        if word == '0':
            continue
        if word[-1] == '-':
            word = word[:-1]
        validate(word, pos, id)
        if 'v' in prefixes:
            if word not in prefixes['v']:
                prefixes['v'].append(word)
        else:
            prefixes['v'] = [word]
    else:
        print('WARNING: Skipping unsupported pos {}'.format(pos))

#histogram(detailed_characters, 'detailed_characters')
#histogram(characters, 'characters')
#histogram(detailed_part_of_speechs, 'detailed_part_of_speechs')
#histogram(part_of_speechs, 'part_of_speechs')

aff = open('../generated/tlh_Latn.aff', 'w')  # pylint:disable=consider-using-with
aff.write('# Author: Pander <pander@users.sourceforge.net>\n')
aff.write('# License: Apache License 2.0\n')
aff.write('# Homepage: https://github.com/PanderMusubi/klingon\n')
version = None
control = open('../static/control-hunspell-tlh')  # pylint:disable=consider-using-with
for line in control:
    if 'Version' in line:
        version = (line.split(' ')[1]).strip()
if not version:
    print('ERROR: Could not determine version.')
    sys.exit(1)
aff.write('# Version: {}\n'.format(version))
aff.write('# Date: {}\n'.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
aff.write('# Source: build from boQwI\' version {}\n'.format(source_version))
aff.write('SET UTF-8\n')
if sorted(alphabet) != sorted(encountered_alphabet.keys()):
    print('ERROR: Did not encouter all expected letters from alphabet')
    sys.exit(1)
char_freq = sorted(encountered_alphabet.items(), key=itemgetter(1), reverse=True)
char_freq_sorted_alphabet = [x[0] for x in char_freq]
aff.write('TRY {}\n'.format((''.join(char_freq_sorted_alphabet)).replace(' ', '')))
# support apostrophe TODO Note below that WORDCHARS are being used! Discuss for Nuspell.
aff.write('WORDCHARS {}’\n'.format((''.join(alphabet)).replace(' ', '')))
aff.write('ICONV 1\n')
aff.write("ICONV ’ '\n")
# support QEWRTY and AZERTY keyboards
aff.write('KEY qwertyuiop|asdfghjkl|zxcvbnm|qawsedrftgyhujikolp'
          '|azsxdcfvgbhnjmk|aze|qsd|lm|wx|aqz|qws\n')
# suffixes
for flag, affixes in sorted(suffixes.items()):
    aff.write('SFX {} Y {}\n'.format(flag, len(affixes)))
    for affix in sorted(affixes):
        aff.write('SFX {} 0 {} .\n'.format(flag, affix))
# prefixes
for flag, affixes in sorted(prefixes.items()):
    aff.write('PFX {} Y {}\n'.format(flag, len(affixes)))
    for affix in sorted(affixes):
        aff.write('PFX {} 0 {} .\n'.format(flag, affix))

dic = open('../generated/tlh_Latn.dic', 'w')  # pylint:disable=consider-using-with
dic.write('{}\n'.format(len(dikt)))
for word, flags in sorted(dikt.items()):
    if flags:
        dic.write('{}/{}\n'.format(word, ''.join(flags)))
    else:
        dic.write('{}\n'.format(word))

tst = open('../generated/klingon-latin', 'w')  # pylint:disable=consider-using-with
for word in sorted(words):
    tst.write('{}\n'.format(word))

tst = open('../test/test_words-latin.txt', 'w')  # pylint:disable=consider-using-with
for word in sorted(tests):
    tst.write('{}\n'.format(word))
