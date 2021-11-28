from core.subdomains import Scanner

if __name__ == '__main__':
	targetUrl = ""
	MainTarget =  "targets.txt" #"testTarget.txt" #
	for targetUrl in open(MainTarget, "r"):
		targetUrl = targetUrl.split("\n")[0]
		if "*." in targetUrl:
			targetUrl = targetUrl.split("*.")[-1]
			print(f"[+] Enumerating subdomains : {targetUrl}")
			Scanner(targetUrl)