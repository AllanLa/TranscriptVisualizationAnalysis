''' Complete your program here. '''
import re #importing regular expression library

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
	dic = {}

	#regularExpression designed to specifically parse for NAMES
	reg = re.compile(r"[A-Z]+:")

	prevEnd = None
	prevSpeaker = None

	"""Iterates through each match object, finds the start and end of"""
	for match in reg.finditer(debateLines):
		position = match.span() #gets the tuple object of the start/end of matched
		start = position[0]
		end = position[1]

		speaker = debateLines[start:end].rstrip('\'\"-,.:;!?')
		

		if prevSpeaker in dic:
			dic[prevSpeaker] += [debateLines[prevEnd:start]]

		if speaker not in dic:
			dic[speaker] = [] #initializes dictionary with speaker key, sets value to an empty list

		prevSpeaker = speaker
		prevEnd = end


main()
