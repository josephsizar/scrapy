

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://witanime.cyou/',
    'Upgrade-Insecure-Requests': '1'
}

def get_video_download_url(page_url):
    """
    Scrape the Gofile.io page to extract the video download URL.
    
    :param page_url: URL of the Gofile.io file page
    :return: Direct download URL of the video
    """
    response = requests.get(page_url,headers=headers)
    response.raise_for_status()  # Check if the request was successful

    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)

    # Find the div with class 'plyr__video-wrapper'
    video_wrapper = soup.find('div', class_='plyr__video-wrapper')
    if not video_wrapper:
        raise Exception("Video wrapper div not found")

    # Find the video tag within the div
    video_tag = video_wrapper.find('video')
    if not video_tag:
        raise Exception("Video tag not found")

    # Find the source tag within the video tag
    source_tag = video_tag.find('source')
    if not source_tag:
        raise Exception("Source tag not found")

    # Extract the src attribute from the source tag
    download_url = source_tag.get('src')
    if not download_url:
        raise Exception("Download URL not found")

    return download_url

def download_video(download_url, output_filename):
    """
    Download a video from the given URL and save it to the specified filename.
    
    :param download_url: Direct URL to the video file
    :param output_filename: Path to save the downloaded video file
    """
    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    
    with open(output_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    print(f"Video downloaded successfully: {output_filename}")

# Example usage
page_url = 'https://gofile.io/d/rMioG0'  # URL of the Gofile.io file page
output_filename = 'downloaded_video.mp4'  # Desired output file name

try:
    video_url = get_video_download_url(page_url)
    download_video(video_url, output_filename)
except Exception as e:
    print(f"An error occurred: {e}")
