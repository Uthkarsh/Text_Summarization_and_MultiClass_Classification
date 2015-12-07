import sys
from decimal import *
import math
import copy
import pickle
import os.path



enron=["enron1"]
#enron=["enron1"]
corpus={}

for en in enron:
	labell=["HAM"]	
	for label in labell:
		listdir=os.listdir(en+"/"+label)
		listdir.sort();
		for dirs in listdir:
			if(dirs!=".DS_Store"):
				d={}
				with open(en+"/"+label+"/"+dirs, "r",encoding="latin1") as f:
					for l in f:
						l=l.split("\n")[0].split()
						for word in l:
							word=word.lower()
							if word not in d:
								d[word]=1
							else:
								d[word]+=1
				corpus[dirs]=d


#print (corpus)
#print(corpus["5084.2001-11-26.farmer.ham.txt"]["txu"])

with open('corpus.pkl', 'wb') as f:
	pickle.dump(corpus, f, pickle.HIGHEST_PROTOCOL)

###############################################################################



"""
with open('corpus.pkl', 'rb') as f:
	test=pickle.load(f)
	print(test["5084.2001-11-26.farmer.ham.txt"]["txu"])
	#print (test)
"""


"""
d={}
with open("5084.2001-11-26.farmer.ham.txt", "r",encoding="latin1") as f:
	for l in f:
		l=l.split("\n")[0].split()
		for word in l:
			word=word.lower()
			if word not in d:
				d[word]=1
			else:
				d[word]+=1

for k, v in d.items():
	print (k,":",v)

"""
