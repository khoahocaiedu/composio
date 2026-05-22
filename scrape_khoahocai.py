import urllib.request
import re
from urllib.parse import urljoin, urlparse

url = "https://khoahocai.com.vn/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Fetching {url}...")
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8', errors='ignore')
        
    print("Page fetched successfully. Length:", len(html))
    
    # Simple regex to extract hrefs
    hrefs = re.findall(r'href=["\'](https?://[^"\']+|/[^"\']*)["\']', html)
    
    internal_links = set()
    for href in hrefs:
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)
        if parsed.netloc == "khoahocai.com.vn":
            # Strip query params and hash fragment
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            internal_links.add(clean_url)
            
    print(f"\nFound {len(internal_links)} internal links:")
    for link in sorted(internal_links):
        print("-", link)
        
except Exception as e:
    print("Error:", e)
