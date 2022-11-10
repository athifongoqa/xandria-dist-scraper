from urllib.parse import urlparse 
from parsers import defaults
import logging
 
parsers = { 
	'scrapeme.live': defaults, 
	'quotes.toscrape.com': defaults, 
} 
 
def get_parser(url): 
	logging.info('Get parser reached.')
	hostname = urlparse(url).hostname # extract domain from URL 
	if hostname in parsers: 
		# use the dict above to return the custom parser if present 
		logging.info(f'{parsers[hostname]}')
		return parsers[hostname] 
	return defaults