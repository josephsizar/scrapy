import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://witanime.cyou/',
    'Upgrade-Insecure-Requests': '1'
}

def get_video_url(page_url):
    # Send a request to the MP4Upload page
    response = requests.get(page_url,headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the video URL in the HTML content
    video_url_pattern = re.compile(r'(https?://.*?\.mp4)')
    video_url = video_url_pattern.search(soup.prettify())

    if video_url:
        return video_url.group(0)
    else:
        print("Video URL not found")
        return None


def download_video(video_url, output_filename):
    # Send a request to download the video
    response = requests.get(video_url, stream=True)
    response.raise_for_status()  # Check if the request was successful

    # Write the video content to a file
    with open(output_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Video downloaded successfully as {output_filename}")


# Example usage
page_url = 'https://www.mp4upload.com/dkbol9dnwqyq'  # Replace with your video page URL
output_filename = 'video.mp4'

video_url = get_video_url(page_url)
if video_url:
    download_video(video_url, output_filename)
