import requests
from bs4 import BeautifulSoup
import re
import tldextract
from urllib.parse import urljoin, urlparse
import sys
import csv
import time
import os

EXCLUDE_PATTERNS = ["blog", "article", "news", ".pdf", "how-to", "top-10"]
RESULTS_FILE = "results.csv"

def fetch_sitemap(url):
    sitemap_url = urljoin(url, "/sitemap.xml")
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[!] No sitemap found at {sitemap_url}")
            return None
    except Exception as e:
        print(f"[!] Error fetching sitemap: {e}")
        return None

def parse_sitemap(xml):
    soup = BeautifulSoup(xml, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    return urls

def is_valid_url(url, base_domain):
    parsed = tldextract.extract(url)
    domain = f"{parsed.domain}.{parsed.suffix}"
    if domain != base_domain:
        return False

    # Count path segments between slashes
    parsed_url = urlparse(url)
    path_segments = [seg for seg in parsed_url.path.split('/') if seg]
    return len("/".join(path_segments)) < 15

def should_skip(url):
    return any(keyword in url.lower() for keyword in EXCLUDE_PATTERNS)

def extract_contacts(html):
    emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', html))
    phones = set(re.findall(r'\+?\d[\d\s\-\.\(\)]{7,}\d', html))
    return list(emails), list(phones)

def scrape_page(url):
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            emails, phones = extract_contacts(res.text)
            return emails, phones, res.text
    except Exception as e:
        print(f"[!] Failed to scrape {url}: {e}")
    return [], [], ""

def extract_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        links.add(full_url)
    return links

def save_result(row):
    file_exists = os.path.isfile(RESULTS_FILE)
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "emails", "phones"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def crawl_site(base_url, base_domain):
    to_visit = set([base_url])
    visited = set()

    while to_visit:
        url = to_visit.pop()
        if url in visited or should_skip(url) or not is_valid_url(url, base_domain):
            continue

        print(f"[*] Crawling: {url}")
        visited.add(url)
        emails, phones, html = scrape_page(url)

        if emails or phones:
            row = {"url": url, "emails": ", ".join(emails), "phones": ", ".join(phones)}
            save_result(row)

        new_links = extract_links(url, html)
        to_visit.update(new_links - visited)

        time.sleep(1)  # Be nice to servers

def main(base_url):
    parsed_base = tldextract.extract(base_url)
    base_domain = f"{parsed_base.domain}.{parsed_base.suffix}"
    sitemap = fetch_sitemap(base_url)

    if sitemap:
        urls = parse_sitemap(sitemap)
        for url in urls:
            if not is_valid_url(url, base_domain) or should_skip(url):
                continue
            print(f"[*] Scraping: {url}")
            emails, phones, _ = scrape_page(url)
            if emails or phones:
                row = {"url": url, "emails": ", ".join(emails), "phones": ", ".join(phones)}
                save_result(row)
            time.sleep(1)
    else:
        print("[!] No sitemap found, falling back to crawling.")
        crawl_site(base_url, base_domain)

    print("\n[✓] Scraping complete. Results saved to results.csv")

if __name__ == "__main__":
    url = input("enter your url : ")
    main(url)
