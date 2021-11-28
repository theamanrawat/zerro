import os

def Scanner(domain):
	# os.system(f'amass enum -passive -d {domain} -silent -o subdomains/subdomain-tmp.txt && sublist3r -d {domain} -n -s >> subdomains/subdomain-tmp.txt && cat subdomains/subdomain-tmp.txt | sort -u > subdomains/subdomainUniq.txt && cat subdomains/subdomainUniq.txt | httpx -silent >> subdomains/subdomain.txt')
	os.system(f'sublist3r -d {domain} -n -s | httpx -silent > subdomains/subdomain.txt ')


	