# -*- coding: utf-8 -*-
import codecs
import utils
import re
import sys
from nltk.metrics import edit_distance

def hasNumbers(inputString):
	return bool(re.search(r'\d',inputString))

def hasBrackets(inputString):
	return bool(re.search(r'\[|\]|\)|\(',inputString))

def hasAlphabets(inputString):
	return bool(re.search(r'[a-zA-Z]',inputString))

def hasSpecialCharacters(inputString):
	return bool(re.search(r'\|',inputString))

if __name__ == '__main__':

	source = sys.argv[1]+"/"
	source += sys.argv[2]
	language = sys.argv[4]
	number_of_edits = int(sys.argv[5])
	output = sys.argv[3]
	files = codecs.open(output+"/spelling_error.txt","a", encoding='utf-8')
	files_2 = codecs.open(output+"/orig_sen.txt","a", encoding='utf-8')
	files_3 = codecs.open(output+"/error_sen.txt","a", encoding='utf-8')
	revisions = []
	line = []
	f=0

	with codecs.open(source,'r') as f1:
		text = f1.read()
		to_write_uni = unicode(text, encoding='utf-8', errors='ignore')
		for lines in to_write_uni.split("\n"):
			lines = re.sub(r'\n',"",lines)
			if(len(lines)>1):
				line.append(lines)

	for i in range(0,len(line)):
		if("Revision timestamp" in line[i]):
			i+=1
			s=""
			#print(line[i].decode('unicode-escape'))
			while i<len(line) and "Revision timestamp" not in line[i]:
				s+=line[i]
				i+=1
			revisions.append(s)

	if language == "hindi":
		for i in range(1, len(revisions)):
			earlier = revisions[i-1].split(u'। ')
			current = revisions[i].split(u'। ')
			if len(earlier)==len(current):
				for j in range(0, len(earlier)):
					f=0
					earlier_words = earlier[j].split(' ')
					current_words = current[j].split(' ')
					if(len(earlier_words) == len(current_words)):
						for k in range(0,len(earlier_words)):
							if earlier_words[k]==current_words[k]:
								continue
							elif hasNumbers(earlier_words[k])==False and hasBrackets(earlier_words[k])==False :
								if hasAlphabets(earlier_words[k])==False and hasSpecialCharacters(earlier_words[k])==False:
									edits = edit_distance(earlier_words[k],current_words[k], transpositions=True)
									print(earlier_words[k])
									if(edits > 0 and edits<=number_of_edits):
										files.write(current_words[k]+"	:	"+earlier_words[k]+"\n")
										f=1
					if(f==1):
						files_2.write(earlier[j]+"\n")
						files_3.write(current[j]+"\n")
	else:
		for i in range(1, len(revisions)):
			earlier = revisions[i-1].split(u'. ')
			current = revisions[i].split(u'. ')
			if len(earlier)==len(current):
				for j in range(0, len(earlier)):
					f=0
					earlier_words = earlier[j].split(' ')
					current_words = current[j].split(' ')
					if(len(earlier_words) == len(current_words)):
						for k in range(0,len(earlier_words)):
							if earlier_words[k]==current_words[k]:
								continue
							elif hasNumbers(earlier_words[k])==False and hasBrackets(earlier_words[k])==False :
								if hasSpecialCharacters(earlier_words[k])==False:
									edits = edit_distance(earlier_words[k],current_words[k], transpositions=True)
									print(earlier_words[k])
									if(edits > 0 and edits<=number_of_edits):
										files.write(current_words[k]+"	:	"+earlier_words[k]+"\n")
										f=1
					if(f==1):
						files_2.write(earlier[j]+"\n")
						files_3.write(current[j]+"\n")
	files.close()
	files_2.close()
	files_3.close()
