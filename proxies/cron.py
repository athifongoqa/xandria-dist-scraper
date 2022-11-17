import repo
import proxies.getProxies
import concurrent.futures

def free_proxies():
	repo.clear_proxies()
	proxylist = proxies.getProxies.getProxies()

	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(proxies.getProxies.extract, proxylist)

	return True