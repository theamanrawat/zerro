import requests
import concurrent.futures
from discord_webhook import DiscordWebhook, DiscordEmbed
import json

class utils:
	def urlWithParam(url, payload):
		finalurl = ''
		if "?" not in url:
			finalurl = url
		else:
			try:
				base_url, parameters = url.split("?")
			except:
				pass
			try:
				if "&" in parameters:
					modif = ""
					for params in parameters.split("&"):
						name, value = params.split("=")
						modif += name + "=" + payload + "&"
					finalurl = base_url + "?" + modif.strip("&")
				else:
					finalurl = url.split("=")[0] + "=" + payload
			except:
				finalurl = url
		return finalurl

	def paramInPostBody(postBody, payload):
		finalBody = ""
		try:
			if "&" in postBody:
				modif = ""
				for params in postBody.split("&"):
					name, value = params.split("=")
					modif += name + "=" + payload + "&"
				finalBody = modif.strip("&")
			else:
				finalBody = url.split("=")[0] + "=" + payload
		except:
			finalBody = postBody

		return finalBody


	def convertStringToDict(values):
		res = [] 
		for sub in values.replace("}", "").replace("{", "").replace("\"").split(', '): 
			if ':' in sub: 
				res.append(map(str.strip, sub.split(':', 1))) 
		res = dict(res) 

		return res

	def updateKeyValues(reqPayload, oldValues, newValues):
		for key in oldValues:
			reqPayload.update({key:newValues})
		return reqPayload

	def sendRequest(reqUrl, reqPayload, reqMethod):
		response = ""
		try:
			if reqMethod == "GET":
				response = requests.get(reqUrl, timeout=6).text.lower()
			elif reqMethod == "POST":
				response = requests.post(reqUrl, timeout=6, data=reqPayload).text.lower()
		except:
			pass
		return response

	def sendConcurrentReq(data):
		with concurrent.futures.ProcessPoolExecutor() as executor:
			results = executor.map(lambda args: utils.sendRequest(*args), data)
		return results

	def createPostPayload(postBody):
		reqPayload = {}
		key = []
		if postBody:
			postBody = postBody.split("&")
			for post in postBody:
				post = post.split("=")
				reqPayload[post[0]] = post[1]
				key.append(post[0])

		return reqPayload, key

	def saveFinding(url):
		f = open('output/found.txt', 'a')
		f.write(f"possible xss :{url}\n")

	def notifyIfFileMofidy():
		web_hook = "https://discord.com/api/webhooks/795898237843537920/azY5CzIJ4ECn8Bzut3fdgY2euSrCzc7wPT5-ORkRULVrpFwG_WlQx6qUZlfminhDU5DU"
		#webhook_urls = [web_hook]
		webhook = DiscordWebhook(url=web_hook, content=f'[+] Possible XSS reported please check found.txt')
		with open("output/found.txt", "rb") as f:
			webhook.add_file(file=f.read(), filename='found.txt')
		webhook.execute()

	def checkUpdate():
		remoteVersionUrl = "https://raw.githubusercontent.com/theamanrawat/zerro/main/config/config.json"
		with open("config/config.json") as data:
			localVersion = json.loads(data.read())["Version"]
			#print(version)
		remoteVersion = json.loads(requests.get(remoteVersionUrl).text)["Version"]
		if localVersion != remoteVersion:
			print(f"Update available version :{remoteVersion}")
			exit()
