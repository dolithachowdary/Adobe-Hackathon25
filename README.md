# Adobe India Hackathon 2025

## 🚀 Connecting the Dots Challenge

> Rethink Reading. Rediscover Knowledge.

In a world flooded with documents, what wins is not more content — it's context. This challenge reimagines the humble PDF as an intelligent, interactive experience. You are tasked with making PDFs understand structure, surface insights, and respond like a smart research assistant.

---

##  Challenge Overview

This repository includes solutions to both parts of Round 1:

- **Challenge 1A:** Structured PDF outline extraction
- **Challenge 1B:** Multi-document, persona-driven content analysis

All solutions are built for **CPU-only environments**, fully **offline**, and containerized using **Docker**.

---

##  Challenge 1A – Structured PDF Processing

###  Approach

- Extract the **title** from the first page by identifying the largest font size in the top 1/3 of the page.
- Generate a **structured outline** by analyzing font sizes across the document.
- Map top font sizes to heading levels (H1, H2, H3) heuristically.

###  Libraries Used

- `PyMuPDF` (`fitz`) – for PDF parsing
- Python 3.10 – language runtime

###  How to Build & Run (Docker)


 Navigate to Challenge_1a directory
```
cd Challenge_1a
```
 Build the Docker image
```
docker build --platform linux/amd64 -t challenge1a .
```

 Run the container
 windows:
```
docker run --rm `
  -v "${PWD}\sample_dataset\pdfs:/app/input:ro" `
  -v "${PWD}\sample_dataset\outputs\challenge1a:/app/output" `
  --network none `
  challenge1a
```
linux/macOS:
```
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs/challenge1a:/app/output \
  --network none \
  challenge1a

```
>  Output: JSON files stored in sample_dataset/outputs/ with title and outline per PDF.

##  Challenge 1B – Multi-Collection Persona-Based PDF Analysis
###  Approach
- Read the persona and task from the input JSON.
-Analyze all PDFs in the collection.
-Extract relevant sections by matching heading text and paragraph content with the task.
-Rank each extracted section by estimated importance.
-Generate a final output JSON containing:
-Extracted sections with titles and page numbers
-Refined subsection content

###  Libraries Used
- PyMuPDF (fitz) – PDF parsing
- Standard Python libraries (json, os, re, etc.)

###  How to Build & Run (Docker)
 Navigate to Challenge_1b directory
```
cd ../Challenge_1b
```

 Build the Docker image
```
docker build --platform linux/amd64 -t challenge1b .
```
 Run for Collection 1:
 windows:
```
docker run --rm -v "${PWD}\Collection 1:/app/input:ro" -v "${PWD}\Collection 1:/app/output" --network none challenge1b

```
linux/macOS:
```
docker run --rm \
  -v "$(pwd)/Collection 1:/app/input:ro" \
  -v "$(pwd)/Collection 1:/app/output" \
  --network none \
  challenge1b
```
> Output: challenge1b_output.json in the same collection folder.
>➡ Repeat for Collection 2 and Collection 3 by changing the volume mount path.

### 📦 Folder Structure
```
Adobe-India-Hackathon25/
├── Challenge_1a/
│   ├── Dockerfile
│   ├── process_pdfs.py
│   ├── requirements.txt
│   └── sample_dataset/
│       ├── pdfs/
│       ├── outputs/
│       └── schema/
├── Challenge_1b/
│   ├── Dockerfile
│   ├── challenge1b.py
│   ├── Collection 1/
│   ├── Collection 2/
│   └── Collection 3/
└── README.md
```
### ✅ Constraints Satisfied
-  Offline execution only — no internet access required
-  Pure CPU execution — no GPU dependencies
-  Fully containerized using Docker
-  Deterministic output format matching Adobe's expected schemas

> Let’s connect the dots — and redefine how we read.
