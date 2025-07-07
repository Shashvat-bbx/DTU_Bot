from bs4 import BeautifulSoup
from urllib.parse import urljoin

html_file_path = "notices.html"
base_url = "https://www.dtu.ac.in/"

with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

# Extract .pdf links and prepend base URL only if needed
pdf_links = []
for a in soup.find_all('a', href=True):
    href = a['href'].strip()
    if href.lower().endswith('.pdf'):
        # Use urljoin to correctly handle relative and absolute URLs
        full_url = href if href.startswith("http") else urljoin(base_url, href)
        pdf_links.append(full_url)

# Save to file
with open("pdf_links.txt", "w") as f:
    for link in pdf_links:
        f.write(link + "\n")

print(f"✅ Saved {len(pdf_links)} PDF links to pdf_links.txt")
