# 🕵️‍♂️ Contact Info Web Scraper

This Python tool extracts **emails** and **phone numbers** from any website. It first tries to use the `sitemap.xml` to efficiently gather all internal pages. If the sitemap is missing, it falls back to crawling the site by exploring all reachable internal links — while smartly skipping blog-style content like "how-to" or "top-10" pages.

---

## 🚀 Features

- 📬 Extracts Emails
- 📱 Extracts Phone Numbers
- 🗺️ Parses Sitemap Automatically
- 🔄 Falls back to crawling when sitemap is missing
- 🧠 Skips irrelevant paths (e.g. blog, articles, how-to)
- 💾 Saves results instantly to `results.csv`
- 🧹 Avoids re-visiting the same URL

---

## 🔧 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage

```bash
python scraper.py https://example.com
```

After running, results will be available in:

```
results.csv
```

---

## 🧠 Tech Stack

- Python
- BeautifulSoup
- Requests
- Regex
- TLDExtract
- CSV

---

## 📁 Output Example

| URL                          | Emails                | Phones            |
|-----------------------------|------------------------|--------------------|
| https://example.com/contact | info@example.com       | +1 234-567-8901    |

---

## ⚠️ Disclaimer

Use this script responsibly. Always respect robots.txt and terms of service of the websites you scrape.

---

## 📬 Contact

For questions or collaboration, feel free to reach out!