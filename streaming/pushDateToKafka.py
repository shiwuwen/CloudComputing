import os
import csv
import datetime
import time

from kafka_manager import KafkaManager

def getDirList(path):
	dirs = os.listdir(path)

	return dirs

def getYearMonthDay(filename):
	tempDate = filename.split('.')[0]
	spiltDate = tempDate.split('-')
	year = spiltDate[0]
	month = spiltDate[1]
	day = spiltDate[2]

	return year, month, day

def readFromCsv(filename):
	path = './sharesPackage/' + filename
	returnDataList = []

	with open(path, 'r') as f:
		reader = csv.reader(f)
		DataList = list(reader)
		for line in DataList[2:]:
			name = line[0].split('/')[0]

			try:
				precent = float(line[2].strip('%'))
			except:
				precent = 0

			returnDataList.append([name, precent])

	return returnDataList

###对列表进行排序###
def getSecondItem(inputList):
	return inputList[1]

def sortDataList(dataList):
	dataList.sort(key=getSecondItem, reverse=True)

	return dataList[:10]
###end###

###添加kafka所需信息###
def addDescriptionToDataList(dataList, year, month, Time):
	date = year + '-' + month
	for data in dataList:
		data.append(date)
		data.append(Time)

	return dataList

def getDateTime(baseTime):

	baseTime = datetime.datetime.strptime(baseTime, '%Y-%m-%d %H:%M:%S')

	baseTime += datetime.timedelta(seconds=30)

	baseTime = baseTime.strftime('%Y-%m-%d %H:%M:%S')

	return baseTime
###end###

###将list转换为dict###
def ListToDict(inList):
	outDict = {}

	keyName = ['name', 'stockUpAndDrop', 'currMonth', 'index']

	for key, value in zip(keyName, inList):
		outDict[key] = value

	return outDict
###end###

def pushCsvDataToKafka(path, kafka):

	baseTime = datetime.datetime.strptime('2020-11-8', '%Y-%m-%d')
	Time = (baseTime + datetime.timedelta(seconds=17)).strftime('%Y-%m-%d %H:%M:%S')

	print(Time)

	baseMonth = 0
	baseyear = 2007

	dirs = getDirList(path)

	for currdir in dirs:
		# print(currdir)
		year, month, day = getYearMonthDay(currdir)

		# print(int(month))

		if int(year) > baseyear:
			baseMonth = 0
			baseyear = int(year)

		if int(month) > baseMonth:
			Time = getDateTime(Time)
			# print(Time)
			baseMonth = int(month)
			print(year, month, baseMonth)
			time.sleep(5)

		dataList = readFromCsv(currdir)
		sortedDataList = sortDataList(dataList)

		finalDataList = addDescriptionToDataList(sortedDataList, year, month, Time)
		# print(finalDataList[0])

		for dataList in finalDataList:
			dataDict = ListToDict(dataList)
			print(dataDict)
			kafka.push_record(dataDict)

	print('end')





if __name__ == '__main__':
	path = '/home/hadoop/workplace/CloudComputing/sharesPackage'
	bootstrap_servers = 'hadoop-node-1:9092,hadoop-node-1:9092,hadoop-node-1:9092'
	topic = 'streamingInput20201116'
	kafka = KafkaManager(bootstrap_servers, topic)
	
	pushCsvDataToKafka(path, kafka)
	# dirs = getDirList(path)

	# # print(dirs[0:20])

	# year, month, day = getYearMonthDay(dirs[0])
	# # print(year, month, day)

	# dataList = readFromCsv(dirs[0])
	# # print(dataList)

	# sortedDataList = sortDataList(dataList)
	# # print(sortedDataList)
	
	
	# finalDataList = addDescriptionToDataList(sortedDataList, year, month, Time)
	# print(finalDataList)

	# getDateTime()