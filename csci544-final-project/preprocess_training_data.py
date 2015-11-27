import sys
import os

def isolateData():
	count = 0
	path = os.getcwd()+"/enron_with_categories"
	destPath = os.getcwd()+"/trainingData"
	folderSet = sorted(os.listdir(path))

	for folder in folderSet:
		folderPath = path+"/"+folder
		fileNames = sorted(os.listdir(folderPath))
		
		for fileName in fileNames:
			ind = fileName.find(".cats")
			if ind != -1:		
				fileCatPath = folderPath+"/"+fileName	
				#print(fileCatPath)
				file = open(fileCatPath, 'r')
				for line in file:
					temp = line.split(",")
					item = temp[0]+"."+temp[1]
					flag = 0
					tag = ""
					if item == "1.1":
						flag =1
						tag = "Business"
					elif item == "1.3":
						flag = 1
						tag = "Personal"
					elif item == "1.4":
						flag = 1
						tag = "Logistics"
					if flag == 1:	
						ifile = open(folderPath+"/"+fileName[:ind]+".txt", 'r')
						ofile = open(destPath+"/"+fileName[:ind]+".txt", 'w')
						ofile.write(tag+"\n")
						count = 0
						for line in ifile:
							count += 1
							if count> 2:
								ofile.write(line)
						ifile.close()
						ofile.close()
						print(fileName)
						break

isolateData()