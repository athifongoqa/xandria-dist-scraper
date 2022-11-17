import repo
from proxies.getProxies import getProxies, extract
import concurrent.futures

def free_proxies():
	repo.clear_proxies()
	proxylist = getProxies()

	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(extract, proxylist)

	return True