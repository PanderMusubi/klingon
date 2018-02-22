from operator import itemgetter
from os.path import isfile
from xml.etree import ElementTree
import PyGnuplot

if not isfile('data.xml'):
	print('ERROR: Missing file data.xml')
	exit(1)
	
def histogram(data, name):
	print(name)
	for value, count in sorted(data.items(), key=itemgetter(1)):
		print('{}\t{}'.format(count, value)) 

def graph_pie(data, name):
	x = list(data.keys())
	y = list(data.values())
	print(x)
	print(y)
	sum = 0
	for i in range(len(y)):
		sum += y[i]
	for i in range(len(y)):
		y[i] /= sum
	print(y)
	PyGnuplot.s([x, y])
	PyGnuplot.s('plot "tmp.dat" ')
	# https://stackoverflow.com/questions/31896718/generation-of-pie-chart-using-gnuplot

part_of_speechs = {}
detailed_part_of_speechs = {}
characters = {}
detailed_characters = {}
grphs = {}

root = ElementTree.parse('data.xml').getroot()
for table in root[0]: # only one database
		for column in table:
			if column.attrib['name'] == 'entry_name':
				for character in column.text:
					if character in detailed_characters:
						detailed_characters[character] += 1
					else:
						detailed_characters[character] = 1
#				i = 0
#				while i < len(column.text):
#					print(i, column.text[i:i+2])
#					if i < len(column.text) - 1 and 'ch' == column.text[i:i+2]: 
#						print(column.text)
#					i += 1
#				exit(0)
#				if 'ngh' in column.text:
#					print(column.text)
			if column.attrib['name'] == 'part_of_speech':
				part_of_speech = column.text 
				if part_of_speech in detailed_part_of_speechs:
					detailed_part_of_speechs[part_of_speech] += 1
				else:
					detailed_part_of_speechs[part_of_speech] = 1
				part_of_speech = column.text.split(':')[0] 
				if part_of_speech in part_of_speechs:
					part_of_speechs[part_of_speech] += 1
				else:
					part_of_speechs[part_of_speech] = 1

#histogram(detailed_characters, 'detailed_characters')
#histogram(characters, 'characters')
histogram(detailed_part_of_speechs, 'detailed_part_of_speechs')
histogram(part_of_speechs, 'part_of_speechs')

nouns = []
verbs = []
adverbs = []
tests = []
noun_suffixes = []
verb_suffixes = []
verb_prefixes = []
root = ElementTree.parse('data.xml').getroot()
for table in root[0]: # only one database
		id = None
		name = None
		for column in table:
			if column.attrib['name'] == '_id':
				id = column.text
			elif column.attrib['name'] == 'entry_name':
				name = column.text
			elif column.attrib['name'] == 'part_of_speech':
				for part_of_speech in column.text.split(','): 
					if 'n' == part_of_speech[0] and 'suff' not in part_of_speech and 'pref' not in part_of_speech:
						if name in nouns:
							print('ERROR: Duplicate noun {}'.format(name))
						elif ' ' in name: 
							print('WARNING: Omitting noun with space {}'.format(name))
						else:
							nouns.append(name)
					elif 'v' == part_of_speech[0] and 'suff' not in part_of_speech and 'pref' not in part_of_speech:
						if name in verbs:
							print('ERROR: Duplicate verb {}'.format(name)) 
						elif ' ' in name: 
							print('WARNING: Omitting verb with space {}'.format(name))
						else:
							verbs.append(name)
					elif 'adv' == part_of_speech[:3]:
						if name in verbs:
							print('ERROR: Duplicate adverb {}'.format(name)) 
						elif ' ' in name: 
							print('WARNING: Omitting adverb with space {}'.format(name))
						else:
							adverbs.append(name)
					elif 'sen' == part_of_speech[:3]:
						words = name.replace(',', ' ').replace('...', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').replace('X', ' ').split(' ')
						for word in words:
							if '' != word:
								if '-' == word[0]:
									print('WARNING: Omitting word strating with hyphen {} from sentence {}'.format(word, name))
								else:
									ws = word.split('-')
									for w in ws:
										if '' != w and w not in tests:
											tests.append(w)
					elif 'n:suff' == part_of_speech:
						if '-' == name[0]:
							name = name[1:] 
						if name in verb_prefixes:
							print('ERROR: Duplicate noun suffix {}'.format(name)) 
						else:
							noun_suffixes.append(name)
					elif 'v:suff' == part_of_speech:
						if '-' == name[0]:
							name = name[1:] 
						if name in verb_prefixes:
							print('ERROR: Duplicate verb suffix {}'.format(name)) 
						else:
							verb_suffixes.append(name)
					elif 'v:pref' == part_of_speech:
						if '-' == name[-1]:
							name = name[:-1] 
						if name in verb_prefixes:
							print('ERROR: Duplicate verb prefix {}'.format(name)) 
						else:
							verb_prefixes.append(name)

aff = open('tlh_Latn.aff', 'a')
aff.write('# noun suffixes\n')
aff.write('SFX N Y {}\n'.format(len(noun_suffixes)))
for affix in sorted(noun_suffixes):
	aff.write('SFX N 0 {} .\n'.format(affix))
aff.write('# verb suffixes\n')
aff.write('SFX V Y {}\n'.format(len(verb_suffixes)))
for affix in sorted(verb_suffixes):
	aff.write('SFX V 0 {} .\n'.format(affix))
aff.write('# verb prefixes\n')
aff.write('PFX v Y {}\n'.format(len(verb_prefixes)))
for affix in sorted(verb_prefixes):
	aff.write('PFX v 0 {} .\n'.format(affix))

dic = open('tlh_Latn.dic', 'w')
dic.write('{}\n'.format(len(nouns)+len(verbs)))
dic.write('# nouns ({})\n'.format(len(nouns)))
for word in sorted(nouns):
	dic.write('{}/N\n'.format(word))
dic.write('# verbs ({})\n'.format(len(verbs)))
for word in sorted(verbs):
	dic.write('{}/Vv\n'.format(word))
dic.write('# adverbs ({})\n'.format(len(adverbs)))
for word in sorted(adverbs):
	dic.write('{}\n'.format(word))

tst = open('tests.txt', 'w')
for word in sorted(nouns + verbs + adverbs + tests):
	tst.write('{}\n'.format(word))

#print(verb_suffixes)

# 	sort | uniq >> words.txt
#TODO strip, no 0, no empty lines, no only space, etc
