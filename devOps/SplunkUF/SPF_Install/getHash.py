import requests
import re
from collections import defaultdict

REPO = "splunk/splunk"
URL = f"https://hub.docker.com/v2/repositories/{REPO}/tags?page_size=100"

# Match tags like 9.4.2 (not 9.4 or latest)
version_re = re.compile(r'^\d+\.\d+\.\d+$')
hash_re = re.compile(r'^[a-f0-9]{12}$')

def fetch_all_tags():
    tags = []
    url = URL
    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        tags.extend(data["results"])
        url = data.get("next")
    return tags

def group_tags_by_digest(tags):
    digest_map = defaultdict(list)
    for tag in tags:
        name = tag["name"]
        images = tag.get("images", [])
        if images:
            digest = images[0].get("digest")
            if digest:
                digest_map[digest].append(name)
    return digest_map

def extract_version_hash_pairs(digest_map):
    pairs = []
    for tags in digest_map.values():
        versions = [t for t in tags if version_re.match(t)]
        hashes = [t for t in tags if hash_re.match(t)]
        for version in versions:
            for h in hashes:
                pairs.append((version, h))
    return pairs

def main():
    tags = fetch_all_tags()
    digest_map = group_tags_by_digest(tags)
    pairs = extract_version_hash_pairs(digest_map)

    print("version,hash")
    for version, h in sorted(pairs):
        print(f"{version},{h}")

if __name__ == "__main__":
    main()
