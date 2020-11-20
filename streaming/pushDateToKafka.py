import os
import csv
import datetime
import time

from kafka_manager import KafkaManager

def getDirList(path):
	'''
	获取指定文件夹下的全部文件名
	'''
	dirs = os.listdir(path)

	return dirs

def getYearMonthDay(filename):
	'''
	通过filename获取年 月 日
	'''
	tempDate = filename.split('.')[0]
	spiltDate = tempDate.split('-')
	year = spiltDate[0]
	month = spiltDate[1]
	day = spiltDate[2]

	return year, month, day

def readFromCsv(filename):
	'''
	从.csv文件读取数据
	'''
	path = './sharesPackage/' + filename
	returnDataList = []

	with open(path, 'r') as f:
		reader = csv.reader(f)
		DataList = list(reader)
		for line in DataList[2:]:
			#获取股票板块名称
			name = line[0].split('/')[0]

			try:
				#返回当日股票涨跌情况
				precent = float(line[2].strip('%'))
			except:
				#若当日无信息则设为0
				precent = 0

			returnDataList.append([name, precent])

	return returnDataList

###对列表进行排序###
def getSecondItem(inputList):
	'''
	返回第二列的值
	'''
	return inputList[1]

def sortDataList(dataList):
	'''
	通过每行第二个元素对列表进行降序排序
	'''
	dataList.sort(key=getSecondItem, reverse=True)

	#返回前十名
	return dataList[:10]
###end###

###添加后端kafka所需信息###
def addDescriptionToDataList(dataList, year, month, Time):
	date = year + '-' + month
	for data in dataList:
		data.append(date)
		data.append(Time)

	return dataList

def getDateTime(baseTime):
	'''
	返回basetime偏移30s后的时间
	'''

	baseTime = datetime.datetime.strptime(baseTime, '%Y-%m-%d %H:%M:%S')

	baseTime += datetime.timedelta(seconds=30)

	baseTime = baseTime.strftime('%Y-%m-%d %H:%M:%S')

	return baseTime
###end###

###将list转换为dict###
def ListToDict(inList):
	'''
	将列表转换为字典
	'''
	outDict = {}

	#主键
	keyName = ['name', 'stockUpAndDrop', 'currMonth', 'index']

	for key, value in zip(keyName, inList):
		outDict[key] = value

	return outDict
###end###

def pushCsvDataToKafka(path, kafka):
	'''
	将CSV中的内容推送到Kafka中
	'''

	baseTime = datetime.datetime.strptime('2020-11-8', '%Y-%m-%d')
	#每月数据time相同，初始为17s
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
			#每过一年，baseyear置为0
			baseMonth = 0
			baseyear = int(year)

		if int(month) > baseMonth:
			#每过一个月，time偏移30s
			Time = getDateTime(Time)
			# print(Time)
			baseMonth = int(month)
			print(year, month, baseMonth)
			#暂停5s，等待Kafka处理
			time.sleep(5)

		#读数据
		dataList = readFromCsv(currdir)
		#排序
		sortedDataList = sortDataList(dataList)
		#添加额外信息
		finalDataList = addDescriptionToDataList(sortedDataList, year, month, Time)
		# print(finalDataList[0])

		for dataList in finalDataList:
			dataDict = ListToDict(dataList)
			print(dataDict)
			#发送给Kafka
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