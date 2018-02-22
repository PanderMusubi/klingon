from operator import itemgetter
from os.path import isfile
from xml.etree import ElementTree

if not isfile('data.xml'):
	print('ERROR: Missing file data.xml')
	exit(1)
	
def histogram(data, description):
	print(description)
	for value, count in sorted(data.items(), key=itemgetter(1)):
		print('{}\t{}'.format(count, value)) 

part_of_speechs = {}
detailed_part_of_speechs = {}
characters = {}
detailed_characters = {}
grphs = {}
	
root = ElementTree.parse('data.xml').getroot()
#print(root.tag, root.attrib)
for table in root[0]: # only one database
#		print(table.tag, table.attrib)
		for column in table:
#			print(column.tag, column.attrib)
			if column.attrib['name'] == 'entry_name':
#				print(column.text)
				for character in column.text:
					if character in detailed_characters:
						detailed_characters[character] += 1
					else:
						detailed_characters[character] = 1
				i = 0
				while i < len(column.text):
#					print(i, column.text[i:i+2])
					if i < len(column.text) - 1 and 'ch' == column.text[i:i+2]: 
						print(column.text)
					i += 1
#				exit(0)
#				if 'ngh' in column.text:
#					print(column.text)
			if column.attrib['name'] == 'part_of_speech':
				for part_of_speech in column.text.split(','): 
					if part_of_speech in detailed_part_of_speechs:
						detailed_part_of_speechs[part_of_speech] += 1
					else:
						detailed_part_of_speechs[part_of_speech] = 1
					part_of_speech = part_of_speech.split(':')[0] 
					if part_of_speech in part_of_speechs:
						part_of_speechs[part_of_speech] += 1
					else:
						part_of_speechs[part_of_speech] = 1

histogram(detailed_part_of_speechs, 'detailed_part_of_speechs')
histogram(part_of_speechs, 'part_of_speechs')
histogram(detailed_characters, 'detailed_characters')
histogram(characters, 'characters')


# 	sort | uniq >> words.txt
#TODO strip, no 0, no empty lines, no only space, etc
