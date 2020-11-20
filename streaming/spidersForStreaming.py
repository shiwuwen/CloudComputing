#coding=utf-8

import requests
import pandas as pd 

def getDateFromWeb(dateList=None):
	'''
	获取aigaogao.com中的股票信息
	'''

	for date in dateList:
		#目标网址
		target = 'http://aigaogao.com/tools/sectors.html?dt=' + date
		print(target)

		#保存路径
		csvPath = './sharesPackage/' + date + '.csv'

		#获取表格样式的数据
		tables = pd.read_html(target, attrs={'id':'sectscmp'})
		# print(len(tables))

		#获取有用的数据
		usefulTable = tables[0]

		#重命名列属性
		usefulTable.columns = ['分类', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
		#去除2,3列
		usefulTable = usefulTable.drop([2,3], axis=1)
		
		usefulTable.columns = ['分类', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]	
		# print(usefulTable.columns)
		# print(usefulTable
		usefulTable.to_csv(csvPath, encoding="utf-8", index=0)


def getDateList(dateBegin='2007-01-01'):
	'''
	获取时间列表
	2007-01-01 -- now
	'''
	import datetime
	#获取当前时间
	dateEnd = datetime.datetime.now().strftime('%Y-%m-%d')
	dateEnd = datetime.datetime.strptime(dateEnd, '%Y-%m-%d')
	# print('dateEnd', dateEnd)

	dateList = []
	dateBegin = datetime.datetime.strptime(dateBegin, '%Y-%m-%d')
	dateList.append(dateBegin.strftime('%Y-%m-%d'))

	while dateBegin < dateEnd:
		dateBegin += datetime.timedelta(days=+1)
		# print('dateBegin: ', dateBegin)
		dateList.append(dateBegin.strftime('%Y-%m-%d'))

	return dateList


if __name__ == '__main__':

	dateList = getDateList('2007-01-01')
	print(len(dateList))

	getDateFromWeb(dateList)