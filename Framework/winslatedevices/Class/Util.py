import time
from datetime import timedelta, datetime
from time import sleep
import json

#Define a function to get data from userDBFile.txt				
def getCallParams(file):

	paramList = {}
	clusterData = {}
	clusterName = None
	txt = open(file)
	data = txt.read()
	#print(data)
	lineList = data.split("\n")
	startData = 0
	for eachLine in lineList :
		#print(eachLine)
		if eachLine != "":
			line = eachLine.split()
			if 'Cluster' in line[0] and startData == 0 :
				startData = 1
				clusterName = line[1]
			elif 'Cluster' in line[0] and startData == 1 :
				paramList[clusterName] = clusterData.copy()
				#print(paramList)
				#print('\n')
				clusterData.clear()
				startData = 1
				clusterName = line[1]
			elif (startData == 1 and  "Cluster" not in line[0] and line[0] != ""):
				line = eachLine.split(" = ")
				clusterData[line[0]] = line[1]
				
	paramList[clusterName] = clusterData.copy()
	#print(paramList)
		
	txt.close()
	return paramList
	
def getUserData() :
	userData = []
	txt = open("UserDBFile.txt")
	data = txt.read()
	lineList = data.split("\n")
	counter = 0
	columnList = []
	tempData = {}
	
	for eachLine in lineList:
		if not eachLine.strip():
			continue
		elif eachLine.startswith("#"):
			continue
		else:
			line = eachLine.split()
			if counter == 0:
				columnList = lineList[0].split()
				counter += 1
			else :
				for i in range(len(columnList)) :
					tempData[columnList[i]] = line[i]
				#print(tempData)
				userData.append(tempData.copy())
				#print(userData)
	
	txt.close()
	return userData		
