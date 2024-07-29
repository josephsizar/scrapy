import requests
from bs4 import BeautifulSoup
import base64

# URL of the page you want to scrape
url = 'https://witanime.cyou/episode/garouden-the-way-of-the-lone-wolf-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-2/'

# Define custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Send an HTTP request to the URL with custom headers
response = requests.get(url, headers=headers)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all elements with class 'download-link'
download_links = soup.find_all(class_='btn btn-default download-link')

# Dictionary to store the extracted URLs
download_urls = {}

for link in download_links:
    print(link)
    data_key = link.get('data-key')
    # print(data_key)
    encoded_url = link.get('data-url')
    # print(encoded_url)
    
    if data_key and encoded_url:
        try:
            # Decode the base64-encoded URL
            decoded_url = base64.b64decode(encoded_url).decode('utf-8').split('|')[0]
            print(decoded_url)
            download_urls[data_key] = decoded_url
        except (TypeError, ValueError) as e:
            print(f"Error decoding URL for key {data_key}: {e}")

scripts = soup.find_all('script')
for script in scripts:
    if 'dynamicVarName' in script.text:
        print(script.text)

# Print or use the extracted URLs
for key, url in download_urls.items():
    print(f"Key: {key}, URL: {url}")
