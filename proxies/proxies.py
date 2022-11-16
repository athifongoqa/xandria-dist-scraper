import random
from repo import get_valid_proxies_list
import repo
import proxies.getProxies
import concurrent.futures

def free_proxies():
	repo.clear_proxies()
	proxylist = proxies.getProxies.getProxies()

	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(proxies.getProxies.extract, proxylist)

	free_proxies = get_valid_proxies_list()
	print(free_proxies)
	free = { 
	'free': free_proxies,
	} 
	return free

 
async def random_proxies(type='free'): 
	proxies = free_proxies()
	choice = random.choice(proxies[type]) 
	print(choice)
	return choice