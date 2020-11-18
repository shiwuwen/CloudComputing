import requests
import json
import time


def getTotalPnNums(mid, pn):
	'''
	获取up主mid全部作品的数量
	返回在一页显示pn个作品的情况下共有多少页
	'''
	path = 'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=1&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'.format(mid=mid)
	headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
	
	req = requests.get(path, headers=headers, verify=True)

	result = json.loads(req.content)
	totalPage = result['data']['page']['count']

	pnNums = totalPage // pn

	return pnNums + 1


def getBvidList(mid, pnNums):
	'''
	获取up主mid所有作品的bvid
	'''
	bvidList = []
	for pageNum in range(1, pnNums+1):
		# print(pageNum)
		path = 'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn={pageNum}&keyword=&order=pubdate&jsonp=jsonp'.format(pageNum=pageNum, mid=mid)
		headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
		
		req = requests.get(path, headers=headers, verify=True)
		vlist = json.loads(req.content)['data']['list']['vlist']
		lenVlist = len(vlist)

		for index in range(lenVlist):
			bvidList.append(vlist[index]['bvid'])

	return bvidList

def getMidCooperatorByBvid(bvid):
	'''
	获取一个bvid中的所有合作者
	返回 mid:name 的字典
	'''
	MidDict = {}
	path = 'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'.format(bvid=bvid)
	headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
	
	req = requests.get(path, headers=headers, verify=True)
	try:
		staffList = json.loads(req.content)['data']['staff']

		for index in range(len(staffList)):
			MidDict[staffList[index]['mid']] = staffList[index]['name']

		return MidDict
	except:
		# print('no cooperator', bvid)
		return None

def saveMidCooperatorToTXT(mid, MidDict):
	'''
	将与up主mid进行合作的所有其他up主写入TXT文件
	格式为 mid name
	'''
	filePath = './resourcePackage/MidCooperator/' + str(mid) + '.txt'
	msg = ''
	with open(filePath, 'a') as f:
		for key, value in MidDict.items():
			msg += str(key) + ' '
		
		msg.rstrip()
		f.write(msg)
		f.write('\n')

def readMidCooperatorFromTXT(mid):
	'''
	读取up主mid的所有合作者
	'''
	filePath = './resourcePackage/MidCooperator/' + str(mid) + '.txt'
	with open(filePath, 'r') as f:
		for line in f.readlines():
			tempMidList = line.strip().split(' ')

def getAllCooperator(mid):
	'''
	获取与up主mid的所有合作者
	'''
	pnNums = getTotalPnNums(mid, 30)
	print('总页数： ', pnNums)

	bvidList = getBvidList(mid, pnNums)
	print('作品总数: ', len(bvidList))

	totalMidDict = {}

	for bvid in bvidList:
		MidDict = getMidCooperatorByBvid(bvid)
		# print(MidDict, ' ', bvid)

		if MidDict:
			saveMidCooperatorToTXT(mid, MidDict)
			totalMidDict = {**MidDict, **totalMidDict}

		# time.sleep(5)

	print('ok')
	print(mid, ' ', totalMidDict)

	return totalMidDict

def recursion4Times(initMidDict):

	globalMidDict = initMidDict
	currMidSet = []


	print('initMidDict: ', globalMidDict)

	for i in range(3):
		
		print('当前迭代次数： ', i)
		print('-------------------------')


		midList = list(globalMidDict.keys())

		# print(midList)
		# print(type(midList[0]))

		for mid in midList:
			if mid not in currMidSet:
				print('mid: ', mid, 'name: ', globalMidDict[mid])

				totalMidDict = getAllCooperator(mid)
				globalMidDict = {**totalMidDict, **globalMidDict}

				currMidSet.append(mid)
				# print(currMidSet)
				# print(type(currMidSet[0]))

		print('========================')

	return globalMidDict

def saveGlobalMidToTXT(globalMidDict, mid):
	filePath = './resourcePackage/globalMid_' + str(mid) + '_' + name +'.txt'
	msg = ''
	with open(filePath, 'a') as f:
		for key, value in globalMidDict.items():
			msg = str(key) + ' ' + value + '\n'
			f.write(msg)


if __name__ == '__main__':

	mid= 546195
	name = '老番茄'

	initMidDict = {}
	initMidDict[mid] = name

	globalMidDict = recursion4Times(initMidDict)
	print('globalMidDict: ', globalMidDict)
	saveGlobalMidToTXT(globalMidDict, mid, name)











	# pnNums = getTotalPnNums(mid, 30)
	# print(pnNums)

	# bvidList = getBvidList(mid, pnNums)
	# print(len(bvidList))

	
	# MidDict = getMidCooperatorByBvid(bvidList[0])
	# print(MidDict)

	# if MidDict:
	# 	saveMidCooperatorToTXT(mid, MidDict)

	# pageNum = 1
	# mid=546195
	# path = 'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn={pageNum}&keyword=&order=pubdate&jsonp=jsonp'.format(pageNum=pageNum, mid=mid)
	# headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
	# # path = 'https://api.bilibili.com/x/space/navnum?mid=546195&jsonp=jsonp&callback=__jp3'
	# req = requests.get(path,  headers=headers, verify=False)

	# result = json.loads(req.content)
	# print(result)



	# saveMidCooperatorToTXT(mid, MidDict)


