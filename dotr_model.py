# !pip install python-doctr[torch,viz]
# !pip uninstall -y tensorflow
# !pip install python-doctr[torch,viz]@git+https://github.com/mindee/doctr.git

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from tqdm import tqdm
import csv
import os
import time
import csv
import sys

csv.field_size_limit(sys.maxsize)

# Parameters
max_rows = 700
input_csv_path = "downloaded_mapping.csv"
output_csv_path = "output.csv"

# OCR Function
def get_ocr(file_path):
    doc = DocumentFile.from_pdf(file_path)
    print(f"📄 Number of pages: {len(doc)} in {file_path}")

    predictor = ocr_predictor(pretrained=True)
    result = predictor(doc)

    string_result = result.render()
    print(f"✅ OCR Result for {file_path}:\n")
    # if len(doc)>=1:
    #     time.sleep(7)
    if len(doc)>5:
        time.sleep(10)
    if len(doc)>15:
        time.sleep(5)
    if len(doc)>25:
        time.sleep(5)
    return string_result

# Load already processed references if output file exists
processed_refs = set()
if os.path.exists(output_csv_path):
    with open(output_csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                processed_refs.add(row[1])  # original_reference
for i in processed_refs:
    print("already processed: ", i)
# Read input
with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile, \
     open(output_csv_path, 'a', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Only write header if file is empty
    if os.stat(output_csv_path).st_size == 0:
        writer.writerow(["extracted_text", "original_reference"])

    next(reader)  # Skip header row

    pending_rows = []
    for row in reader:
        if len(row) < 2:
            continue
        if row[0] in processed_refs:
            print("already done, skipping:", row[0])
            continue
        pending_rows.append(row)
        if len(pending_rows) >= max_rows:
            break

    for row in tqdm(pending_rows, desc="🔍 Processing PDFs"):
        
        try:
            extracted_text = get_ocr(row[1])
            writer.writerow([extracted_text, row[0]])
        except Exception as e:
            print(f"❌ Error processing {row[1]}: {e}")

print(f"\n✅ Finished extracting OCR text for {len(pending_rows)} new files. Results saved to {output_csv_path}")
