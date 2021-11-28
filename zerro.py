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

if __name__ == '__main__':
	# SSTI : https://ac0d1f571f1a22ba81b8119800b600b4.web-security-academy.net
	# XSS  : http://testphp.vulnweb.com

	# utils.checkUpdate()
	# targetUrl = ""
	# done = []
	# #MainTarget =  "testTarget.txt" #"targets.txt" #t
	# while True:
	# 	target = 'subdomains/subdomain.txt'  #http://testphp.vulnweb.com/' 
	# 	for subs in open(target, 'r'):
	# 		url = subs.split('\n')[0]
	# 		if url not in done:
	# 			done.append(url)
	# 			ZapSpider(url).spider()

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
						# #http://testphp.vulnweb.com/' 
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


