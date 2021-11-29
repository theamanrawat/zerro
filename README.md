# zerro
This is a vulnerability scanner which scans for reflected XSS and SSTI.

### Scanning workflow

1. Enumerate subdomains using [Sublist3r](https://github.com/aboul3la/Sublist3r).
2. Crawl each subdomain using [ZAP](https://github.com/zaproxy/zaproxy).
3. Replace parameter value to HTML tags i:e., `>`, `<` and check for reflection.
4. If found any then it will notify you on discord.

### Installation & Setup

#### Requiremnts

- ZAP Python API
```cmd
pip install python-owasp-zap-v2.4
```

- [Sublist3r](https://github.com/aboul3la/Sublist3r) and [httpx](https://github.com/projectdiscovery/httpx)
- [ZAP Desktop](https://www.zaproxy.org/download/)


#### Setup

1. Install the ZAP and get the API Key.
2. Save the API key in `/config/config.json`

```json
{
	"Version":"0.1",
	"ZapApiKey":"API-KEY-HERE"
}
```
3. Create a discord server and get the webhook URL. Save the webhook URL in `core/utils.py`

```python
def notifyIfFileMofidy():
		web_hook = "WEB-HOOK_URL-HERE"
		webhook = DiscordWebhook(url=web_hook, content=f'[+] Possible XSS reported please check found.txt')
		
```

#### Run

1. Enter target to targets.txt

```
http://testphp.vulnweb.com 
*.evil.com
```

Add `http://` or `https://` for testing single website and `*.` for testing subdomains.

2. Run zerro.py

```
python3 zerro.py
```
