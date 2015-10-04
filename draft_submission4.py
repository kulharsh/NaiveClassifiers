import nltk
from nltk.stem.porter import *
from collections import Counter



def calculatePriorProbabilityOfClass():
	print 'Calculating Prior Probabilities...'
	file = open('train.tsv','r')
	file.readline()
	for line in file :
		probabilityOfClass[line.split('\t')[3][:-1]] = probabilityOfClass[line.split('\t')[3][:-1]]+1
	numberOfPhrases = probabilityOfClass['0'] + probabilityOfClass['1'] + probabilityOfClass['2'] + probabilityOfClass['3'] + probabilityOfClass['4']
	for class1 in classes:
		probabilityOfClass[str(class1)] = float(probabilityOfClass[str(class1)] / (float)(numberOfPhrases))


def countVocabularyFromFile():
	print 'Calculating vocabulary size..'
	file = open('train.tsv','r')
	file.readline()
	outFile = open('Vocabulary.txt','w')
	for line in file :
		for w in line.split('\t')[2].split():
			outFile.write(w + '\n')

def createFilesOfClasses():
	file = open('train.tsv','r')
	file.readline()
	for line in file :
		outFile = open(line.split('\t')[3][:-1]+'.txt','a')
		outFile.write(line.split('\t')[2] + '\n')
		outFile.close()

def createFrequncyFiles():
	print 'Creating Frequency Files'
	createFilesOfClasses()
	stemmer = PorterStemmer()
	for class1 in classes:
		print 'Processing '+str(class1)+'...'
		counter = Counter()
		readFile = open(str(class1)+'.txt','r')
		for line in readFile :
			for word in line.split():
				counter[stemmer.stem(word.lower()).lower()] = counter[stemmer.stem(word.lower()).lower()] +1
		writeFile = open('StemWordFreq_'+str(class1)+'.txt','w')
		for word in counter:
			writeFile.write(word+'--->'+str(counter[word])+'\n')
		writeFile.close()
		readFile.close()

def getWordFrequencyFromFile(class1,word):
	file = open('StemWordFreq_'+str(class1)+'.txt')
	for line in file:
		if line.split('--->')[0].lower() == word.lower() :
			return int(line.split('--->')[1][:-1])
	return 0

def getProbabilityForClassForWord(class1,word):
	wf1 = getWordFrequencyFromFile(class1,word)
	den = wordsInClass[class1] + vocabulary
	probability = (float)(( wf1 + 1 ) / float(den))
	return probability

def countVocabulary():
	readFile = open('Vocabulary.txt','r')
	wordSet = set(readFile.readlines())
	vocabulary = len(wordSet)
	return vocabulary

'''def createWFFiles():
	file = open('train.tsv','r')
	file.readline()
	for line in file :
		word_list = word_list + line.split('\t')[3]
	unique_words = set(word_list)
	vocabulary = len(wordSet)'''

def calculateWordsInClass():
	for class1 in classes:
		num = 0
		file = open('StemWordFreq_'+str(class1)+'.txt')
		print 'Processing file '+str(class1)+ ':'
		for line in file:
			n = line.split('--->')[1][:-1]
			num = num + int(n)
		wordsInClass[class1] = num
		file.close()
 
def processsLine(inputLine):
	maxPrediction = -99
	maxClass = -99
	words = inputLine.split()
	stemmer = PorterStemmer()
	inputLine = " ".join((stemmer.stem(w) for w in inputLine.split() if w.lower() not in stopWords))
	for class1 in classes:
		currentMultiplication = 1
		for word in inputLine.split():
			currentMultiplication = currentMultiplication * getProbabilityForClassForWord(class1,word)
		currentMultiplication  = probabilityOfClass[str(class1)] * currentMultiplication
		if maxPrediction < currentMultiplication :
			maxPrediction = currentMultiplication
			maxClass = class1
	return maxClass



def createSubmission():
	print 'Creating submission'
	testFile = open('test.tsv','r')
	submissionFile = open('stemmingSubmission.txt','w')
	line = testFile.readline()
	submissionFile.write('PhraseId,Sentiment\n')
	for line in testFile:
		try :
			phraseId = line.split('\t')[0]
			sentence = line.split('\t')[2]
		except:
			continue
		submissionFile.write(phraseId)
		submissionFile.write(',')
		submissionFile.write(str(processsLine(sentence)))
		submissionFile.write('\n')
		print phraseId
	submissionFile.close()	

if __name__ =="__main__":
	classes = [0,1,2,3,4]
	wordsInClass = {'0':0,'1':0,'2':0,'3':0,'4':0}
	probabilityOfClass = {'1':0,'2':0,'3':0,'4':0,'0':0}
	stopWords = ['a','an','the']
	countVocabularyFromFile()
	vocabulary = countVocabulary()
	createFrequncyFiles()
	calculateWordsInClass()
	calculatePriorProbabilityOfClass()
	createSubmission()
