''' Complete your program here. '''
import re #importing regular expression library
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

#Speakers to ignore in the transcript
IGNORE_SPEAKERS = ["MODERATOR", "PARTICIPANTS", "MODERATORS", "QUESTION"]

def main():
# Inputting a file
	while True:
		#try:
		fileName = raw_input("Type in file name in the format e.g. 'FileName.txt': ")
		fileIn = open(fileName, 'rt')

		break
#	except  Exception:
		print("File not found, make sure it is in same working directory.")
		print("Press Ctrl + C to escape.\n")
	
	# This will create a long string of the debate file
	debateLines = fileIn.read()

	#dictionary to hold each speaker (key) and their words (values)
	dic = extractSpeakers(debateLines)

	cleanDic(dic) #removes speakers based on the global ignore list, pass by reference

	information = analysis(dic) #returns a list [dic_unique_words, dic_total_words]

	uniqueDic = information[0]
	totalDic = information[1]

	plotTotalWords(totalDic)
	plotUniqueWords(uniqueDic)

def cleanDic(dic):
	"""for each speaker in the global ignore_speakers, this function will remove
	those speakers from the dictionary"""
	for ignore in IGNORE_SPEAKERS:
		if ignore in dic:
			del dic[ignore]

def extractSpeakers(transcriptText):
	"""Takes in a string of the entire debateText and returns a dictionary holding
	each speaker has a key and the value as a long string of what the speaker has said
	in the transcript"""

	dic = {} #initializes the dictionary

	reg = re.compile(r"[A-Z]+:") #regular expression to parse for NAME:

	prevEnd = None
	prevSpeaker = None

	"""Iterates through each match object, finds the start and end of
	each time SPEAKER: appears, then adds what they say to the dictionary"""
	for match in reg.finditer(transcriptText):
		position = match.span() #gets the tuple object of the start/end of matched
		start = position[0] #gets starting position of when speaker first appeared
		end = position[1] #gets ending position of when speaker first appeared

		speaker = transcriptText[start:end].rstrip('\'\"-,.:;!?') #cleans up the string
		

		if prevSpeaker in dic:
			dic[prevSpeaker] += transcriptText[prevEnd:start]

		if speaker not in dic:
			dic[speaker] = "" #initializes dictionary with speaker key, sets value to an empty string

		prevSpeaker = speaker
		prevEnd = end

	#loop skips the last portion of the transcript of the prevSpeaker so just add the rest of transcript
	dic[prevSpeaker] += transcriptText[prevEnd:]

	return dic



def analysis(dic):
	"""takes in a dictionary that holds each speaker as a key, and everything they said
		as a value in the form of a long string, and returns a dictionary using again
		each speaker as a key, and the amount of unique words as a value"""

	uniqueCountDic = {}
	totalCountDic = {}

	for speaker in dic:
		sentence = dic[speaker]
		listOfWords = sentence.split()

		totalCountDic[speaker] = len(listOfWords) #total words used

		count = 0
		tempDic = {} #used temp to optimize code to find #unique words
		for word in listOfWords:
			cleanWord = word.rstrip('\'\"-,.:;!?')
			cleanWord = cleanWord.lower() #make words are not case sensitive
			if cleanWord in tempDic:
				pass

			else:
				count +=1
				tempDic[cleanWord] = "" 

		uniqueCountDic[speaker] = count


	return [uniqueCountDic, totalCountDic]


def plotTotalWords(totalDic):
	"""takes in a dictionary with keys as speakers and values
	assosicated to the speakers as the total number of words the speaker used"""

	speakers = totalDic.keys()
	y_pos = np.arange(len(speakers))
	performance = totalDic.values()

	plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, speakers)
	plt.ylabel('Number of Words')
	plt.title('Total Words Used')
	plt.figure()



def plotUniqueWords(uniqueDic):
	"""takes in a dictionary with keys as speakers and values
	assosicated to the speakers as the total number of words the speaker used"""
	speakers = uniqueDic.keys()
	y_pos = np.arange(len(speakers))
	performance = uniqueDic.values()

	plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, speakers)
	plt.ylabel('Number of Unique Words')
	plt.title('Unique Words Used')
	plt.show()

main()
