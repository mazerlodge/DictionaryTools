#!/usr/bin/python

# Version: 20170825-2015

import sys
from ArgTools import ArgParser

class DictionaryEngine:

	# Hard coded constants
	DICTIONARY_FILE__MAC = "/Users/mazerlodge/Documents/XProjects/ObjectiveC/Skylar/Dictionaries/DictionaryPatterns.csv"
	DICTIONARY_FILE__WIN = "C:\pmsoren\_PT\pyproj\DictionaryTools\Data\DictionaryPatterns.csv"

	# Setup variables
	bInitOK = False
	bInDebug = False
	osType = "NOT_SET"
	maintType = "NOT_SET"
	searchType = "NOT_SET"
	dictionaryPath = "NOT_SET"
	outDictionaryPath = "NOT_SET"
	targetPhrase = "NOT_SET" 
	action = "NOT_SET"
	lines = []
	windowSize = -1

	def __init__(self,args):
		if (self.parseArgs(args)):
			self.bInitOK = True
		else:
			print("Init failed in argument parser.")
			
	def showUsage(self):
		print("Usage: python dict.py -os [mac | win] -action [search | genmask | jumblept2 | maint ] {-debug}\n"
				+ "About searches: find a word, pattern (like ABBC), substitution "
				+ "encoded word (like GBRRCB),\n or jumbled word (like ISFH, returns fish).\n"
				+ "\tParams for -action search: -searchtype [word | pattern | encword | jumble] -target targetPhrase \n"
				+ "\tParams for -action jumblept2: -target letterList -windowsize n  \n"
				+ "\tParams for -action genmask: -target targetPhrase \n"
				+ "\tParams for -action maint: -mainttype [ gensortcolumn | addword ] -target word_to_add \n "
				+ "\tNote: search for word or encword returns first match, pattern returns all matches.\n")
		
	def parseArgs(self,args):
		# Parse the arguments looking for required parameters.
		# Return false if any tests fail.

		#global osType, action, searchType, targetPhrase

		subtestResults = []
		rval = True

		# Instantiate the ArgParser
		ap = ArgParser(args)
		
		# check for optional debug flag
		self.bInDebug = ap.isInArgs("-debug", False)

		# check the OS type
		rv = False
		if (ap.isArgWithValue("-os", "mac") or ap.isArgWithValue("-os", "win")):
			self.osType = ap.getArgValue("-os")
			rv = True
		subtestResults.append(rv)

		# check for action
		self.action = "NOT_SET"
		rv = False
		if (ap.isInArgs("-action", True)):
			# action value must appear after target
			self.action = ap.getArgValue("-action")
			rv = True
		subtestResults.append(rv)

		# check for searchtype, using a different arg parse approach than the OS check.
		if (self.action == "search"):
			rv = False
			if (ap.isInArgs("-searchtype", True)):
				# value must be either word or pattern
				st = ap.getArgValue("-searchtype")
				validSearchTypes = ["word", "pattern", "encword", "jumble"]
				for vst in validSearchTypes:
					if (st == vst):
						self.searchType = st
						rv = True
			subtestResults.append(rv)
			
			# search also requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResults.append(rv)
			
		# check for JumblePt2 
		if (self.action == "jumblept2"):
			rv = False
			if (ap.isInArgs("-windowsize", True)):
				self.windowSize = int(ap.getArgValue("-windowsize"))
				rv = True
			subtestResults.append(rv)

			# JumblePt2 also requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResults.append(rv)
			
		# check for genmask 
		if (self.action == "genmask"):
			# GenMask requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResults.append(rv)			

		# check for maintenance 
		if (self.action == "maint"):
			rv = False
			if (ap.isInArgs("-mainttype", True)):
				self.maintType = ap.getArgValue("-mainttype")
				if (self.maintType == "addword"):
					if (ap.isInArgs("-target", True)):
						self.targetPhrase = ap.getArgValue("-target")
						rv = True

				# no additional checks for adding sort column
				if (self.maintType == "gensortcolumn"):
					rv = True
			subtestResults.append(rv)

		# Determine if all subtests passed
		for idx in range(len(subtestResults)):
			if (self.bInDebug):
				print "Arg subtest " + str(subtestResults[idx])
			rval = rval and subtestResults[idx]
				
		return(rval)
	
	def getDictionaryLines(self):

		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.dictionaryPath = self.DICTIONARY_FILE__MAC 
		else:
			self.dictionaryPath = self.DICTIONARY_FILE__WIN

		# Read the dictionary
		file = open(self.dictionaryPath, "r")
		lines = file.readlines()
		file.close()
	
		return(lines)
	
	def writeDictionaryLinesWithSortColumn(self):

		outLineCount = 0
	
		lines = self.getDictionaryLines()

		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.outDictionaryPath = self.DICTIONARY_FILE__MAC 
		else:
			self.outDictionaryPath = self.DICTIONARY_FILE__WIN

		# open the new file for writing.
		file = open(self.outDictionaryPath + "NEW", "w")
	
		for aline in lines:
			parts = aline.split(',')
			line2write = aline
			# if the line is commented out, don't add sort column
			if aline[0] != '#':	
				line2write = aline.strip() + "," + doSortGen(parts[0]) + "\n"
			file.write(line2write)
			outLineCount += 1

		file.close()
	
		print("Lines written to new dictionary file: " + str(outLineCount))
	
		return(outLineCount)
		
	def addWordToDictionary(self, newWord):
		# add the specified word to the dictionary.
		# dictionary entries have the following format:
		# #word,len,pattern,sortedword
		# aardvark,8,AABCDABE,aaadkrrv
		
		# search the dictionary to see if the word already exists.
		searchResult = self.doSearch("word", newWord, True)
		
		if (len(searchResult) > 0):
			print "addWordToDictionary: The word is already in dictionary."
			return
			
		# generate line to add to the dictionary
		line2Add = ",".join([ newWord, 
								str(len(newWord)),
								self.doMaskGen(newWord),
								self.doSortGen(newWord)])
		line2Add = line2Add + "\n"
				
		print "Line to add: " + line2Add			

	
		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.DictionaryPath = self.DICTIONARY_FILE__MAC 
		else:
			self.DictionaryPath = self.DICTIONARY_FILE__WIN

		# open the new file for writing.
		file = open(self.DictionaryPath, "a")
		file.write(line2Add)
		file.close()
	
		print("Lines written to dictionary: " + self.DictionaryPath)
		
		
	def generateOdometer(self, letterList, windowSize):
		# factory like method producing an odometer (array of strings) 
		
		odometer = []

		# Note: No shortening of the wheels to remove dupes, 
		#        those dupes are skipped by advanceOdometer().
		for x in range(0,windowSize): 
			odometer.append(letterList)
			
		return odometer
	
	def isOdometerAtMax(self, odometer,oIdx):
	
		rval = True 
		
		for i in range(0,len(odometer)):
			if (oIdx[i] < len(odometer[i])-1):
				rval = False
				
		return rval
		
	def advanceOdometer(self, odometer, oIdx):
		# Advance the odometer and skip any combos where a letter would be repeated.
		# Said another way, each oIdx value must be distinct.
		# Example: given 1-2-0, 1-2-1 is invalid, so is 1-2-2, skip to 1-2-3)
			
		indexToAdvance = -1
		wheelLength = len(odometer[0])
		windowSize = len(odometer)
		
		cycleCount = 0
		cycleLimit = wheelLength**windowSize
		bDone = False
		while (not bDone): 
			cycleCount += 1
			
			# walk odometer wheels right to left ( <-- )
			for i in range(windowSize-1, -1, -1):
				if (oIdx[i] < wheelLength-1):
					# this index can be advanced 
					indexToAdvance = i
					break
					
			# advance specified index and neighbors to the right
			if (indexToAdvance > -1):
				oIdx[indexToAdvance] += 1
				# set all indexes to the right of this one.
				# Use values this high plus 1 per position to the right (e.g. +1, +2, +3,... for neghbors to the right).
				# This ONLY WORKS because this result is used in a context where order of elements doesn't matter.
				# 	(e.g. 012 and 021 are considered dupes so rolling over from 019 to 023 skipping 020 and 021 is desirable)
				#  Note: the step after this will correct any that exceeded the max.
				for x in range(indexToAdvance+1, windowSize):
					oIdx[x] = oIdx[indexToAdvance]+(x-indexToAdvance)

				# The max value is based on combo of odometer length and position.
				# E.G. With 5 values in odometer[n], and a window size of 3 (specified by oIdx length), 
				#        max values are 2-3-4 (indexes are zero based).
				for x in range(0, windowSize):
					if (oIdx[x] > wheelLength-(windowSize-x)):
						oIdx[x] = wheelLength-1
			
			# mark as done if there are no dupes except for all maxes
			bDone = True
			maxCount = 0
			for x in range(0, len(oIdx)):
				if (oIdx.count(oIdx[x]) > 1): # and (oIdx[x] < wheelLength-1)):
					bDone = False
					
				if (oIdx[x] == wheelLength -1):
					maxCount += 1
					
				if (maxCount == windowSize):
					bDone = True
					
			# check governor
			if (cycleCount > cycleLimit):
				print "advanceOdometer hit governor limit, exiting."
				bDone = True
				
			
	def readOdometer(self, odometer, oIdx):
	
		rval = "" 
		
		for x in range(0,len(odometer)): 
			rval += odometer[x][oIdx[x]]
		
		return rval
				
	
	def doJumblePt2(self, letterList, windowSize): 
		# process Jumble Part 2 using Odometer method.
		
		phraseList = []
		
		# generate odometer and odometer index, the odometer is an array of strings.
		odometer = self.generateOdometer(letterList, windowSize)
		oIdx = []
		for i in range(0,len(odometer)):
			oIdx.append(i)
		
		# Generate Phrase List 
		print "Building distinct potential jumble list..."
		odoCycleCount = 0
		
		# set cycle limit to length of letter list factorial for windowsize range.
		# e.g. letter list of 7, widow size 2 --> 7*6 (stop, aka given 7 letters there are 42 2 letter combos).

		cycleLimit = len(letterList)
		for x in range(len(letterList)-1,len(letterList)-windowSize,-1):
			cycleLimit = cycleLimit * x
			
		msgInterval = cycleLimit * .1
		ci = msgInterval
		print "Cycle Limit set to " + str(cycleLimit)
		bDone = False
		while(not bDone): 
			odoCycleCount += 1
			
			phrase = self.readOdometer(odometer, oIdx)
			sortedPhrase = self.doSortGen(phrase)
			
			if (self.bInDebug):
				print "doJumblePt2: phrase = " + phrase, str(oIdx[0]), str(oIdx[1]), str(oIdx[2])
			
			if(phraseList.count(sortedPhrase) == 0):
				phraseList.append(sortedPhrase) 
			
			# If at odometer is at max position mark as done, otherwise advance.
			if (self.isOdometerAtMax(odometer,oIdx)):
				# remove last item, it is all maxes.
				del phraseList[len(phraseList)-1]
				bDone = True
			else:
				self.advanceOdometer(odometer, oIdx)
				
			# Check governor for runaway process
			if (odoCycleCount > cycleLimit):
				print "doJumblePt2: Cycle limit governor hit."
				bDone = True
				
			if (odoCycleCount > ci):
				print "Working, cycle limit percent consumed = " + str(odoCycleCount*1.0/cycleLimit)
				ci += msgInterval

		print "Cycles used = %s " % odoCycleCount
	
		# Process phrases through jumble evaluation 
		print("Processing, letter combos count = " + str(len(phraseList)))
		
		# Walk the phrase list, finding jumble matches, adding them to 
		#   the distinct match list.
		matchList = []
		loopCount = 0
		phraseCount = len(phraseList)
		msgInterval = phraseCount * .1
		ci = msgInterval
		for phrase in phraseList:
			loopCount += 1
			currentMatches = self.doSearch("jumble", phrase, True)
			if (len(currentMatches) > 0):
				for m in currentMatches:
					if (matchList.count(m) == 0):
						matchList.append(m)
						
			if (loopCount > ci):
				print "Working, combos processed = " + str(loopCount*1.0/phraseCount)
				ci += msgInterval
				
		# end for phrase...
		
		if (len(matchList) == 0):
			print "No matches found"
		else:
			for aMatch in matchList:
				print aMatch
			print "Match count = " + str(len(matchList))


	def showMsg(self, msg, bQuiet):
		if (not bQuiet):
			print(msg)

	
	def doSearch(self, searchType, targetPhrase, bQuiet):

		rval = []

		# Load the dictionary if not already set
		if (len(self.lines) < 1):
			self.lines = self.getDictionaryLines()

		# determine which index to search; 0 for words, 2 for patterns
		idx = 0
		if (searchType == "pattern"):
			idx = 2
			self.showMsg("Searching for patterns.", False)
		
		if (searchType == "encword"):
			# find a pattern from the encrypted word and do a pattern search
			idx = 2
			targetPhrase = self.doMaskGen(targetPhrase)
			self.showMsg("Searching for generated pattern.", bQuiet)

		if (searchType == "jumble"):
			# find a sorted pattern from the target word and do a search
			idx = 3
			self.showMsg("Searching for jumbled word %s." % targetPhrase, bQuiet)
			targetPhrase = self.doSortGen(targetPhrase)

		# If the word2find was a phrase, break up the phrase and search for each word
		w2fParts = targetPhrase.split(' ')
		if (len(w2fParts) > 1):
			self.showMsg("Searching for each word in the phrase '%s'." % targetPhrase, bQuiet)
	
		for word2find in w2fParts:
			# work on each word in the phrase
			bFound = False

			# Search for a word
			for line in self.lines:
				parts = line.split(',')
				# word is in part 0
				currentWord = parts[idx].strip()
				if(word2find.lower() == currentWord.lower()):
					self.showMsg(line.strip(), bQuiet)
					rval.append(line.strip())
					bFound = True

					# perf improvement: if not searching for a pattern stop after 1.
					if (searchType != "pattern"):
						break

			# Print not found results
			if (not bFound):
				self.showMsg("%r not found" % word2find, bQuiet)
				
		return rval
			
	def doMaskGen(self, rawPhrase):
		# generate a mask for the value in targetPhrase
		rval = ""
		
		phraseLen = len(rawPhrase)
		distinctPhraseLetters = []
		patternLetters = []
	
		# build distinct phrase letters array
		for aLetter in rawPhrase:
			if(not self.isInArray(aLetter, distinctPhraseLetters)):
				distinctPhraseLetters.append(aLetter)
	
		# populate pattern letters array
		currASCIIVal = 65
		for x in range(0,len(distinctPhraseLetters)):
			patternLetters.append(chr(currASCIIVal))
			currASCIIVal += 1
		
		# generate mask
		for tpl in rawPhrase:
			maskLetter = self.getCorrespondingEntry(tpl,distinctPhraseLetters,patternLetters)
			rval += maskLetter
		
		# output result
		print("doMaskGen: The mask is " + rval)
	
		return(rval)
	
	def doSortGen(self, phrase):
		# Generate a string with chars from phrase in sorted order.
	
		newphrase=""
	
		for ac in sorted(phrase):
			newphrase += ac
	
		return(newphrase)
					
	def getCorrespondingEntry(self, letter, phraseArray, patternArray):

		rval = "?"
	
		for x in range(0,len(phraseArray)):
			if (letter == phraseArray[x]):
				rval = patternArray[x]
				break;
	
		return(rval)
		
	def isInArray(self, letter, phraseArray):
	
		rval = False
	
		for aLetter in phraseArray:
			if (letter == aLetter):
				rval = True
				break
			
		return(rval)
		
	def doMaint(self):

		if (self.bInDebug):
			print "doMaint: Processing maintenance type [%s]" % self.maintType

		# determine which maintenance to do 		
		if (self.maintType == "gensortcolumn"):
			self.writeDictionaryLinesWithSortColumn()

		if (self.maintType == "addword"):
			self.addWordToDictionary(self.targetPhrase)		
		
	def doAction(self):
	
		if (self.bInDebug):
			print "doAction: Processing action [%s]" % self.action
	
		# determine which action to execute
		if (self.action == "search"):
			self.doSearch(self.searchType, self.targetPhrase, False)
	
		if (self.action == "genmask"):
			self.doMaskGen(self.targetPhrase)
	
		if (self.action == "jumblept2"):
			self.doJumblePt2(self.targetPhrase, self.windowSize)

		if (self.action == "maint"):
			self.doMaint()
	
	
	


