import repo
from collectors import headless_chromium
from headers import random_headers 
from proxies import random_proxies 
import logging
import json
import re
 
def extract_content(url, soup):
	logging.info('Extraction begun.')
	
	data = [json.loads(x.string) for x in soup.find_all("script", type="application/ld+json")]
	logging.info(f'Data: {data[0]}')

	headline = data[0]['headline']
	# meta name=description
	description = 'Needs updating.'
	url = data[0]['url']
	imageURL = data[0]['image']
	author = data[0]['author']
	createdAt = data[0]['datePublished']
	updatedAt = data[0]['dateModified']

	resource = {
		'headline': headline,
		'description': description,
		'url': url,
		'imageURL': imageURL,
		'protocol': re.search("^(.+?)://", url).group(1),
		'rootSite': re.search("//(.+?)/", url).group(1),
		'author': author,
		'createdAt': createdAt,
		'updatedAt': updatedAt
	}
	
	logging.info(f'Resource returned: {resource}')


	return resource
 
def store_content(url, content): 
	# store in a hash with the URL as the key and the content object as the value
	repo.set_content(url, content)
 
def allow_url_filter(url): 
	# allow all by default
	# validate URLs
	return True 

async def get_html(url):
	logging.info(random_proxies())
	return await headless_chromium.get_html(url, headers=random_headers(), proxies=random_proxies())