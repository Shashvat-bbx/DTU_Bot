# DTU_Bot

DTU_Bot is a pipeline for scraping, downloading, parsing, and intelligent querying of official PDF notices, syllabi, and documents from [Delhi Technological University (DTU)](https://www.dtu.ac.in/). It leverages modern Python tools for web scraping, PDF processing, OCR extraction, vector storage, and retrieval-augmented generation (RAG) with LLMs, enabling users to ask natural-language questions about DTU documents and get context-rich, cited answers.

---

## Features

- **Automated Scraping:** Extracts all PDF links from DTU’s official notices and web pages.
- **Bulk Download:** Downloads hundreds of PDFs asynchronously and maps web URLs to local files.
- **OCR & Parsing:** Extracts and processes text from PDFs (including scanned images).
- **Metadata Mapping:** Maintains a CSV mapping of source links to downloaded files.
- **Vector Store:** Embeds and indexes documents for fast semantic search using FAISS and HuggingFace embeddings.
- **Conversational RAG QA:** Enables users to query the database with natural language, returning answers with inline citations.
- **Modular Design:** Each stage (scraping, downloading, OCR, vector store, QA) is a separate, reusable script.

---

## Pipeline Overview

1. **Scraper & Parser** (`Scraper_parser.py`)
   - Scrapes PDF links from DTU web pages using BeautifulSoup.
   - Outputs to `pdf_links.txt`.

2. **Downloader & Metadata** (`downloader_metadata.py`)
   - Asynchronously downloads all PDFs from `pdf_links.txt`.
   - Stores them in `downloaded_pdfs_meta/`.
   - Saves a mapping (`downloaded_mapping.csv`) of web URLs to local file paths.

3. **OCR & Text Extraction** (`dotr_model.py`)
   - Uses [doctr](https://github.com/mindee/doctr) (PyTorch backend) for OCR on PDFs.
   - Reads local PDFs, extracts text, and outputs structured data to `output.csv`.

4. **Vector Store & Embedding** (`Rag_vector_store.py`)
   - Embeds extracted text using HuggingFace or OpenAI embeddings.
   - Stores all chunks in a FAISS vector store for efficient retrieval.

5. **Conversational QA (RAG)**
   - Uses LangChain and OpenAI LLMs (or compatible models).
   - Accepts user queries, retrieves relevant document chunks, and generates context-rich, cited answers.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shashvat-bbx/DTU_Bot.git
   cd DTU_Bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   - Make sure you have `poppler` or similar system dependencies for PDF parsing.
   - For OCR, PyTorch is required. Install with:  
     `pip install torch torchvision torchaudio`
   - The doctr model is installed via:
     ```
     pip install python-doctr[torch,viz]@git+https://github.com/mindee/doctr.git
     ```

3. **Set up environment variables:**
   - Create a `.env` file for API keys, e.g., for OpenAI or HuggingFace.

---

## Usage

### 1. Scrape PDF Links

```bash
python Scraper_parser.py
```
- Outputs: `pdf_links.txt` with all found PDF URLs.

### 2. Download PDFs and Map Metadata

```bash
python downloader_metadata.py
```
- Outputs: downloads files to `downloaded_pdfs_meta/` and creates `downloaded_mapping.csv`.

### 3. OCR PDFs to Extract Text

```bash
python dotr_model.py
```
- Outputs: `output.csv` with extracted text and references.

### 4. Build Vector Store and Enable QA

Edit `Rag_vector_store.py` to set your API keys and paths as needed.

```bash
python Rag_vector_store.py
```
- Interactive code lets you run queries like:
  ```python
  final = ask_rag("find me details for BTech academic calendar 2025")
  print(final)
  ```

---

## Requirements

See `requirements.txt` for details:

- selenium, bs4, requests, aiohttp, aiofiles
- faiss-cpu, langchain, langchain-huggingface, langchain-community, langchain_core
- doctr (from Mindee, with PyTorch + viz)
- huggingface, sentence-transformers, streamlit, dotenv

---

## File Structure

```
DTU_Bot/
│
├── Scraper_parser.py          # Scrapes PDF links from DTU website
├── downloader_metadata.py     # Downloads PDFs and maps URLs to files
├── dotr_model.py              # Performs OCR on PDFs, outputs extracted text
├── Rag_vector_store.py        # Embeds text, stores vectors, enables QA
│
├── data_files/
│   └── pdf_links.txt          # List of scraped PDF URLs
│
├── downloaded_pdfs_meta/      # Downloaded PDFs
├── downloaded_mapping.csv     # Mapping of URLs to local files
├── output.csv                 # OCR-extracted text and metadata
│
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (API keys, etc.)
```

---

## Example: End-to-End Run

1. Scrape PDF links:
   ```
   python Scraper_parser.py
   ```
2. Download PDFs:
   ```
   python downloader_metadata.py
   ```
3. OCR and extract text:
   ```
   python dotr_model.py
   ```
4. Build vector store and ask a question:
   ```
   python Rag_vector_store.py
   # Then in code: ask_rag("What are the latest DTU academic notices?")
   ```

---

## Notes & Tips

- Some PDFs may be image-based and require OCR. The pipeline handles both text and image PDFs.
- The vector store directory and embedding model can be configured in `Rag_vector_store.py`.
- For best results with LLMs, use an API key with sufficient quota (OpenAI, etc.).
- The code is modular and can be adapted for other universities or websites with minor changes.

---

## License

MIT License

---

## Contributors

- [Shashvat-bbx](https://github.com/Shashvat-bbx)

---

## Acknowledgements

- [DTU Official Website](https://www.dtu.ac.in/)
- [Mindee Doctr](https://github.com/mindee/doctr)
- [LangChain](https://github.com/langchain-ai/langchain)
- [FAISS](https://github.com/facebookresearch/faiss)
