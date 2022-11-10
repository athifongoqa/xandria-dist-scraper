import random 
 
free_proxies = [ 
	{'server': 'https://138.19.29.147:80', 'server': 'http://213.241.205.2:8080'} 
] 
 
proxies = { 
	'free': free_proxies, 
} 
 
def random_proxies(type='free'): 
	return random.choice(proxies[type]) 