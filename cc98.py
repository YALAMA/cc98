import hashlib
import urllib
import urllib2
import cookielib

class cc98():
	def __init__(self, name, pwd):
		self.name = name
		self.pwd = pwd = hashlib.md5(pwd).hexdigest()
		# self.cj = cookielib.CookieJar()
		self.cj = cookielib.LWPCookieJar("cook1")
		try:
			self.cj.load()
			self.method="ck"
			print "login_with_ck"
		except:
			self.method="pw"
			print "login_with_pw"

		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

	def login(self):
		if self.method=="ck":
			self. login_with_ck();
		else:
			self. login_with_pw();
			
	def login_with_ck(self):
		LogUrl = "http://www.cc98.org/sign.asp"
		try:
			req = urllib2.Request(LogUrl)
		except:
			print "Request Error!"
			print req

		try:
			response = self.opener.open(req)
		except:
			print "Open Error!"
			# print response		

	def login_with_pw(self):
		params = {
				'a':'i',
				'u':self.name,
				'p':self.pwd,
				'userhidden':1
		}

		data = urllib.urlencode(params)
		LogUrl = "http://www.cc98.org/sign.asp"
		try:
			req = urllib2.Request(LogUrl, data)
		except:
			print "Request Error!"
			print req

		try:
			response = self.opener.open(req)
		except:
			print "Open Error!"
			# print response
		self.cj.save()


def main():
	name = "ph-test"
	password = "1qaz"
	url_soul = "http://www.cc98.org/list.asp?boardid=182"
	cc = cc98(name, password)
	cc.login()
	response = cc.opener.open(url_soul)
	f=open("result.html","w");
	f.write( response.read())

if __name__ == '__main__':
	main()


