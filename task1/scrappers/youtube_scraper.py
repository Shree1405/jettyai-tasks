from youtube_transcript_api import YouTubeTranscriptApi
import re
import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

def extract_video_id(url):
    patterns = [
        r"(?:v=|\/|embed\/|youtu\.be\/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def scrape_youtube(url):
    video_id = extract_video_id(url)
    if not video_id:
        return {"author": "Unknown", "published_date": "Unknown", "content_chunks": []}

    headers = {"User-Agent": ua.random}
    
    # Fetch page for metadata
    try:
        with httpx.Client(follow_redirects=True, headers=headers) as client:
            response = client.get(url)
            html = response.text
    except:
        html = ""

    soup = BeautifulSoup(html, "html.parser")
    
    # Robust metadata extraction
    channel = "Unknown"
    channel_tag = soup.find("link", itemprop="name") or soup.find("meta", property="og:site_name")
    if channel_tag:
        channel = channel_tag.get("content", "Unknown")
    
    description = ""
    desc_tag = soup.find("meta", attrs={"property": "og:description"}) or soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        description = desc_tag.get("content", "")

    # Fetch transcript
    chunks = []
    try:
        transcript_data = YouTubeTranscriptApi().fetch(video_id)
        full_text = [entry["text"] for entry in transcript_data]
        # Combine into chunks of ~5 lines each
        chunks = [" ".join(full_text[i:i+5]) for i in range(0, len(full_text), 5)]
    except Exception as e:
        # Fallback to description if no transcript
        if description:
            chunks = [description]

    return {
        "author": channel,
        "published_date": "YouTube Data API required for exact date",
        "content_chunks": chunks
    }