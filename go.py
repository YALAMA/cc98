# coding= utf-8
from cc98 import *
from bs4 import *
from threading import *
from Queue import *
from time import *
from sat import *
import json
import re

# from pymongo import MongoClient
# DBClient = MongoClient()
# # DBClient = MongoClient('10.110.91.236')
# DBSave = DBClient["cc98"]
# Collection = DBSave["soul"]
# DBLog = DBClient["log"]
# LogColl = DBLog["Error"]

name = "ph-test"
password = "1qaz"

UrlSite = "http://www.cc98.org/"

#display site
DispSite = "http://www.cc98.org/dispbbs.asp" 

#list post site
ListSite = "http://www.cc98.org/list.asp"


#the boardID of the each board
BoarIdInfo = {
	"soul":182,
	"love":152
}
expls=["4626324","4593133","4238943","4424124"]

cc = cc98(name,password)


record=[];
#Page to be parsed Queue
PageToParseQueue = Queue()

def save_post_info(filename):
	f=open(filename,"w");
	counter=1
	while not PageToParseQueue.empty():
		buff="".encode('utf-8');
		PageInfo = PageToParseQueue.get()
		BoardId = PageInfo[0]
		PostId = PageInfo[1]
		PageNum = PageInfo[2]
		url = DispSite + "?boardID=" + BoardId + "&ID=" + PostId + "&star=" + PageNum
		# print url+"\n"		
		try:
			response = cc.opener.open(url)
			soup = BeautifulSoup(response.read(), "lxml")
		except:
			print "Http Request Error"	
		pass
		# f.write(soup.get_text().encode('utf-8')) 
		templs=soup.find_all('table', class_ = "tableborder1")
		counter += 1
		print "parsing...."+str(counter)+"\n"
		for i in templs[1:-1]:
				# f.write(''.join(i.get_text().encode('utf-8').split())+'\n')
				# break
			# try:
			 	info_tr1 = i.tr
			 	# info_tr2 = info_tr1.next_sibling
			 	info_tr2 = info_tr1.next_sibling.next_sibling
			 	info_tr1_td1 = info_tr1.td
			 	info_tr1_td2 = info_tr1_td1.next_sibling.next_sibling
			 # 	# info_tr1_td2 = info_tr1_td1.next_sibling.next_sibling
			 	FloorInfo = {}
			 	FloorInfo["user"] = info_tr1_td1.td.b.string.encode('utf-8')
			 	FloorInfo["floor"] = ''.join(info_tr1_td2.tr.get_text().encode('utf-8').split())
			 	TimeData = info_tr2.td.contents[2].string.encode('utf-8')
			 	FloorInfo["TimeData"] = re.sub(r'[\r\n]','',TimeData)
			 	# print re.search(r'\d+/\d+/\d+', TimeData).group()
			 	# FloorInfo["date"] = re.search(r'\d+/\d+/\d+', TimeData).group()
			 	# FloorInfo["time"] = re.search(r'\d+:\d+:\d+\s\w+', TimeData).group()
			 	# FloorInfo["message"] = ''.join(info_tr1_td2.article.get_text().encode('utf-8').split());
			 	# .encode('UTF-8')
			 	FloorInfo["message"]=''.join(info_tr1_td2.article.get_text().encode('utf-8').split()).strip("")
			 	FloorInfo["message"] = re.sub(r'\[[a-z\=\,0-9]*\]\S*\[\/[a-z]*\]','',FloorInfo["message"])
			 	FloorInfo["message"] = re.sub(r'searchubb\(\S*\)\;','',FloorInfo["message"])			 	

			 	# FloorInfo["message"] = info_tr1_td2.article
			 # 	FloorInfo['BoardId'] = int(BoardId)
			 	FloorInfo['PostId'] = PostId
			 # 	FloorInfo['PageNum'] = int(PageNum)
				# print json.dumps(FloorInfo)
				buff+=FloorInfo["user"]+"\t"
				buff+=FloorInfo["PostId"]+"\t"
				buff+=FloorInfo["TimeData"]+"\t"
				buff+=FloorInfo["floor"]+"\t"
				buff+=FloorInfo["message"]+"\n"
		f.write(buff)
				# f.write(FloorInfo["user"])
				# f.write("\t")
				# f.write(FloorInfo["PostId"])
				# f.write("\t")	
				# # f.write(FloorInfo["date"])
				# # f.write("\t")						
				# f.write(FloorInfo["TimeData"])
				# f.write("\t")						
				# f.write(FloorInfo["floor"])
				# f.write("\t")
				# f.write(FloorInfo["message"])
				# f.write('\n')
			# except:
			# 	print "io Error"
	f.close()
def save_post_info_ori():
	while True:
		PageInfo = PageToParseQueue.get()
		BoardId = PageInfo[0]
		PostId = PageInfo[1]
		PageNum = PageInfo[2]
		url = DispSite + "?boardID=" + BoardId + "&ID=" + PostId + "&star=" + PageNum
		try:
			response = cc.opener.open(url)
			soup = BeautifulSoup(response.read(), "lxml")
		except:
			print "Http Request Error"
			ErrInfo = {}
			ErrInfo["PageInfo"] = PageInfo
			ErrInfo["BoardId"] = int(BoardId)
			ErrInfo["PostId"] = int(PostId)
			ErrInfo["PageNum"] = int(PageNum)
			LogColl.insert(ErrInfo)
			pass
		#each floor
		for i in soup.find_all('table', class_ = "tableborder1"):
			 try:
			 	info_tr1 = i.tr
			 	info_tr2 = info_tr1.next_sibling.next_sibling
			 	info_tr1_td1 = info_tr1.td
			 	info_tr1_td2 = info_tr1_td1.next_sibling.next_sibling
			 	FloorInfo = {}
			 	FloorInfo["user"] = info_tr1_td1.td.b.string
			 	FloorInfo["floor"] = ''.join(info_tr1_td2.tr.get_text().split())
			 	TimeData = info_tr2.td.contents[2].string
			 	FloorInfo["date"] = re.search(r'\d+/\d+/\d+', TimeData).group()
			 	FloorInfo["time"] = re.search(r'\d+:\d+:\d+\s\w+', TimeData).group()
			 	FloorInfo["message"] = info_tr1_td2.blockquote.span.get_text()
			 	FloorInfo['BoardId'] = int(BoardId)
			 	FloorInfo['PostId'] = int(PostId)
			 	FloorInfo['PageNum'] = int(PageNum)
			 	try:
			 		Collection.insert(FloorInfo)			 		
			 	except:
			 		print "MongoDB insert Error!"
			 except:
			 	pass
	return

#according to the board, calculate the pages
BoardQueue = Queue()
BoardPageQueue = Queue()
def parse_board(page):
	while not BoardQueue.empty():
		BoardId = BoardQueue.get()
		BoardUrl = ListSite + "?boardid=" + BoardId
		try:
			response = cc.opener.open(BoardUrl)
			soup = BeautifulSoup(response.read(), "lxml")
		except:
			print "Board Parse Request Error!"
		Info = soup.body.form.next_sibling.next_sibling.td.get_text()
		# print "Info is "+Info
		BoardLen = re.search(r'1/\d+', Info).group()[2:]
		# for i in range(1,int(BoardLen)+1):
		if page==0:
			page=int(BoardLen)
			pass
		for i in range(1,page+1):
			BoardPageQueue.put([BoardId, str(i)])
	return

#parse each page to find the length of each post in this page
def parse_page():
	while not BoardPageQueue.empty():
		[BoardId, BoardPage] = BoardPageQueue.get()
		PageUrl = ListSite + "?boardid=" + BoardId + "&page=" + BoardPage
		# print PageUrl
		try:
			response = cc.opener.open(PageUrl)
			soup = BeautifulSoup(response.read(), "lxml")
		except:
			print "Page Parse Request Error!"
		#find the ID of the post
		IdPattern = re.compile(r'&ID=\d+')
		for i in soup.find_all('td', class_ = "tablebody1"):
			try:
				UrlHref = i.find_all('a')
				PostId = IdPattern.search(UrlHref[0]['href']).group()[4:]
				if PostId in expls:
					print "pass"
					continue
				if len(UrlHref) == 1:
					PostLen = 1
				else:
					PagePattern = re.compile(r'star=\d+')
					#the link to the last page of the post
					LastPage = UrlHref[-1]['href']
					PostLen = int(PagePattern.search(LastPage).group()[5:])
				for i in range(1, PostLen+1):
					PageToParseQueue.put([BoardId, PostId, str(i)])
					print [BoardId, PostId, str(i)]
			except:
				pass
	return
		
def queue_info():
	print "here"
	while True:
		print "PageToParseQueue:", PageToParseQueue.qsize()
		print "BoardQueue:", BoardQueue.qsize()
		print "BoardPageQueue", BoardPageQueue.qsize()
		sleep(5)


BoardList = ["182"]
def get_board():
	for i in BoardList:
		BoardQueue.put(i)
	return

ThreadList = []
def main():

	cc.login()
	get_board()
	parse_board(100)

	parse_page()
	save_post_info("result.txt")
	all_sat("result.txt")		
	chineseSplit("sum.txt",20,"cut.txt")

if __name__ == '__main__':
	main()
