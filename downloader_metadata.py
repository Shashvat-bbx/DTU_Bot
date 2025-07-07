import os
import asyncio
import aiohttp
import aiofiles
import csv
import urllib.parse
from tqdm.asyncio import tqdm
from asyncio import Lock

# Load PDF links
with open("pdf_links.txt", "r") as f:
    pdf_links = [line.strip() for line in f if line.strip()]

# Create output directory
output_dir = "downloaded_pdfs_meta"
os.makedirs(output_dir, exist_ok=True)

# CSV path
csv_path = "downloaded_mapping.csv"

# Async CSV lock to prevent concurrent writes
csv_lock = Lock()

async def download_pdf(session, link, i, writer):
    path = urllib.parse.urlparse(link).path
    ext = os.path.splitext(path)[1] or ".pdf"
    filename = f"doc_{i}{ext}"
    save_path = os.path.join(output_dir, filename)

    if os.path.exists(save_path):
        async with csv_lock:
            writer.writerow([link, save_path])
        return

    try:
        async with session.get(link, timeout=500) as resp:
            if resp.status == 200:
                async with aiofiles.open(save_path, "wb") as f_out:
                    await f_out.write(await resp.read())
                async with csv_lock:
                    writer.writerow([link, save_path])
            else:
                print(f"[{i}] HTTP {resp.status} for {link}")
    except Exception as e:
        print(f"[{i}] Error downloading {link}: {e}")

async def main():
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Open CSV and prepare writer
        async with aiofiles.open(csv_path, "w", newline='', encoding="utf-8") as csvfile_async:
            # aiofiles doesn't support csv.writer, so we open a sync file in a separate thread-safe block
            with open(csv_path, "w", newline='', encoding="utf-8") as sync_csvfile:
                writer = csv.writer(sync_csvfile)
                writer.writerow(["web_url", "local_file_path"])  # Header row

                tasks = [
                    download_pdf(session, link, idx, writer)
                    for idx, link in enumerate(pdf_links, start=1)
                ]

                for task in tqdm.as_completed(tasks, total=len(tasks), desc="📥 Downloading PDFs"):
                    await task

if __name__ == "__main__":
    asyncio.run(main())
    print(f"\n✅ Downloads complete. Mapping saved to: {csv_path}")
