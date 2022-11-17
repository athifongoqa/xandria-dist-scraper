import repo
from collectors import headless_chromium
from headers import random_headers 
from proxies.proxies import random_proxies 
import logging
import json
import re
import requests
 
def extract_content(url, soup):
	# TO-DO: Error handling
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
		'rootSite': re.search("//(.+?)/", url).group(1),
		'author': author['name'],
	}
	
	logging.info(f'Resource returned: {resource}')


	return resource
 
def store_content(url, content): 
	# store in a hash with the URL as the key and the content object as the value
	# TO-DO: Error handling
	repo.set_content(url, content)
 
def allow_url_filter(url): 
	# allow all by default
	# validate URLs/Robots.txt
	# TO-DO: Error handling
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}

	r = requests.get('https://webris.org/robots.txt', 
	headers=headers, 
	proxies={
		'http' : '200.105.215.22:33630',
		'https': '200.105.215.22:33630'
		})

	x = re.findall("[A-Za-z0-9]+-[a-zA-Z]+: \*", r.text)
	if x: 
		return True

async def get_html(url):
	proxies = await random_proxies()
	logging.info(await random_proxies())
	# TO-DO: Error handling
	return await headless_chromium.get_html(url, headers=random_headers(), proxies=proxies)

def use_regex(input_text):
    pattern = re.compile(r"[A-Za-z0-9]+-\._~:/\?#.*@!\$&'.*\*\+.*=", re.IGNORECASE)
    return pattern.match(input_text)

