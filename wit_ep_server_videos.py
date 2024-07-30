import asyncio
from pyppeteer import launch
import base64

async def get_urls_from_witanime_episode_page(page_url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(page_url, {'waitUntil': 'networkidle2'})

    # Wait for the #episode-servers element to load
    await page.waitForSelector('#episode-servers')

    # Extract the data-url attributes from <a> tags inside <li> elements within the <ul> with id="episode-servers"
    data_urls = await page.evaluate('''() => {
        const items = document.querySelectorAll('#episode-servers li a')
        return Array.from(items).map(item => item.getAttribute('data-url'))
    }''')

    # Process each link
    processed_urls = []
    for encoded_url in data_urls:
        # Decode the URL
        decoded_url = base64.b64decode(encoded_url).decode('utf-8')
        
        # Ensure the URL starts with 'https:'
        if decoded_url.startswith('//'):
            # Convert protocol-relative URLs to 'https:'
            processed_urls.append(f'https:{decoded_url}')
        elif not decoded_url.startswith('https://'):
            # If the URL does not start with 'https:', prepend 'https://'
            processed_urls.append(f'https://{decoded_url}')
        else:
            processed_urls.append(decoded_url)

    await browser.close()
    return processed_urls

# Example usage
async def main():
    page_url = 'https://witanime.cyou/episode/isekai-yururi-kikou-kosodateshinagara-boukensha-shimasu-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-5/'
    processed_urls = await get_urls_from_witanime_episode_page(page_url)
    print('Processed URLs:', processed_urls)

asyncio.get_event_loop().run_until_complete(main())
