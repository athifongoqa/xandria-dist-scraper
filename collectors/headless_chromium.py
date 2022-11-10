from playwright.async_api import async_playwright

import logging

async def get_html(url, headers=None, proxies=None, timeout=10000):
    logging.info('Headless Chromium running.')
    html = ''
    async with async_playwright() as p:
        logging.info(proxies)

        browser_type = p.chromium
        browser = await browser_type.launch()
        print(browser)
        page = await browser.new_page()
        # await page.set_extra_http_headers(headers)
        page.set_default_timeout(0)
        await page.goto(url)
        # await page.wait_for_timeout(timeout)

        html = await page.content()
        if html:
            logging.info('html received')
            await browser.close()
            return html

        return logging.info('Headless Chromium: Problem returning html')
