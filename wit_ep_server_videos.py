from playwright.async_api import async_playwright
import base64


async def get_urls_from_witanime_episode_page(page_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(page_url, wait_until='networkidle')
        await page.wait_for_selector('#episode-servers')

        # Extract data-url attributes
        data_urls = await page.evaluate('''() => {
            const items = document.querySelectorAll('#episode-servers li a');
            return Array.from(items).map(item => item.getAttribute('data-url'));
        }''')

        # Process each URL
        processed_urls = []
        for encoded_url in data_urls:
            decoded_url = base64.b64decode(encoded_url).decode('utf-8')
            if decoded_url.startswith('//'):
                processed_urls.append(f'https:{decoded_url}')
            elif not decoded_url.startswith('https://'):
                processed_urls.append(f'https://{decoded_url}')
            else:
                processed_urls.append(decoded_url)

        await browser.close()
        return processed_urls


