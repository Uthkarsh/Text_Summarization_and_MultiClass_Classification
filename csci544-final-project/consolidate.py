'''
Author: Uthkarsh Satish
'''

import sys
import re
import os
from collections import namedtuple

''' Returns a tuple containing the label for the corresponding file and the tokenized words. '''
def preProcess_Helper(fp):
	label = None
	words = list()
	for tempWords in fp:
		for word in tempWords.split():
			if word == 'Business' or word == 'Logistics' or word == 'Personal':
				if label == None: # To make sure that the later text in the file do not change the actual label
					label = word
				continue
			temp = re.sub(r'[.|,|;|_|:|?|!|@|#|$|%|^|&|*|(|)|"|\'|/|\\|>|<|\-|=|+|\[|]|\}|\{|\~|\`',r'',word)
			temp = re.sub(r'[0-9]',r'',temp)
			if len(temp)!=0:
				words.append(temp.lower())

	tuple = namedtuple('tuple',['label','words'])
	tuple.label = label
	tuple.words = words
	return tuple

def preProcess():

	print("Pre Processing ...")
	path = "trainingData"
	files = sorted(os.listdir(path))

	# The file in which the consolidated and tokenized Emails with labels will be written to.
	oFile = open("Consolidated.txt",'w')

	# For the purpose of testing
	count = 0

	for fileName in files:
		fp = open(path+"/"+fileName)
		# call the preProcess function to tokenize the file
		tuple = preProcess_Helper(fp)	
		oFile.write(tuple.label+" ")

		for word in tuple.words:
			oFile.write(word+" ")

		oFile.write("\n")

		count+=1
		# Close each of the opened files
		fp.close()

	# Close the consolidated file
	oFile.close()
	#print(count)
	return