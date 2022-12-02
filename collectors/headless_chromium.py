from playwright.async_api import async_playwright
from proxies.proxies import random_proxies 
import logging

async def get_html(url, headers=None):
    # TO-DO: Error handling
    logging.info('Headless Chromium running.')
    html = ''
    proxies = await random_proxies()
    async with async_playwright() as p:
        print(f'proxies: {proxies}')

        proxy = str(proxies)
        print(type(proxy))

        try: 
            browser_type = p.chromium
            browser = await browser_type.launch()
            logging.info(f'Browser used: {browser} - for url:{url}')

            ctx = await browser.new_context(accept_downloads=False)

            page = await ctx.new_page()
            logging.info(f'Empty New Page: {page}')

            await page.set_extra_http_headers(headers)
            logging.info(f'Headers set for: {url}')

            page.set_default_timeout(0)
            await page.goto(url)
            logging.info(f'Gone to URL: {url}')

            html = await page.content()
            if html:
                logging.info('HTML received')
                await browser.close()
                return html

            return logging.info('Headless Chromium: Problem returning html')
        except Exception as error:
            print(error)
            raise
