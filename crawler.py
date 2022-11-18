from bs4 import BeautifulSoup
from urllib.parse import urljoin
import repo
import logging

async def crawl(url, get_html, extract_content):
    # TO-DO: Error handling
    if not url:
        logging.info('URL not provided', url)
        return 'URL not provided'
        
    repo.add_to_queue(url)

    content = await _crawl(url, get_html, extract_content)

    repo.move_from_queued_to_visited(url)

    logging.info(f"Content extracted in main crawl: {content}")

    return content

def add_results_to_queue(urls, allow_url_filter):
    # TO-DO: Error handling
    if not urls:
        return

    for url in urls:
        if allow_url_filter(url):
            print('Add URL to visit queue', url)
            repo.add_to_visit(url)

async def _crawl(url, get_html, extract_content):
    # TO-DO: Error handling
    print('Crawl ->', url)

    html = await get_html(url)
    logging.info("Html returned.")
    soup = BeautifulSoup(html, 'html.parser')
    logging.info(f'Soup returned.')

    # links = _extract_links(url, soup)
    content = extract_content(url, soup)

    logging.info(f"Content extracted in _crawl: {content}")

    return content

def _extract_links(url, soup):
    # TO-DO: Error handling
    return list({
        urljoin(url, a.get('href'))
        for a in soup.find_all('a')
        if a.get('href') and not(a.get('rel') and 'nofollow' in a.get('rel'))
    })

def _seen(url):
    # TO-DO: Error handling
    return repo.is_visited(url) or repo.is_queued(url)