import os
import time
import datetime
import gzip
def getSubDirs(directoryToSearch, debug):
	try:
		results = [os.path.join(directoryToSearch, o) for o in os.listdir(directoryToSearch) 
	if os.path.isdir(os.path.join(directoryToSearch,o))]
	except:
		if(debug == True):
			print("could not search:", directoryToSearch.decode("utf-8"))
		return([])
	thislist = []
	for i in results:
		thislist.append(i)

	return (thislist)
def getDirectoryAndAllSubDirectorys(directory, debug):
	monitorIterations = 0
	if(debug == True):
		startTime = datetime.datetime.now()
		lastDebugMsg = datetime.datetime.now()
		allDirectories = []
		directoriesToSearch = []
		directoriesToSearch.append(os.fsencode(directory))
		allDirectories.append(os.fsencode(directory))
		while True:
			for i in directoriesToSearch:
				monitorIterations += 1
				if (monitorIterations % 200) == 0:
					timeHasPassedCheck = datetime.datetime.now()
					difference = (timeHasPassedCheck - lastDebugMsg)
					total_seconds = difference.total_seconds()
					if total_seconds > 1:
						lastDebugMsg = datetime.datetime.now()
						print("Found:", monitorIterations, "directories so far...")
				returnedDirectories = []
				directoriesToSearch.remove(i)
				returnedDirectories = getSubDirs(i, debug)
				allDirectories += returnedDirectories
				directoriesToSearch += returnedDirectories
			if(not directoriesToSearch):
				endTime = datetime.datetime.now()
				difference = (endTime - startTime)
				total_seconds = difference.total_seconds()
				if(debug == True):
					print("Took:",total_seconds, "seconds to find:", monitorIterations, "directories")
				return(allDirectories)
	else:
		allDirectories = []
		directoriesToSearch = []
		directoriesToSearch.append(os.fsencode(directory))
		while True:
			for i in directoriesToSearch:
				returnedDirectories = []
				directoriesToSearch.remove(i)
				returnedDirectories = getSubDirs(i, debug)
				allDirectories += returnedDirectories
				directoriesToSearch += returnedDirectories
			if(not directoriesToSearch):
				return(allDirectories)



class invalidArg(Exception):
	pass
def searchAll(directoryStart, searchFor, debug, extensions, excludeOrIncludeExtensions):
	bool(debug)
	if(excludeOrIncludeExtensions == "exclude" or excludeOrIncludeExtensions == "include"):
		pass
	else:
		print("exception")
		raise(invalidArg)
	extensions = [ext.replace('.', '') for ext in extensions]
	startTime = datetime.datetime.now()
	lastDebugMsg = datetime.datetime.now()
	returnVal = ""
	directoryList = getDirectoryAndAllSubDirectorys(directoryStart, debug)
	searchFor = searchFor.casefold()
	if(debug == True):
		#Estimate how long search will take
		print("calculating size of search area for progress report...")
		fileWeight = 0
		if(debug == True):
			for directory in directoryList:
				try:
					for file in os.listdir(directory):
						extensionFinder = os.fsdecode(file).split(".")
						extensionFound = extensionFinder[-1]
						if(excludeOrIncludeExtensions == "exclude"):
							if(extensionFound in extensions):
								continue
						else:
							if(extensionFound not in extensions):
								continue
						path = os.fsdecode(directory) + "\\" + os.fsdecode(file)
						if os.path.isdir(path) == True:
							continue
						if(extensionFound == "gz"):
							fileWeight += (os.path.getsize(path))
							continue
						try:
							with open(path) as fp:
								line = fp.readline()
							fileWeight += (os.path.getsize(path))
						except:
							pass
				except:
					directoryList.remove(directory)
		print("Size of files to search:", str(fileWeight/1000000000), "Gigabytes")
	fileWeightProgress = 0
	for directory in directoryList:
		try:
			for file in os.listdir(directory):
				extensionFinder = os.fsdecode(file).split(".")
				extensionFound = extensionFinder[-1]
				if(excludeOrIncludeExtensions == "exclude"):
					if(extensionFound in extensions):
						continue
				else:
					if(extensionFound not in extensions):
						continue
				path = os.fsdecode(directory) + "\\" + os.fsdecode(file)
				if(debug == True):
					timeHasPassedCheck = datetime.datetime.now()
					difference = (timeHasPassedCheck - lastDebugMsg)
					total_seconds = difference.total_seconds()
					if total_seconds > -1:
						lastDebugMsg = datetime.datetime.now()
						print(path, "Progress:", str(round(((fileWeightProgress/fileWeight)*100))) +"%")
					fileWeightProgress += os.path.getsize(path)

				if os.path.isdir(path) == True:
					continue
				if(extensionFound == "gz"):
					with gzip.open(path) as fp:
						found = False
						foundVals = []
						try:
							line = fp.readline()
						except:
							print("failed to read:", path)
							continue
						cnt = 0
						while line:
							try:
								line = str(line).casefold()
								if(searchFor in line):
									found = True
									result = line.replace(searchFor, (""+searchFor.upper()+"")).strip("\n")
									result = result[:-5]
									foundVals.append("[{}]: {}".format(cnt, result))
								line = fp.readline()
								cnt += 1
							except:
								if(debug == True):
									print("failed to read line:", cnt, "in:", path)
								break
						if(found):
							returnVal += path+":\n"
							for val in foundVals:
								returnVal+="     "+val + "\n"
				else:
					with open(path) as fp:
						found = False
						foundVals = []
						try:
							line = fp.readline()
						except:
							print("failed to read:", path)
							break
						cnt = 0
						while line:
							try:

								line = line.casefold()
								if(searchFor in line):
									found = True
									result = line.replace(searchFor, (""+searchFor.upper()+"")).strip("\n")
									foundVals.append("[{}]: {}".format(cnt, result))
									#foundVals.append(str(lineStr, line.replace(searchFor, (""+searchFor.upper()+"")).strip("\n") ))
								line = fp.readline()
								cnt += 1
							except:
								print("failed to read line:", cnt, "in:",path)
								break
						if(found):
							returnVal += path+":\n"
							for val in foundVals:
								returnVal+="     "+val + "\n"
		except:
			directoryList.remove(directory)
			print("Something bad happend in:", directory)
	return(returnVal)




extensions = []
#extensions = [".log", ".gz", ".txt"]
locations = searchAll("C:\\Users\\modding2\\Desktop", "hi", False, extensions, "exclude")
print(locations)