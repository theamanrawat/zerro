##Fully automated scanner to find vulnerabilities in web application.
from core.zapspider import ZapSpider
from core.scanner.vulnerabilities import *
from core.utils import utils
from core.subdomains import Scanner
import requests
import time
from urllib.parse import urlparse
import concurrent.futures
from multiprocessing import Process

def StartScanner():
	done = []
	j =''
	while True:
		MainTarget = 'targets.txt'
		for i in open(MainTarget, 'r'):
			url = i.split('\n')[0]
			if url not in done:
				done.append(url)
				if '*.' in url:
					j = url.split('*.')[-1];
					try:
						print(f"[+] Enumerating subdomains : {j}")
						Scanner(j)
						target = 'subdomains/subdomain.txt'
						#http://testphp.vulnweb.com/' 
						for i in open(target, 'r'):
							url = i.split('\n')[0]
							ZapSpider(url).spider()

					except:
						pass
				else:
					try:
						res = urlparse(url)
						if res.scheme == "":
							url = f'http://{url}'
							
						ZapSpider(url).spider()
					except:
						pass


def checkServer():
	try:
		s = socket.socket()
		s.connect(('127.0.0.1',8080))
		started = True
	except:
		started = False
	return started

if __name__ == '__main__':
	start_zap = False
	while True:
		start_zap = checkServer()
		if start_zap == True:
			break
		else:
			pass

	StartScanner()































	# p1 = Process(target=xssInAction, args=(reqUrl, reqMethod, reqBody, ))
	# p1.start()
	# p1.join()

	# done = []
	# j =''
	# while True:
	# 	MainTarget = 'targets.txt'
	# 	for i in open(MainTarget, 'r'):
	# 		url = i.split('\n')[0]
	# 		if url not in done:
	# 			done.append(url)
	# 			if '*.' in url:
	# 				j = url.split('*.')[-1];
	# 				try:
	# 					print(f"[+] Enumerating subdomains : {j}")
	# 					Scanner(j)
	# 					target = 'subdomains/subdomain.txt'
	# 						# #http://testphp.vulnweb.com/' 
	# 					for i in open(target, 'r'):
	# 						url = i.split('\n')[0]
	# 						#ZapSpider(url).spider()

	# 				except:
	# 					pass
	# 			try:
	# 				res = urlparse(url)
	# 				if res.scheme == "":
	# 					url = f'http://{url}'
						
	# 				#ZapSpider(url).spider()
	# 			except:
	# 				pass


