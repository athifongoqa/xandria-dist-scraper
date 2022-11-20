import random
from repo import get_valid_proxies_list
 
async def random_proxies(type='free'):
	free_proxies = get_valid_proxies_list()

	print(free_proxies)

	free = { 
	'free': free_proxies,
	} 

	choice = random.choice(free[type]) 
	print(f'Choice: {choice}')
	return choice