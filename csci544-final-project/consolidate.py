'''
Author: Uthkarsh Satish
'''


import sys
import re
import os
from collections import namedtuple

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

''' 
OFName -> The Output File Name for the modified file
IFName -> The Input File Name from which we have to extract the tokens
bigrams -> False or True, indicating wheather the bigrams have to be included
trigrams -> False or True, indicating whether the trigrams have to be included
'''
def preProcess_Experimentation(IFName,OFName,bigrams,trigrams):

	if bigrams == 0 and trigrams == 0:
		print("Nothing to be changed in the preProcess_Experimentation")
		sys.exit()

	iFp = open(IFName, "r")
	oFp = open(OFName, "w")



	for line in iFp:

		# Good practice to use a list of strings for the purpse of building a string.
		# Cancatentation of strings are expensice, hence, this is a more pythonic way to do things. 
		str_list = list()

		tuple = getTuple(line)

		str_list.append(tuple.label)
		str_list.append(" ")

		prev = curr = None

		if trigrams:
			prev2 = None

		for word in tuple.words:

			# Irrespective, you have to write the word

			str_list.append(word+" ")

			if prev == None:
				if curr == None:

					 #It means that this is the first Iteration
					 curr = word
				else:

					# It comes here if it is the second iteration
					prev = curr
					curr = word

					if(bigrams==True):
						str_list.append("bi_"+prev+"_"+curr+" ")

				continue

			if bigrams == True:
				prev = curr
				curr = word
				str_list.append("bi_"+prev+"_"+curr+" ")

			if trigrams == True:

				prev2 = prev
				prev = curr
				curr = word

				str_list.append("tri_"+prev2+"_"+prev+"_"+curr+" ")
		# Join the list into a single string
		str = ''.join(str_list)
		# Strip the string of trailing spaces
		str = str.strip()
		# Add a newline character
		str+="\n"

		oFp.write(str)

	oFp.close()
	iFp.close()



			






