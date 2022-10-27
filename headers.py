import random 
 
chrome_linux_88 = { 
	# ... 
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36', 
} 
 
chromium_linux_92 = { 
	# ... 
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
} 
 
firefox_linux_88 = { 
	# ... 
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0', 
} 
 
headers = [ 
	chrome_linux_88, 
	chromium_linux_92, 
	firefox_linux_88 
] 
 
def random_headers(): 
	return random.choice(headers) 