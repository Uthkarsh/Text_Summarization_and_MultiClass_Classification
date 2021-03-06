'''
Author: Uthkarsh Satish


Description: Contains the code for the multiclass perceptron learner. The main function
calls the required functions and prints each step. 

Usage: python3 perceptron_Learn.py [-maxIterations number]

The maxIterations option is optional. 

For the purpse of debugging, the "weightsTable" file can be checked. It has the entire weightsTable
Printed. 

The multiple Iterations have been incorporated. 

Performance increase form 1 to 2 iterations is 40 (963-923) labels. 

Ex: 
python3 perceptron_Learn.py -maxIterations 2

python3 perceptron_Learn.py -maxIterations 2 --experiment



'''

import sys
import re
import os
import math
from collections import namedtuple
from consolidate import preProcess
from consolidate import preProcess_Experimentation

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
def buildTable(IFname):
		#input = open("trainingData", "r");
	''' A dictionary for the table of features. The Key for the dictionary will be the 
	feature name and the value will be a named tuple. The tuples would have the name
	as the label names -- business, logistics and personal '''
	weightsTable = dict()

	fp = open(IFname, "r")

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

	print("Number of lines processed =",count)

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

# Correct the weights of the labels depending upon the wrongly predicted label.
def correctWeights(weightstable,tuple,predictedLable):
	# Decrement the wrongly predicted label's weight by 1 and increment the correct label's by 1
	for word in tuple.words:
		# Could not find a better way to do this. Should be made more elegantly later. 
		if predictedLable == 'Business':
			weightstable[word].Business-=1
		elif predictedLable == 'Logistics':
			weightstable[word].Logistics-=1
		else:
			weightstable[word].Personal-=1

		if tuple.label == 'Business':
			weightstable[word].Business+=1
		elif tuple.label == 'Logistics':
			weightstable[word].Logistics+=1
		else:
			weightstable[word].Personal+=1
		#getattr(weightstable[word],predictedLable)-=1
		#getattr(weightstable[word],tuple.label)+=1

def learn(weightstable, maxIterations, IFile):
	# Weights for individual labels. Intially taken to be zero
	businessWeight = 0
	logisticsWeight = 0
	personalWeight = 0
    
	predictedLable = ""

	correctlyPredictedCount = 0

	fp = open(IFile,"r")

	for i in range(0,maxIterations):
		# Loop this for maxIterations number of times
		print("Performing ",i+1,"th/nd/rd/st iteration")
		for line in fp:
			tuple = getTuple(line)
			for word in tuple.words:
				# Calculate the weights of individual words in the line. Summation of all the weights in the table
				businessWeight+=weightstable[word].Business
				logisticsWeight+=weightstable[word].Logistics
				personalWeight+=weightstable[word].Personal

			weight = max(businessWeight,logisticsWeight,personalWeight)

			# Predict the label by taking the maximum of the calculated weights. 
			# In the case of equal weights, the order is Business, Logistics and Personal respectively. 
			if weight == businessWeight:
				predictedLable = "Business"
			elif weight == logisticsWeight:
				predictedLable = "Logistics"
			else:
				predictedLable = "Personal"

			if tuple.label != predictedLable:
				correctWeights(weightstable,tuple,predictedLable)

			else:
				correctlyPredictedCount+=1

			# Reset the values for the next line

			predictedLable = ""
			businessWeight = logisticsWeight = personalWeight = 0

		# Set the file pointer to the beginning of the file
		fp.seek(0)
		print("Number of correctly predicted labels = ",correctlyPredictedCount)
		# Reset the count for the next iteration
		correctlyPredictedCount = 0

	# Close the file
	fp.close()


def writeWeightsTable(weightsTable):
	oFile = open("weightsTable", "w")

	for k in weightsTable:
		oFile.write(str(k)+"	"+str(weightsTable[k].Business)+" "+str(weightsTable[k].Personal)+" "+str(weightsTable[k].Logistics))
		oFile.write("\n") 

	oFile.close()

def shouldExperiment():
	if len(sys.argv)>2:
		if sys.argv[len(sys.argv)-1] == "--experiment":
			return True
		else:
			return False

''' Author: Anushree Narasimha '''
def evaluate(label, predict, evaluate):
	#print(label, predict)
	if predict == label:
		if predict == "Business":
			evaluate.correctClassified[0] += 1
		elif predict == "Logistics":
			evaluate.correctClassified[1] += 1
		elif predict == "Personal":
			evaluate.correctClassified[2] += 1

	if predict == "Business":
		evaluate.numClassified[0] += 1
	elif predict == "Logistics":
		evaluate.numClassified[1] += 1
	elif predict == "Personal":
		evaluate.numClassified[2] += 1

	if label == "Business":
		evaluate.numTrue[0] += 1
	elif label == "Logistics":
		evaluate.numTrue[1] += 1
	elif label == "Personal":
		evaluate.numTrue[2] += 1

	'''print(evaluate.correctClassified)
	print(evaluate.numClassified)
	print(evaluate.numTrue)
	print()'''
	return evaluate

''' Author: Anushree Narasimha'''
def calculate_performance(evaluate):
	for i in range(3):
		if evaluate.numClassified[i] != 0:
			evaluate.precision[i] = round(float(evaluate.correctClassified[i]) / evaluate.numClassified[i] , 2)
	
		if evaluate.numTrue[i] != 0:
			evaluate.recall[i] = round(float(evaluate.correctClassified[i]) / evaluate.numTrue[i], 2)

		if (evaluate.precision[i] + evaluate.recall[i]) != 0:
			evaluate.fScore[i] = round(((2 * evaluate.precision[i] * evaluate.recall[i]) / float(evaluate.precision[i] + evaluate.recall[i])) , 2)

	f = open("perf.txt",'a')
	f.write("Business, Logistics, Personal\n")
	f.write("Correctly classified : "+ str(evaluate.correctClassified)+ "\n")
	f.write("Number classified : "+ str(evaluate.numClassified)+ "\n")
	f.write("Number of true : "+ str(evaluate.numTrue)+"\n")
	f.write("\n")
	f.write("Precision : "+ str(evaluate.precision)+"\n")
	f.write("Recall    : "+ str(evaluate.recall)+"\n")
	f.write("Fscore    : "+ str(evaluate.fScore)+"\n\n\n")
	f.close()

def classify(weightstable,IFName):
	iFp = open(IFName,"r")
	#oFp = open(OFName,"w")

	correctlyPredictedCount = 0
	evaluation = namedtuple('evaluation',['correctClassified', 'numClassified', 'numTrue', 'precision', 'recall', 'fScore'])
	evaluation.correctClassified  = [0,0,0]
	evaluation.numClassified = [0,0,0]
	evaluation.numTrue = [0,0,0]
	evaluation.precision = [0,0,0]
	evaluation.recall = [0,0,0]
	evaluation.fScore = [0,0,0]

	for line in iFp:
			predictedLable = ""
			businessWeight = logisticsWeight = personalWeight = 0

			tuple = getTuple(line)
			for word in tuple.words:
				# Calculate the weights of individual words in the line. Summation of all the weights in the table
				if word in weightstable:
					businessWeight+=weightstable[word].Business
					logisticsWeight+=weightstable[word].Logistics
					personalWeight+=weightstable[word].Personal

			weight = max(businessWeight,logisticsWeight,personalWeight)

			# Predict the label by taking the maximum of the calculated weights. 
			# In the case of equal weights, the order is Business, Logistics and Personal respectively. 
			if weight == businessWeight:
				predictedLable = "Business"
			elif weight == logisticsWeight:
				predictedLable = "Logistics"
			else:
				predictedLable = "Personal"

			if tuple.label == predictedLable:
				correctlyPredictedCount+=1

			evaluation = evaluate(tuple.label, predictedLable, evaluation)	

			# Reset the values for the next line

			

	print("Number of labels correctly printed from the classifier = ",correctlyPredictedCount)
	calculate_performance(evaluation)

# k is the size of each test chunk
'''Author: Anushree Narasimha'''
def kFoldValidation(k, trainpath, testpath):
	train = os.listdir(trainpath)
	iterations = math.ceil(len(train)/k)
	first = True

	for i in range(iterations):
		start = i*k
		
		#train = sorted(os.listdir(trainpath))

		for fileName in train[start:start+k]:
			#test.append(fileName)
			os.system("move "+trainpath+fileName+" "+testpath)

		perceptron()

		temp_files = os.listdir(testpath)
		for fileName in temp_files:
			os.system("move "+testpath+fileName+" "+trainpath)	

def perceptron():
	preProcess("trainingData", "consolidatedTrainingData.txt") # Need not be done every time. Can be gotten rid off once the consolidated file is built.
	preProcess("testData","consolidatedTestData.txt")
	print("Getting the maximum Iterations ...")
	maxIterations = getMaxIterations()

	flag = shouldExperiment()

	IFname = "consolidatedTrainingData.txt"

	if flag == True:
		print("Preprocessing the experiment.txt file")
		preProcess_Experimentation("consolidatedTrainingData.txt","experiment.txt",1,0)
		IFname = "experiment.txt"


	print("Building the Weights Table ...")
	weightsTable = buildTable(IFname)

	print("Learning ...")
	learn(weightsTable,maxIterations, IFname)

	print("Length of the dictionary =",len(weightsTable.keys()))

	print("Writing the weightstable to an output file ...")
	writeWeightsTable(weightsTable)

	print("Classifying the testing data")
	classify(weightsTable, "consolidatedTestData.txt")


def main():
	flag = 0
	k = 0
	for ind in range(len(sys.argv)):
		if sys.argv[ind] == "-kfold":
			flag = 1
			k = int(sys.argv[ind+1])
			break

	if flag == 0:
		perceptron()
		print("Just one perceptron")
	else:
		print("K - fold")
		kFoldValidation(k, "trainingData\\", "testData\\")
		

if __name__ == "__main__":
	main()
