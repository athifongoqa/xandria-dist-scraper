from playwright.async_api import async_playwright

import logging

async def get_html(url, headers=None, proxies=None):
    # TO-DO: Error handling
    logging.info('Headless Chromium running.')
    html = ''
    async with async_playwright() as p:
        print(f'proxies: {proxies}')

        proxy = str(proxies)
        print(type(proxy))

        browser_type = p.chromium
        browser = await browser_type.launch(proxy={'server': proxy})
        logging.info(f'Browser used: {browser} - for url:{url}')

        page = await browser.new_page()
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
