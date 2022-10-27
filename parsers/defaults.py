import repo 
import requests
 
def extract_content(url, soup): 
	return soup.title.string # extract page's title 
 
def store_content(url, content): 
	# store in a hash with the URL as the key and the title as the content 
	repo.set_content(url, content) 
 
def allow_url_filter(url): 
	return True # allow all by default 
 
def get_html(url): 
	try: 
		response = requests.get(url) 
		return response.content 
	except Exception as e: 
		print(e) 
 
	return '' 