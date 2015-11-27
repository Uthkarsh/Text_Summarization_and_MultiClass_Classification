import sys
import re
import os
from collections import namedtuple

''' Returns a tuple containing the label for the corresponding file and the tokenized words. '''
def preProcess(fp):
	label = None
	words = list()
	for tempWords in fp:
		for word in tempWords.split():
			if word == 'Business' or word == 'Logistics' or word == 'Personal':
				if label == None: # To make sure that the later text in the file do not change the actual label
					label = word
				continue
			temp = re.sub(r'[.|,|;|_|:|?|!|@|#|$|%|^|&|*|(|)|"|\'|/|\\|>|<|\-|=|+|\[|]|\}|\{',r'',word)
			temp = re.sub(r'[0-9]',r'',temp)
			if len(temp)!=0:
				words.append(temp.lower())

	tuple = namedtuple('tuple',['label','words'])
	tuple.label = label
	tuple.words = words
	return tuple


# Builds the weight table for all the words in all the files after tokenizing them. 
def buildTable():
		#input = open("trainingData", "r");
	''' A dictionary for the table of features. The Key for the dictionary will be the 
	feature name and the value will be a named tuple. The tuples would have the name
	as the label names -- business, logistics and personal '''
	weightsTable = dict()
	path = "trainingData"
	files = sorted(os.listdir(path))
	for fileName in files:
		fp = open(path+"/"+fileName)
		# call the preProcess function to tokenize the file
		tuple = preProcess(fp)

		for word in tuple.words:
			if word not in weightsTable:
				# Add thd word to the table with all the label weights as zero
				tempTuple = namedtuple('labelsWeights', ['Business','Logistics','Personal'])
				tempTuple.Business = tempTuple.Logistics = tempTuple.Personal = 0
				weightsTable[word] = tempTuple
		fp.close()
		#break # For testing purposes, do it for only one file. Should Remove later. 

	# Finally return the weightstable to the calling function. 
	return weightsTable


def main():
	weightsTable = buildTable()
	for key in weightsTable.keys():
		print(key)

if __name__ == "__main__":
	main()
