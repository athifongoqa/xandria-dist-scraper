import repo
from collectors import headless_chromium
from headers import random_headers 
from proxies.proxies import random_proxies 
import logging
import json
import re
import requests
import yake

def extract_content(url, soup):
	# TO-DO: Error handling
	logging.info('Extraction begun.')
	
	data = [json.loads(x.string) for x in soup.find_all("script", type="application/ld+json")]
	print(f'Data: {data[0]}')

	try:
		headline = data[0]['name']
	except:
		headline = 'Not found.'

	try: 
		description = data[0]['headline']
		cleaned = []
		kw_extractor = yake.KeywordExtractor()
		keywords = kw_extractor.extract_keywords(description)

		for kw in keywords:
			item = list(kw)

			if ' ' not in item[0]: 
				cleaned.append(item[0])

		tagSet = set(cleaned)	
		tags = list(tagSet)
	except:
		description = 'Not found.'
		tags = ['Null']

	try: 
		url = data[0]['url']
		rootSite = re.search("//(.+?)/", url).group(1)
		if '.' in rootSite:
			tagRootSite = rootSite.split('.')
			tags.append(tagRootSite[1])
		else:
			tags.append(rootSite)
	except:
		url = 'Not found.'
		rootSite = 'Not found.'

	try: 
		imageURL = data[0]['image']
	except:
		imageURL = 'Not found.'

	try: 
		author = data[0]['author']['name']
	except:
		author = 'Not found.'

	resource = {
		'headline': headline,
		'description': description,
		'url': url,
		'imageURL': imageURL,
		'rootSite': rootSite,
		'author': author,
		'tags': tags
	}
	
	logging.info(f'Resource returned: {resource}')

	return resource
 
def store_content(url, content):
	# store in a hash with the URL as the key and the content object as the value
	# TO-DO: Error handling
	repo.set_content(url, content)
 
def allow_url_filter(url): 
	# TO-DO: Error handling
	robotstxt(url)
	safe_chars(url)
	
# @retry()
async def get_html(url):
	try:
		# proxies = await random_proxies()
		# logging.info(await random_proxies())
		# TO-DO: Error handling
		return await headless_chromium.get_html(url, headers=random_headers())
	except Exception as error:
		print(error)
		raise

def safe_chars(url):
    pattern = re.compile(r"[A-Za-z0-9]+-\._~:/\?#.*@!\$&'.*\*\+.*=", re.IGNORECASE)
    return pattern.match(url)

async def robotstxt(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}

	r = requests.get('https://webris.org/robots.txt', 
	headers=headers, 
	proxies=await random_proxies())

	x = re.findall("[A-Za-z0-9]+-[a-zA-Z]+: \*", r.text)
	if x: 
		return True

