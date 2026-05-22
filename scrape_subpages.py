import urllib.request
import re
from urllib.parse import urljoin, urlparse

urls = [
    "https://khoahocai.com.vn/tin-tuc/",
    "https://khoahocai.com.vn/kien-thuc/"
]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

all_links = set()

for url in urls:
    print(f"Fetching {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        print("Page fetched successfully. Length:", len(html))
        
        # Simple regex to extract hrefs
        hrefs = re.findall(r'href=["\'](https?://[^"\']+|/[^"\']*)["\']', html)
        
        for href in hrefs:
            full_url = urljoin(url, href)
            parsed = urlparse(full_url)
            if parsed.netloc == "khoahocai.com.vn":
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                all_links.add(clean_url)
                
    except Exception as e:
        print("Error fetching", url, ":", e)

print(f"\nFound {len(all_links)} total internal links:")
for link in sorted(all_links):
    if not any(x in link for x in ['wp-content', 'wp-json', 'xmlrpc', 'chinh-sach-bao-mat', 'gioi-thieu', 'lien-he', 'wp-includes']):
        print("-", link)
