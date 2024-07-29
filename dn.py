import requests
import re
import json
import base64

def get_decoded_urls(page_url):
    # Define headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://witanime.cyou/',
        'Upgrade-Insecure-Requests': '1'
    }

    # Send an HTTP request to the URL
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Extract the page content
    html_content = response.text

    # Regex pattern to find JavaScript variable declarations
    js_var_pattern = r"(?:var|let|const)\s+(\w+)\s*=\s*({.*?});"

    # Find all matches
    matches = re.findall(js_var_pattern, html_content, re.DOTALL)

    # Find and process the `downloadUrls` variable
    download_urls = None
    for variable, value in matches:
        if "downloadUrls" in variable:
            download_urls = value.strip()
        
        
        # break

    if download_urls:
        # Parse the JSON text
        try:
            data = json.loads(download_urls)
            decoded_urls = []

            # Decode base64 encoded URLs
            for encoded_url in data.values():
                try:
                    decoded_url = base64.b64decode(encoded_url).decode('utf-8')
                    decoded_url = decoded_url.split("|")[0]
                    decoded_urls.append(decoded_url)
                except (base64.binascii.Error, UnicodeDecodeError) as e:
                    print(f"Error decoding URL: {e}")

            return decoded_urls

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []

    else:
        print("Variable containing 'downloadUrls' not found in the page.")
        return []
    

def get_video_urls(page_url):
    # Define headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://witanime.cyou/',
        'Upgrade-Insecure-Requests': '1'
    }

    # Send an HTTP request to the URL
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Extract the page content
    html_content = response.text

    # Regex pattern to find JavaScript variable declarations
    js_var_pattern = r"(?:var|let|const)\s+(\w+)\s*=\s*({.*?});"

    # Find all matches
    matches = re.findall(js_var_pattern, html_content, re.DOTALL)

    # Find and process the `downloadUrls` variable
    download_urls = None
    for variable, value in matches:
        if "serverUrls" in variable:
            download_urls = value.strip()
        
        
        # break

    if download_urls:
        # Parse the JSON text
        try:
            data = json.loads(download_urls)
            decoded_urls = []

            # Decode base64 encoded URLs
            for encoded_url in data.values():
                try:
                    decoded_url = base64.b64decode(encoded_url).decode('utf-8')
                    decoded_url = decoded_url
                    apiKey = "97c2f6cd-5143-4e42-93d8-b239b7c781be"

                    if test_url(decoded_url):
                        decoded_url += "&apikey="+apiKey
                        print(decoded_url)
                        decoded_urls.append(decoded_url)
                    else:
                        print("Not passed patern")
                except (base64.binascii.Error, UnicodeDecodeError) as e:
                    print(f"Error decoding URL: {e}")

            return decoded_urls

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []

    else:
        print("Variable containing 'downloadUrls' not found in the page.")
        return []
    
def test_url(decoded_url):
    # Compile the regular expression pattern
    pattern = r'^https://yonaplay\.org/embed\.php\?id=\d+$'
    regex = re.compile(pattern)
    
    # Test the URL against the pattern
    if regex.fullmatch(decoded_url):
        return True
    else:
        return False

# Example usage
url = 'https://witanime.cyou/episode/garouden-the-way-of-the-lone-wolf-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-2/'
decoded_urls = get_video_urls(url)
print("Decoded URLs:")
for url in decoded_urls:
   print(url)


# serverUrls_rJpvULGL