# 🚀 Challenge 1A – Structured PDF Processing

This repository contains the solution for **Challenge 1A** of the Adobe India Hackathon 2025.

The task: Convert unstructured PDF documents into meaningful JSON outputs by extracting titles and a hierarchical outline — all inside a Docker container with strict offline and performance constraints.

---

##  Approach

- **Title Extraction**:  
  Extracted from the **first page** using the **largest font** found in the top third of the page.

- **Outline Generation**:  
  Scanned the entire PDF and:
  - Detected all text spans with size info.
  - Ranked top 3 unique font sizes.
  - Assigned heading levels: **H1**, **H2**, **H3** using a heuristic.
  - Built a flattened outline (not nested, but labeled by level).

---

##  Libraries & Tools Used

| Tool / Library | Purpose                  |
|----------------|---------------------------|
| Python 3.10     | Main runtime              |
| [PyMuPDF (`fitz`)](https://pymupdf.readthedocs.io/) | PDF parsing and font/structure analysis |
| Docker (amd64) | Containerized execution   |

---

##  How to Build & Run (Docker)
1. Navigate to the directory

```
cd Challenge_1a
```
2. Build the Docker image
```
docker build --platform linux/amd64 -t challenge1a .
```
3. Run the container
- On Windows (PowerShell):
```
docker run --rm `
  -v "${PWD}\sample_dataset\pdfs:/app/input:ro" `
  -v "${PWD}\sample_dataset\outputs\challenge1a:/app/output" `
  --network none `
  challenge1a
```
- On Linux/macOS:
```
docker run --rm \
  -v "$(pwd)/sample_dataset/pdfs:/app/input:ro" \
  -v "$(pwd)/sample_dataset/outputs/challenge1a:/app/output" \
  --network none \
  challenge1a
```
Output
JSON files (named as <filename>.json) will be generated in:
```
sample_dataset/outputs/challenge1a/
```
Each JSON contains:
- title: Title extracted from the first page
- outline: A list of detected headings with page numbers and heading levels (H1, H2, H3)

📂 Folder Structure
```
Challenge_1a/
├── sample_dataset/
│   ├── pdfs/                      # Input PDFs
│   ├── outputs/
│   │   └── challenge1a/           # Generated output JSONs
│   └── schema/
│       └── output_schema.json     # Required JSON schema
├── process_pdfs.py                # Main processing script
├── Dockerfile                     # Docker configuration
└── README.md                      # You're here
```
Constraints Met:
- Offline-only (no network access)
- Runs under 10 seconds for 50-page PDF
- CPU-only (no GPU) and tested with 8 vCPUs / 16 GB RAM
- Works fully inside Docker (amd64)
- Output conforms to provided JSON schema

Validation Checklist:
-  ✅All PDFs in /app/input are scanned
-  ✅Output JSONs match schema
-  ✅ No internet required during execution
-  ✅ Memory and CPU constraints satisfied
-  ✅ Works on both simple and complex PDFs

⚠️ Note
This is a basic functional solution. Future enhancements could include:
- Nested outline generation
- Style-aware content extraction
- Multi-language support
- Better heuristics for heading hierarchy

>Built for Adobe India Hackathon 2025 – “Connecting the Dots” Challenge
