import requests
import json
import time


def getTotalPnNums(mid, pn):
	'''
	获取up主mid全部作品的数量
	返回在一页显示pn个作品的情况下共有多少页
	'''
	#bilibili api接口
	path = 'https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=1&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'.format(mid=mid)
	headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
	
	req = requests.get(path, headers=headers, verify=True)

	#获取json数据
	result = json.loads(req.content)
	#获取作品总数
	totalPage = result['data']['page']['count']

	#获取页数
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
		#获取作品相关信息
		vlist = json.loads(req.content)['data']['list']['vlist']
		lenVlist = len(vlist)

		for index in range(lenVlist):
			#获取bvid
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
	#在filepath中追加内容
	with open(filePath, 'a') as f:
		for key, value in MidDict.items():
			msg += str(key) + ' '
		
		msg.rstrip()
		f.write(msg)
		f.write('\n')

def readMidCooperatorFromTXT(mid):
	'''
	读取up主mid的所有合作者
	该函数未使用
	'''
	filePath = './resourcePackage/MidCooperator/' + str(mid) + '.txt'
	with open(filePath, 'r') as f:
		for line in f.readlines():
			tempMidList = line.strip().split(' ')

def getAllCooperator(mid):
	'''
	获取与up主mid合作的所有合作者
	'''
	pnNums = getTotalPnNums(mid, 30)
	print('总页数： ', pnNums)

	#获取作品bvid
	bvidList = getBvidList(mid, pnNums)
	print('作品总数: ', len(bvidList))

	totalMidDict = {}

	for bvid in bvidList:
		#获取当前作品中的合作者
		MidDict = getMidCooperatorByBvid(bvid)
		# print(MidDict, ' ', bvid)

		#如果有合作者
		if MidDict:
			#保存合作者信息
			saveMidCooperatorToTXT(mid, MidDict)
			#保存所有合作者信息，并去除重复
			totalMidDict = {**MidDict, **totalMidDict}

		# time.sleep(5)

	print('ok')
	print(mid, ' ', totalMidDict)

	#返回所有合作者
	return totalMidDict

def recursion4Times(initMidDict):
	'''
	从当前up主开始，向下递归3次
	'''

	globalMidDict = initMidDict
	currMidSet = []


	print('initMidDict: ', globalMidDict)

	for i in range(3):
		
		print('当前迭代次数： ', i)
		print('-------------------------')

		#当前迭代的所有up主
		midList = list(globalMidDict.keys())

		# print(midList)
		# print(type(midList[0]))
		
		#对每一个up主进行迭代
		for mid in midList:
			#当前up主是第一次被访问
			if mid not in currMidSet:
				print('mid: ', mid, 'name: ', globalMidDict[mid])

				totalMidDict = getAllCooperator(mid)
				#保存所有涉及到的up主
				globalMidDict = {**totalMidDict, **globalMidDict}

				#保存已访问的up主，防止循环访问
				currMidSet.append(mid)
				# print(currMidSet)
				# print(type(currMidSet[0]))

		print('========================')

	return globalMidDict

def saveGlobalMidToTXT(globalMidDict, mid):
	#保存up主信息
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


