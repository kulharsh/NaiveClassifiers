from collections import Counter
def writeCounter(fileName, counterToWrite, lineNumber = 0):
	file = open(fileName, 'a');
	if lineNumber :
		file.write(lineNumber + '\n')
	for word in counterToWrite:
		file.write(word + '-->' + str(counterToWrite[word])+'\n')
	file.close()

def createAMatrix():
	#dictionary = dict()
	file = open('train.tsv','r')
	#counter = Counter()
	for line in file:
		for word in set(line.split('\t')[2].split()):
			vocabCounter[word] = vocabCounter[word] + 1
	file.close()
	writeCounter("vocabulary.txt",vocabCounter)
	file = open('train.tsv','r')
	for line in file:
		print line
		lineCounter = Counter(vocabCounter.keys())
		#print len(lineCounter) 
		for word in line.split('\t')[2].split():
			lineCounter[word] = lineCounter[word] + 1
		writeCounter("vectors.txt",lineCounter, line.split('\t')[0])

		#for word in lineCounter:
			#print word + '---->' + str(lineCounter[word])
		
        
		#dictionary[line.split('\t')[0]] = counter
	#return dictionary

if __name__ == "__main__":
	vocabCounter = Counter()
	createAMatrix()
	print len(vocabCounter)
	#for item in counter:
		#print item
		#print counter[item]