from bs4 import BeautifulSoup
import requests
import pprint

def scrape_witanime(url):
    # Headers for the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Make the request
    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)  # Print status code for debugging

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div elements with class "episodes-card-container"
    div_list = soup.find_all('div', class_='episodes-card-container')

    # Initialize a list to store dictionaries
    data_list = []

    # Extract data from each div
    for div in div_list:
        # Initialize a dictionary for each entry
        data = {}

        # Extract URL and episode from a tag inside div with class "episodes-card-title"
        title_div = div.find('div', class_='episodes-card-title')
        if title_div:
            a_tag = title_div.find('h3').find('a')
            if a_tag and 'href' in a_tag.attrs:
                data['url'] = a_tag['href']
                data['episode'] = a_tag.text.strip()  # Use .text to get text inside the <a> tag
            else:
                data['url'] = None
                data['episode'] = None

        # Extract image URL from img tag with class "img-responsive"
        img_tag = div.find('img', class_='img-responsive')
        if img_tag and 'src' in img_tag.attrs:
            data['img_url'] = img_tag['src']
        else:
            data['img_url'] = None

        # Extract title from div with class "ep-card-anime-title"
        title_card_div = div.find('div', class_='ep-card-anime-title')
        if title_card_div:
            h3_tag = title_card_div.find('h3')
            if h3_tag and h3_tag.a:
                data['title'] = h3_tag.a.text.strip()
            else:
                data['title'] = None
        else:
            data['title'] = None

        # Add the dictionary to the list if it has a URL
        if 'url' in data and data['url']:
            data_list.append(data)

    return data_list

# # Example usage
# if __name__ == "__main__":
#     url = "https://witanime.cyou"
#     data_list = scrape_witanime(url)
#     pprint.pprint(data_list)


# 6991610719:AAFe95FKTVzXKJIB8RDklWrlynIa-tkTQQA