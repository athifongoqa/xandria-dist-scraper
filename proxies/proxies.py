import random
from repo import get_valid_proxies_list
import repo
import proxies.getProxies
import concurrent.futures
import schedule
import time

def free_proxies():
	repo.clear_proxies()
	proxylist = proxies.getProxies.getProxies()

	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(proxies.getProxies.extract, proxylist)

	return True

schedule.every(5).minutes.do(free_proxies)
 
async def random_proxies(type='free'):
	free_proxies = get_valid_proxies_list()

	free = { 
	'free': free_proxies,
	} 

	choice = random.choice(free[type]) 
	print(f'Choice: {choice}')
	return choice