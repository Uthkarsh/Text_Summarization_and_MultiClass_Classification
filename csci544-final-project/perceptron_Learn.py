import sys
import re
import os
from collections import namedtuple
from consolidate import preProcess

def getTuple(line):
	label = None
	tempList = list()
	for word in line.split():
		if label == None:
			label = word
			continue
		tempList.append(word)

	tuple = namedtuple('tuple',['label','words'])
	tuple.label = label
	tuple.words = tempList
	return tuple


# Builds the weight table for all the words in all the files after tokenizing them. 
def buildTable():
		#input = open("trainingData", "r");
	''' A dictionary for the table of features. The Key for the dictionary will be the 
	feature name and the value will be a named tuple. The tuples would have the name
	as the label names -- business, logistics and personal '''
	weightsTable = dict()

	fp = open("Consolidated.txt", "r")

	count = 0
	for line in fp:
		# call the preProcess function to tokenize the file
		count+=1
		tuple = getTuple(line);
		#print(tuple.words)
		for word in tuple.words:
			if word not in weightsTable.keys():
				# Add thd word to the table with all the label weights as zero
				tempTuple = namedtuple('labelsWeights', ['Business','Logistics','Personal'])
				tempTuple.Business = tempTuple.Logistics = tempTuple.Personal = 0
				weightsTable[word] = tempTuple

	print(count)

	fp.close()
		#break # For testing purposes, do it for only one file. Should Remove later. 

	# Finally return the weightstable to the calling function. 
	return weightsTable

# Parses the command line options and returns the corresponding maxIterations value. 
# By default, if nothing is specified, 5 is sent.
def getMaxIterations():
	if len(sys.argv) > 1:
		if sys.argv[1] == "-maxIterations" and len(sys.argv)>2:
			return int(sys.argv[2])
		else:
			print("Invalid Option")
			sys.exit()
	else:
		return 5

def main():

	#preProcess() # Need not be done every time. Can be gotten rid off once the consolidated file is built.

	maxIterations = getMaxIterations()
	weightsTable = buildTable()
	print(len(weightsTable.keys()))

	'''for key in weightsTable.keys():
		print(key)'''


if __name__ == "__main__":
	main()
