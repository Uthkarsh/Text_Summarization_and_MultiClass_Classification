import sys
from decimal import *
import math
import copy
import pickle
import os.path

corpus={}
with open('corpus.pkl', 'rb') as f:
	corpus=pickle.load(f)

d={}
sentences=[]
summaryResult=""

fileName=sys.argv[1]
stiked={}

def idf(term):
	count=0
	for d in corpus:
		#print ("Dict : ",d)
		if term.lower() in corpus[d]:
			count+=1

	#print("Term : ",term.lower(),"\tCount : ",count)
	if count!=0:
		return math.log(float(len(corpus))/(count))
	else:
		return 0

def tf(term,stiked,fileN):
	term=term.lower()
	if term not in stiked:
		#print (term, fileN)
		if term not in corpus[fileN].keys():
			return 0
		return corpus[fileN][term]
	else:
		return 0

def simFun(sentences,fileN,stiked):
	maxSim=0;
	sen="";

	for everySentence in sentences:
		#print("in SumFunc:", everySentence)
		suM=0
		everySentenceList=everySentence.split()
		for word in everySentenceList:
			tf_=tf(word,stiked,fileN)
			idf_=idf(word)
			suM+=tf_*idf_
			#print("tf: ",tf_," idf: ",idf_)
		if suM>maxSim:
			#print("Reached here!")
			maxSim=suM
			sen=everySentence
	return sen



with open(fileName, "r",encoding="latin1") as f:
	sentences=f.read().split(".")
	fulldoc=f.read()
	q=fulldoc
	numUniq=len(corpus[fileName])

	while(1):
		#print ("striked: ",len(stiked)+1," numU: ",numUniq)
		if len(stiked)+1==numUniq or len(sentences)==0:
			break
		sen=simFun(sentences,fileName,stiked)
		#print ("sen: ",sen,"\n\n")
		#print ("sentences: ",sentences,"\n\n")
		sentences.remove(sen)
		summaryResult+=sen.strip()+"\n "
		sen=sen.split()
		for word in sen:
			word=word.lower()
			if word not in stiked:
				stiked[word]=1
		#print("striker: ",stiked)
		#print("-------------------------------------------------------\n\n")


#print("\n\n\n\n==============OUR SUMMARY :======================\n")
print(summaryResult)


