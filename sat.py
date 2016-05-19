# coding= utf-8
import operator
import re
import sys
import codecs
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser



def data_sat(filename):
	tempstr=""
	names={}

	with open(filename) as f:
		lines = f.readlines()
	for x in lines:
		tempstr=x.split("\t")[0]
		if tempstr in names:
			names[tempstr] +=1
		else:
			names[tempstr]=1
			pass
		pass
	
	f=open("sum.txt","w")
	orient=sorted(names.items(), key=operator.itemgetter(1))
	for x in orient:
		# print x[0]+" occur "+str(x[1])+" times"
		f.write(x[0]+"\t"+str(x[1])+"\n")
	f.close()

class itemObj(object):
	"""docstring for itemObj"""
	def __init__(self, name, message):
		super(itemObj, self).__init__()
		self.name = name
		self.times = 1
		tmessage = re.sub(r"[\s]","",message)
		if tmessage==" ":
			tmessage = "quote"
			pass
		self.message=tmessage
		self.message+=";"
	def appendMsg(self, message):
		self.times += 1
		tmessage = re.sub(r"[\s]","",message)
		if tmessage==" ":
			tmessage = "quote"
			pass
		self.message+=tmessage
		self.message+=";"
		pass

def all_sat(filename):
	tempstr=""
	table={}
	with open(filename) as f:
		lines = f.readlines()
	for x in lines:
		tempstr=x.split("\t")[0]
		# print x.split("\t")[8]
		if tempstr in table:
			table[tempstr].appendMsg(x.split("\t")[9])
		else:
			tempit = itemObj(tempstr,x.split("\t")[9])
			# tempit["message"].append(x.split("\t")[5])
			table[tempstr]=tempit
			pass
		pass

	orient=sorted(table.values(), key=lambda x: x.times, reverse=True)
	f=open("sum.txt","w")
	for x in orient:
		f.write(x.name+"\t"+str(x.times)+"\t"+x.message+"\n")
		pass
	# orient=sorted(table.items(), key=operator.itemgetter(1))
	# for x in orient:
	# 	# print x[0]+" occur "+str(x[1])+" times"
	# 	f.write(x[0]+"\t"+str(x[1])+"\n")
	f.close()

def chineseSplit(filename,topK,target):

	file_name = filename
	buff="".encode("utf-8")
	# content = open(file_name, 'rb').read()
	with codecs.open(filename, encoding='utf-8') as f:
		lines = f.readlines()
	for x in lines:
		tags = jieba.analyse.extract_tags(x.split("\t")[2], topK=topK)
		buff += x.split("\t")[0]+'\t'+x.split("\t")[1]+'\t'+",".join(tags)+'\n'
		pass
	f=open(target,"w")
	f.write(buff.encode("utf-8"))
	f.close

	return

def main():
	all_sat("result.txt")		
	chineseSplit("sum.txt",20,"cut.txt")

	pass


if __name__ == '__main__':
	main()
