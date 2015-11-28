'''
Author: Anushree Narasimha
'''

import sys
import os
import random

srcpath = os.getcwd()+"/trainingData/"
destPath = os.getcwd()+"/testData/"

allfiles = os.listdir(srcpath)

max_business = 200
max_personal = 40
max_logistics = 40
max_test_files = max_business + max_personal + max_logistics

test_business = 0
test_personal = 0
test_logistics = 0
test_files = 0

test_files_chosen = {}

while test_files<max_test_files:
	test_file_index = random.randint(0, len(allfiles)-1)
	if test_file_index in test_files_chosen:
		continue

	test_files_chosen[test_file_index] = True

	file = open(srcpath+allfiles[test_file_index], 'r')
	label = file.readline()
	file.close()

	flag = 0
	if label == "Business\n":
		if test_business >= max_business:
			continue
		test_business += 1
		flag = 1
	elif label == "Personal\n":
		if test_personal >= max_personal:
			continue
		test_personal += 1
		flag = 1
	else:
		if test_logistics >= max_logistics:
			continue
		test_logistics += 1
		flag = 1	
	if flag == 1:	
		path = srcpath + allfiles[test_file_index]
		os.system("mv " +  path + " " + destPath)
		test_files += 1