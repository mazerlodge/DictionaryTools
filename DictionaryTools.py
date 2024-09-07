# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-locals
# pylint: disable=superfluous-parens
# pylint: disable=invalid-name
# pylint: disable=bad-indentation
# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-branches
# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-enumerate
# pylint: disable=trailing-whitespace
# pylint: disable=too-many-nested-blocks


# Version: 20170825-2015

from ArgTools import ArgParser


class DictionaryEngine:

	# Hard coded constants
	DICTIONARY_FILE__MAC = "/Users/mazerlodge/Documents/XProjects/Python/"\
						   + "DictionaryTools/Data/DictionaryPatterns.csv"
	DICTIONARY_FILE__WIN = "C:\\pmsoren\\_PT\\pyproj\\DictionaryTools\\Data"\
            + "\\DictionaryPatterns.csv"

	# Setup variables
	bInitOK = False
	bInDebug = False
	bHasRequireList = False
	bHasOmitList = False
	bHasMask = False
	osType = "NOT_SET"
	maintType = "NOT_SET"
	searchType = "NOT_SET"
	dictionaryPath = "NOT_SET"
	outDictionaryPath = "NOT_SET"
	targetPhrase = "NOT_SET"
	includeList = "NOT_SET"
	requireList = "NOT_SET"
	omitList = "NOT_SET"
	mask = "NOT_SET"
	action = "NOT_SET"
	lines = []
	windowSize = -1

	def __init__(self, args):
		if (self.parseArgs(args)):
			self.bInitOK = True
		else:
			print("Init failed in argument parser.")

	@staticmethod
	def showUsage():
		print("Usage: python dict.py -os [mac | win] -action [search | genmask"
			  + " | jumblept2 | maint ] {-debug}\n"
			  + "About searches: find a word, pattern (like ABBC), "
			  + "substitution encoded word (like GBRRCB),\n or jumbled word "
			  + "(like ISFH, returns fish).\n"
			  + "\tParams for -action search: -searchtype [word | pattern | "
			  + "encword | jumble] -target targetPhrase \n"
			  + "\tParams for -action jumblept2: -target letterList "
			  + "-windowsize n  \n"
			  + "\tParams for -action genmask: -target targetPhrase \n"
			  + "\tParams for -action maint: -mainttype [ gensortcolumn | "
			  + "addword ] -target word_to_add \n "
			  + "\tParams for -action wordle: -include letterList {-require "
			  + "letterList} {-omit letterList} {-mask ..a.b}\n "
			  + "\t\tNote: For -action wordle, include list must contain all "
			  + "letters in the require list.\n "
			  + "\tNote: search for word or encword returns first match, "
			  + "pattern returns all matches.\n")

	def doOSCheck(self, ap):
		rv = False
		if (ap.isArgWithValue("-os", "mac")
		   or ap.isArgWithValue("-os", "win")):
			self.osType = ap.getArgValue("-os")
			rv = True

		return rv

	def doSearchTypeCheck(self, ap, subtestResults, subtestResultMessages):
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
			subtestResultMessages.append("-searchtype %s" % rv)
			subtestResults.append(rv)

			# search also requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResultMessages.append("-target %s" % rv)
			subtestResults.append(rv)

	def doJumblePt2Check(self, ap, subtestResults, subtestResultMessages):
		if (self.action == "jumblept2"):
			rv = False
			if (ap.isInArgs("-windowsize", True)):
				self.windowSize = int(ap.getArgValue("-windowsize"))
				rv = True
			subtestResultMessages.append("-jumblept2 %s" % rv)
			subtestResults.append(rv)

			# JumblePt2 also requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResultMessages.append("-target %s" % rv)
			subtestResults.append(rv)

	def doWorldleCheck(self, ap, subtestResults, subtestResultMessages):
		if (self.action == "wordle"):
			# widowSize is always 5 for Wordle
			self.windowSize = 5

			rv = False
			if (ap.isInArgs("-include", True)):
				self.includeList = ap.getArgValue("-include")
				msg = f"Inc List {self.includeList}"
				print(msg)
				rv = True
			subtestResultMessages.append("-include %s" % rv)
			subtestResults.append(rv)

			# Wordle also may optionally have a require list
			rv = True  # not a required parameter
			if (ap.isInArgs("-require", True)):
				self.requireList = ap.getArgValue("-require")
				self.bHasRequireList = True
				msg = "Req List {0}".format(self.requireList)
				print(msg)
				rv = True
			subtestResultMessages.append("-require %s" % rv)
			subtestResults.append(rv)

			# Wordle also may optionally have a omit list
			rv = True  # not a required parameter
			if (ap.isInArgs("-omit", True)):
				self.bHasOmitList = True
				self.omitList = ap.getArgValue("-omit")
				rv = True
			subtestResultMessages.append("-omit %s" % rv)
			subtestResults.append(rv)

			# Wordle also may optionally have a mask
			rv = True  # not a required parameter
			if (ap.isInArgs("-mask", True)):
				self.bHasMask = True
				self.mask = ap.getArgValue("-mask")
				rv = True
			subtestResultMessages.append("-mask %s" % rv)
			subtestResults.append(rv)

	def parseArgs(self, args):
		# Parse the arguments looking for required parameters.
		# Return false if any tests fail.

		# global osType, action, searchType, targetPhrase

		subtestResults = []
		subtestResultMessages = []
		rval = True

		# Instantiate the ArgParser
		ap = ArgParser(args)

		# check for optional debug flag
		self.bInDebug = ap.isInArgs("-debug", False)

		# check the OS type
		subtestResultMessages.append("-os %s" % self.doOSCheck(ap))
		subtestResults.append(self.doOSCheck(ap))

		# check for action
		self.action = "NOT_SET"
		rv = False
		if (ap.isInArgs("-action", True)):
			# action value must appear after target
			self.action = ap.getArgValue("-action")
			rv = True
		subtestResultMessages.append("-action %s" % rv)
		subtestResults.append(rv)

		# check for searchtype
		# using a different arg parse approach than the OS check.
		self.doSearchTypeCheck(ap, subtestResults, subtestResultMessages)

		# check for JumblePt2
		self.doJumblePt2Check(ap, subtestResults, subtestResultMessages)

		# check for Wordle
		self.doWorldleCheck(ap, subtestResults, subtestResultMessages)

		# check for genmask
		if (self.action == "genmask"):
			# GenMask requires a target
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			subtestResultMessages.append("-genmask %s" % rv)
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
			subtestResultMessages.append("-mainttype %s" % rv)
			subtestResults.append(rv)

		if (self.action == "addword"):
			rv = False
			if (ap.isInArgs("-target", True)):
				self.targetPhrase = ap.getArgValue("-target")
				rv = True
			else:
				rv = False

			subtestResultMessages.append("-addword %s" % rv)
			subtestResults.append(rv)

		# Determine if all subtests passed
		for aMsg in subtestResultMessages:
			if (self.bInDebug):
				msg = "Arg subtest {0}".format(aMsg)
				print(msg)

		for aSubResult in subtestResults:
			rval = rval and aSubResult

		return(rval)

	def getDictionaryLines(self):

		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.dictionaryPath = self.DICTIONARY_FILE__MAC
		else:
			self.dictionaryPath = self.DICTIONARY_FILE__WIN

		# Read the dictionary
		with open(self.dictionaryPath, "r", encoding="utf-8") as file:
			lines = file.readlines()

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
		with open(self.outDictionaryPath + "NEW", "w", encoding="utf-8") as file:
			for aline in lines:
				parts = aline.split(',')
				line2write = aline
				# if the line is commented out, don't add sort column
				if aline[0] != '#':
					line2write = aline.strip() + "," + \
											self.doSortGen(parts[0]) + "\n"
				file.write(line2write)
				outLineCount += 1

		print("Lines written to new dictionary file: " + str(outLineCount))

		return(outLineCount)

	def addWordToDictionary(self, newWord):
		# add the specified word to the dictionary.
		# dictionary entries have the following format:
		# #word,len,pattern,sortedword
		# aardvark,8,AABCDABE,aaadkrrv

		# search the dictionary to see if the word already exists.
		searchResult = self.doSearch("word", newWord)

		if (len(searchResult) > 0):
			print("addWordToDictionary: The word is already in dictionary.")
			return

		# generate line to add to the dictionary
		line2Add = ",".join([newWord,
							 str(len(newWord)),
							 self.doMaskGen(newWord),
							 self.doSortGen(newWord)])
		line2Add = line2Add + "\n"

		print("Line to add: %s" % line2Add)

		# set dictionary path based on OS
		if (self.osType == "mac"):
			self.DictionaryPath = self.DICTIONARY_FILE__MAC
		else:
			self.DictionaryPath = self.DICTIONARY_FILE__WIN

		# open the new file for writing.
		with open(self.DictionaryPath, "a", encoding="utf-8") as file:
			file.write(line2Add)

		print("Lines written to dictionary: " + self.DictionaryPath)

	def generateOdometer(self, letterList, windowSize):
		# factory like method producing an odometer (array of strings)

		odometer = []

		# Note: No shortening of the wheels to remove dupes,
		#		those dupes are skipped by advanceOdometer().
		for x in range(0, windowSize):
			odometer.append(letterList)
			self.showDebugMsg("gen odo %d " % x)

		return odometer

	@staticmethod
	def isOdometerAtMax(odometer, oIdx):

		rval = True

		for i in range(0, len(odometer)):
			if (oIdx[i] < len(odometer[i])-1):
				rval = False

		return rval

	@staticmethod
	def advanceOdometer(odometer, oIdx):
		# Advance the odo and skip any combos where a letter would be repeated.
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
				# Use values this high plus 1 per position to the right
				#  (e.g. +1, +2, +3,... for neghbors to the right).
				# This ONLY WORKS because this result is used in a context
				#   where order of elements doesn't matter.
				#	 (e.g. 012 and 021 are considered dupes so rolling over
				#	 from 019 to 023 skipping 020 and 021 is desirable)
				#  Note: the step after this will correct any exceeding max.
				for x in range(indexToAdvance+1, windowSize):
					oIdx[x] = oIdx[indexToAdvance]+(x-indexToAdvance)

				# Max value is based on combo of odometer length and position.
				# E.G. With 5 values in odometer[n], and a window size of 3
				#   (specified by oIdx length), max values are 2-3-4
				#   (indexes are zero based).
				for x in range(0, windowSize):
					if (oIdx[x] > wheelLength-(windowSize-x)):
						oIdx[x] = wheelLength-1

			# set as done if there are no dupes except for all maxes
			bDone = True
			maxCount = 0
			for x in range(0, len(oIdx)):
				# and (oIdx[x] < wheelLength-1)):
				if (oIdx.count(oIdx[x]) > 1):
					bDone = False

				if (oIdx[x] == wheelLength - 1):
					maxCount += 1

				if (maxCount == windowSize):
					bDone = True

			# check governor
			if (cycleCount > cycleLimit):
				print("advanceOdometer hit governor limit, exiting.")
				bDone = True

	@staticmethod
	def readOdometer(odometer, oIdx):

		rval = ""

		for x in range(0, len(odometer)):
			rval += odometer[x][oIdx[x]]

		return rval

	def buildPhraseListForJumble(self, letterList, windowSize):

		phraseList = []

		# generate odometer and odo index, the odometer is an array of strings.
		odometer = self.generateOdometer(letterList, windowSize)
		oIdx = []
		for i in range(0, len(odometer)):
			oIdx.append(i)

		# Generate Phrase List
		print("Building distinct potential jumble list...")
		odoCycleCount = 0

		# set cycle limit to len of letter list factorial for windowsize range.
		# e.g. letter list of 7, widow size 2 --> 7*6 (stop, aka given 7
		#   letters there are 42 2 letter combos).

		cycleLimit = len(letterList)
		for x in range(len(letterList)-1, len(letterList)-windowSize, -1):
			cycleLimit = cycleLimit * x

		msgInterval = cycleLimit * .1
		ci = msgInterval
		print("Cycle Limit set to %d msgInterval=%d" % (cycleLimit, ci))
		bDone = False
		print("Building Phrase List...")
		while(not bDone):
			odoCycleCount += 1

			phrase = self.readOdometer(odometer, oIdx)
			sortedPhrase = self.doSortGen(phrase)

			if(phraseList.count(sortedPhrase) == 0):
				phraseList.append(sortedPhrase)

			# If at odometer is at max position mark as done, else advance
			if (self.isOdometerAtMax(odometer, oIdx)):
				# remove last item, it is all maxes.
				del phraseList[len(phraseList)-1]
				bDone = True
			else:
				self.advanceOdometer(odometer, oIdx)

			# Check governor for runaway process
			if (odoCycleCount > cycleLimit):
				print("doJumblePt2: Cycle limit governor hit.")
				bDone = True

			if (odoCycleCount > ci):
				pctDone = float(odoCycleCount)/float(cycleLimit)
				print("Working, cycle limit percent consumed = %f" % pctDone)
				ci += msgInterval

		print("Phrase List done, cycles used = %d " % odoCycleCount)

		return phraseList

	def doJumblePt2(self, letterList, windowSize):
		# process Jumble Part 2 using Odometer method.

		phraseList = self.buildPhraseListForJumble(letterList, windowSize)

		# Process phrases through jumble evaluation
		DictionaryEngine.showMsg(
			"Processing, letter combos count = %d " % len(phraseList))

		# Walk the phrase list, finding jumble matches, adding them to
		#   the distinct match list.
		matchList = []
		loopCount = 0
		phraseCount = len(phraseList)
		msgInterval = phraseCount * .1
		ci = msgInterval
		for phrase in phraseList:
			loopCount += 1
			currentMatches = self.doSearch("jumble", phrase)
			if (len(currentMatches) > 0):
				for m in currentMatches:
					if (matchList.count(m) == 0):
						matchList.append(m)

			if (loopCount > ci):
				print("Working, combos processed = {0}".format(
					loopCount*1.0/phraseCount))
				ci += msgInterval

		# end for phrase...

		# show results
		self.showMatchList(matchList)

	def buildPhraseListForWordle(self, includeList, requireList, omitList):

		phraseList = []

		# generate odometer and odometer index, the odo is an array of strings.
		# windowSize is always 5 for Wordle, set in parseArgs in action=wordle
		odometer = self.generateOdometer(includeList, self.windowSize)
		oIdx = []
		for i in range(0, len(odometer)):
			oIdx.append(i)

		# Generate Phrase List
		print("Building distinct potential jumble list...")
		odoCycleCount = 0

		# set cycle limit to len of letter list factorial for windowsize range.
		# e.g. letter list of 7, widow size 2 --> 7*6
		#  (stop, aka given 7 letters there are 42 2 letter combos).

		cycleLimit = len(includeList)
		for x in range(len(includeList)-1, cycleLimit-self.windowSize, -1):
			cycleLimit = cycleLimit * x

		msgInterval = cycleLimit * .1
		ci = msgInterval
		print("Cycle Limit set to %d msgInterval=%d" % (cycleLimit, ci))
		bDone = False
		print("Building potential wordle list...")
		while(not bDone):
			odoCycleCount += 1

			phrase = self.readOdometer(odometer, oIdx)
			sortedPhrase = DictionaryEngine.doSortGen(phrase)

			# check for requireList compatibility
			bMissingRequiredLetter = False
			if (self.bHasRequireList):
				for rLet in requireList:
					if(not self.isInArray(rLet, sortedPhrase)):
						bMissingRequiredLetter = True
						break

			# check for omitList compatibility
			bUsingOmitLetter = False
			if (self.bHasOmitList):
				for oLet in omitList:
					if(self.isInArray(oLet, sortedPhrase)):
						bUsingOmitLetter = True
						break

			if((phraseList.count(sortedPhrase) == 0)
					and (not bMissingRequiredLetter)
					and (not bUsingOmitLetter)):
				phraseList.append(sortedPhrase)

			# If at odometer is at max position mark as done, else advance.
			if (self.isOdometerAtMax(odometer, oIdx)):
				# remove last item, it is all maxes.
				print("DictionaryTools.buildPhraseListForWorlde: Odometer is at Max, removing last item.")
				print(f"index targeted = %d  phraseList size = %d"%(len(phraseList)-1, len(phraseList)))
				if (len(phraseList) > 0):
					del phraseList[len(phraseList)-1]
				bDone = True
			else:
				self.advanceOdometer(odometer, oIdx)

			# Check governor for runaway process
			if (odoCycleCount > cycleLimit):
				print("DictionaryTools.buildPhraseListForWorlde: Cycle limit governor hit.")
				bDone = True

			if (odoCycleCount > ci):
				pctDone = float(odoCycleCount)/float(cycleLimit)
				print("Working, cycle limit percent consumed = %f" % pctDone)
				ci += msgInterval

		print("Potential word list done, cycles used = %d " % odoCycleCount)

		return phraseList

	def doWordle(self, includeList, requireList, omitList, mask):
		# process Wordle using Odometer method.

		phraseList = self.buildPhraseListForWordle(includeList,
												  requireList,
												  omitList)

		# Process phrases through jumble evaluation
		print("Processing, potential word list count = %d " % len(phraseList))

		# Walk the phrase list, finding jumble matches, adding them to
		#   the distinct match list.
		matchList = []
		loopCount = 0
		phraseCount = len(phraseList)
		msgInterval = phraseCount * .1
		ci = msgInterval
		for phrase in phraseList:
			loopCount += 1
			currentMatches = self.doSearch("jumble", phrase)
			if (len(currentMatches) > 0):
				for m in currentMatches:
					# check for mask compatibility
					idx = 0
					bFailMaskCheck = False
					if (self.bHasMask):
						# mask like ..e.t
						matchParts = m.split(',')
						for aLet in mask:
							if(aLet not in (".", matchParts[0][idx])):
								bFailMaskCheck = True
								break
							idx += 1

					if ((matchList.count(m) == 0) and (not bFailMaskCheck)):
						matchList.append(m)

			if (loopCount > ci):
				print("Working, words processed = {0}".format(
					loopCount*1.0/phraseCount))
				ci += msgInterval

		# end for phrase...

		# output just word part of matching dictionary entry
		self.showMatchList(matchList)

	def showMatchList(self, matchList):

		if (len(matchList) == 0):
			self.showMsg("No matches found")
		else:
			self.showMsg("Matching words:")
			for aMatch in matchList:
				matchParts = aMatch.split(',')
				print(matchParts[0])
			self.showMsg("Match count = %d" % len(matchList))

	@staticmethod
	def showMsg(msg):
		print(msg)

	def showDebugMsg(self, msg):
		if (self.bInDebug):
			print(msg)

	def doSearch(self, searchType, targetPhrase):

		rval = []

		# Load the dictionary if not already set
		if (len(self.lines) < 1):
			self.lines = self.getDictionaryLines()

		# determine which index to search; 0 for words, 2 for patterns
		idx = 0
		if (searchType == "pattern"):
			idx = 2
			DictionaryEngine.showMsg("Searching for patterns.")

		if (searchType == "encword"):
			# find a pattern from the encrypted word and do a pattern search
			idx = 2
			targetPhrase = self.doMaskGen(targetPhrase)
			DictionaryEngine.showMsg("Searching for generated pattern.")

		if (searchType == "jumble"):
			# find a sorted pattern from the target word and do a search
			idx = 3
			self.showDebugMsg("Searching for jumbled word %s." %
						 targetPhrase)
			targetPhrase = self.doSortGen(targetPhrase)

		# If the word2find was a phrase, break up the phrase
		#   and search for each word
		w2fParts = targetPhrase.split(' ')
		if (len(w2fParts) > 1):
			DictionaryEngine.showMsg("Searching for each word in the phrase '%s'." %
						 targetPhrase)

		for word2find in w2fParts:
			# work on each word in the phrase
			bFound = False

			# Search for a word
			for line in self.lines:
				parts = line.split(',')
				# word is in part 0
				currentWord = parts[idx].strip()
				if(word2find.lower() == currentWord.lower()):
					self.showDebugMsg(line.strip())
					rval.append(line.strip())
					bFound = True

					# Perf improve: if not searching for a pattern stop after 1
					# 20181223 - Removed limit, search for exact word
					#   as encword failed if not first in results.
					# if (searchType != "pattern"):
					#	break

			# Output not found results
			if (not bFound):
				self.showDebugMsg("%r not found" % word2find)

		return rval

	def doMaskGen(self, rawPhrase):
		# generate a mask for the value in targetPhrase
		rval = ""

		distinctPhraseLetters = []
		patternLetters = []

		# build distinct phrase letters array
		for aLetter in rawPhrase:
			if(not self.isInArray(aLetter, distinctPhraseLetters)):
				distinctPhraseLetters.append(aLetter)

		# populate pattern letters array
		currASCIIVal = 65
		for currASCIIVal in range(65, 65+len(distinctPhraseLetters)):
			patternLetters.append(chr(currASCIIVal))

		# generate mask
		for tpl in rawPhrase:
			maskLetter = self.getCorrespondingEntry(
				tpl, distinctPhraseLetters, patternLetters)
			rval += maskLetter

		# output result
		print("doMaskGen: The mask is " + rval)

		return(rval)

	@staticmethod
	def doSortGen(phrase):
		# Generate a string with chars from phrase in sorted order.

		newphrase = ""

		for ac in sorted(phrase):
			newphrase += newphrase.join(ac)

		return(newphrase)

	@staticmethod
	def getCorrespondingEntry(letter, phraseArray, patternArray):

		rval = "?"

		for x in range(0, len(phraseArray)):
			if (letter == phraseArray[x]):
				rval = patternArray[x]
				break

		return(rval)

	@staticmethod
	def isInArray(letter, phraseArray):

		rval = False

		for aLetter in phraseArray:
			if (letter == aLetter):
				rval = True
				break

		return(rval)

	def doMaint(self):

		if (self.bInDebug):
			print("doMaint: Processing maintenance type [%s]" % self.maintType)

		# determine which maintenance to do
		if (self.maintType == "gensortcolumn"):
			self.writeDictionaryLinesWithSortColumn()

		if (self.maintType == "addword"):
			self.addWordToDictionary(self.targetPhrase)

	def doAction(self):

		if (self.bInDebug):
			print("doAction: Processing action [%s]" % self.action)

		# determine which action to execute
		if (self.action == "search"):
			searchResults = self.doSearch(self.searchType, self.targetPhrase)
			self.showMatchList(searchResults)

		if (self.action == "genmask"):
			self.doMaskGen(self.targetPhrase)

		if (self.action == "jumblept2"):
			self.doJumblePt2(self.targetPhrase, self.windowSize)

		if (self.action == "wordle"):
			self.doWordle(self.includeList, self.requireList,
							self.omitList, self.mask)

		if (self.action == "maint"):
			self.doMaint()

		if (self.action == "addword"):
			self.maintType = "addword"
			self.doMaint()
