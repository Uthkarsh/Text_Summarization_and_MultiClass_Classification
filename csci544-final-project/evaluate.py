import sys

testFile = open(sys.argv[1], 'r')
labels = open(sys.argv[2], 'r')

correctClassified  = [0,0,0]
numClassified = [0,0,0]
numTrue = [0,0,0]
precision = [0,0,0]
recall = [0,0,0]
fScore = [0,0,0]

lineNum = 0
for line in testFile:
	lineNum += 1

testFile.seek(0)

for i in range(lineNum):
	predict = testFile.readline()
	label = labels.readline()

	if predict == label:
		if predict == "Business\n":
			correctClassified[0] += 1
		elif predict == "Logistics\n":
			correctClassified[1] += 1
		elif predict == "Personal":
			correctClassified[2] += 1

	if predict == "Business\n":
		numClassified[0] += 1
	elif predict == "Logistics":
		numClassified[1] += 1
	elif predict == "Personal":
		numClassified[2] += 1

	if label == "Business\n":
		numTrue[0] += 1
	elif label == "Logistics":
		numTrue[1] += 1
	elif label == "Personal":
		numTrue[2] += 1


	for i in range(3):
		if numClassified[i] != 0:
			precision[i] = round(float(correctClassified[i]) / numClassified[i] , 2)
	
		if numTrue[i] != 0:
			recall[i] = round(float(correctClassified[i]) / numTrue[i], 2)


		if (precision[i] + recall[i]) != 0:
			fScore[i] = round(((2 * precision[i] * recall[i]) / float(precision[i] + recall[i])) , 2)

print("Business, Logistics, Personal")
print("Precision : ", precision)
print("Recall    : ", recall)
print("Fscore    : ", fScore)