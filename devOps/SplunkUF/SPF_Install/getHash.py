import requests
from bs4 import BeautifulSoup
import re

version = "6.6.3"
os = "linux"
arch = "amd64"
pkg = "deb"
url = f"https://www.splunk.com/en_us/download/previous-releases.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a", href=re.compile(f"splunk-{version}-.*-{os}.*{arch}\.{pkg}"))

for link in links:
    href = link["href"]
    match = re.search(r"splunk-\d+\.\d+\.\d+-([a-f0-9]+)-", href)
    if match:
        hash_value = match.group(1)
        print(f"Found hash: {hash_value}")
