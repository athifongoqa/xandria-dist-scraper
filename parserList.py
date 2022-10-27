from urllib.parse import urlparse 
from parsers import defaults 
 
parsers = { 
	'scrapeme.live': defaults, 
	'quotes.toscrape.com': defaults, 
} 
 
def get_parser(url): 
	hostname = urlparse(url).hostname # extract domain from URL 
	if hostname in parsers: 
		# use the dict above to return the custom parser if present 
		return parsers[hostname] 
	return defaults