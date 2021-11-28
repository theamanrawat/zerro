from core.colors import green, white, end, info, bad, good, run
from core.utils import utils
from zapv2 import ZAPv2
import requests
from core.scanner.vulnerabilities import *
import json
import time
import os

class ZapSpider:
	def __init__(self, target):
		self.target = target
	
	def spider(self):
		with open("config/config.json") as data:
			self.ZapApiKey = json.loads(data.read())["ZapApiKey"]

		zap = ZAPv2(apikey=self.ZapApiKey)
		startFileSize = os.stat("output/found.txt").st_size
		print("%sSpidering target {}".format(self.target)%info)
		scanID = zap.spider.scan(self.target)
		while int(zap.spider.status(scanID)) < 100:
			time.sleep(1)
			# tmpResult = zap.spider.results(scanID)
			# if len(tmpResult) >= 70000:
			# 	self.stopScan()
		# saved result as array in `results` variable
		results = zap.spider.full_results(scanID)
		
		duplicatePostValues, duplicateGetValues, dataForScan = [], [], []

		for result in results[0]["urlsInScope"]:
			try:
				requestInZap = self.getRequestBody(result["messageId"]).json()["messagesById"][0]
				reqUrl = utils.urlWithParam(result["url"], "payload0987654321test")
				reqMethod = result["method"]
				reqBody = utils.paramInPostBody(requestInZap["requestBody"], "payload0987654321test")
			except:
				pass
			if reqBody:
				if reqUrl not in duplicatePostValues:
					dataForScan.append((reqUrl, reqMethod, reqBody, requestInZap))
					duplicatePostValues.append(reqUrl)

			if reqUrl not in duplicateGetValues:
				if "=" in reqUrl:
					dataForScan.append((reqUrl, reqMethod, reqBody, requestInZap))
				duplicateGetValues.append(reqUrl)

		print("[+] scanning started")
		with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
		 	executor.map(lambda args: startScan(*args), dataForScan)

		endFileSize = os.stat("output/found.txt").st_size
		if endFileSize > startFileSize:
			utils.notifyIfFileMofidy()
		print("[+] scanning done")

		self.deleteSite()

	def getRequestBody(self, msgId):
		headers = {
		'Accept': 'application/json',
		'X-ZAP-API-Key': self.ZapApiKey
		}
		message = requests.get('http://127.0.0.1:8080/JSON/core/view/messagesById/', params={
			'ids': msgId
			}, headers = headers)
		return message

	def deleteSite(self):
		headers = {
		  'Accept': 'application/json',
		  'X-ZAP-API-Key': self.ZapApiKey
		}
		requests.get('http://127.0.0.1:8080/JSON/core/action/deleteSiteNode/', params={'url': self.target}, headers = headers)

	def removeScan(self):
		headers = {
		'Accept': 'application/json',
		'X-ZAP-API-Key': 'API_KEY'
		}
		requests.get('http://zap/JSON/stats/action/clearStats/', params={}, headers = headers)

	def stopScan(self):
		headers = {
  			'Accept': 'application/json',
  			'X-ZAP-API-Key': self.ZapApiKey
		}
		requests.get('http://127.0.0.1:8080/JSON/spider/action/stop/', params={}, headers = headers)