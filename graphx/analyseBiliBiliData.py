import os

def getFilenameList(path):
	'''
	获取path中的所有文件名
	'''
	filenameList = os.listdir(path)

	return filenameList

def getGlobalMidList(mid, name):
	'''
	获取所有up主信息
	'''

	filePath = './resourcePackage/finalResource/globalMid_' + str(mid) + '_' + name + '.txt'

	globalMidList = []

	with open(filePath, 'r') as f:
		for line in f.readlines():
			mid = line.strip('\n').split(' ')[0]
			globalMidList.append(int(mid))

	#返回up主的mid
	return globalMidList


def createMidMatrix(globalMidList):
	'''
	创建用户矩阵
	'''
	midLength = len(globalMidList)
	midMatrix = []

	for i in range(midLength):
		midMatrix.append([0 for j in range(midLength)])

	return midMatrix



def countCooperatorNums(globalMidList, midMatrix, filename):
	'''
	计算各个up主之间的合作次数
	'''
	dirPath = './resourcePackage/MidCooperator/'
	filePath = dirPath + filename

	with open(filePath, 'r') as f:
		for line in f.readlines():
			midList = line.strip().split(' ')
			length = len(midList)

			for i in range(length-1):
				indexI = globalMidList.index(int(midList[i]))

				for j in range(i+1, length):
					indexJ = globalMidList.index(int(midList[j]))

					midMatrix[indexI][indexJ] += 1


def saveMidCooperatorNums(midMatrix, globalMidList, mid, name):
	'''
	输出各个up主之间的合作次数
	'''
	path = './resourcePackage/finalResource/cooperatorNums_' + str(mid) + '_' + name + '.txt'

	length = len(globalMidList)
	msg = ''

	with open(path, 'a') as f:
		for indexI in range(length-1):
			# indexI = globalMidList.index(int(midList[i]))
			for indexJ in range(indexI+1, length):
				# indexJ = globalMidList.index(int(midList[j]))
				midMatrix[indexI][indexJ] += midMatrix[indexJ][indexI]

				if True: #midMatrix[indexI][indexJ] != 0:
					msg = str(globalMidList[indexI]) + ' ' + str(globalMidList[indexJ]) + ' ' + str(midMatrix[indexI][indexJ])
					f.write(msg + '\n')


if __name__ == '__main__':

	dirPath = './resourcePackage/MidCooperator/'

	filenameList = getFilenameList(dirPath)
	# print(filenameList)
	
	mid= 546195
	name = '老番茄'
	globalMidList = getGlobalMidList(mid, name)
	# print(len(globalMidList))


	midMatrix = createMidMatrix(globalMidList)

	# print(midMatrix)
	for filename in filenameList:
		countCooperatorNums(globalMidList, midMatrix, filename)

	saveMidCooperatorNums(midMatrix, globalMidList, mid, name)