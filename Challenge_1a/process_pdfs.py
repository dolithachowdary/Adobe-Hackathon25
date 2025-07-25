import os
import json
import fitz  # PyMuPDF
import numpy as np
from pathlib import Path

def extract_title(page):
    """Extract document title from first page"""
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
    if not blocks: 
        return ""
    
    # Find largest font size in top 1/3 of page
    max_size = 0
    candidate_text = ""
    for block in blocks:
        for line in block.get("lines", []):
            for span in line["spans"]:
                # Check if span is in top 1/3 of page
                if span["bbox"][1] < page.rect.height * 0.33:
                    if span["size"] > max_size:
                        max_size = span["size"]
                        candidate_text = span["text"]
    return candidate_text.strip()

def extract_headings(doc):
    """Extract hierarchical headings from document"""
    heading_candidates = []
    font_styles = set()
    
    # First pass: collect all candidate headings and font sizes
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:  # Only consider non-empty text
                        heading_candidates.append({
                            "text": text,
                            "size": span["size"],
                            "page": page_num + 1
                        })
                        font_styles.add(span["size"])
    
    if not heading_candidates:
        return []
    
    # Determine heading levels based on font size distribution
    unique_sizes = sorted(font_styles, reverse=True)
    size_to_level = {}
    
    # Map top 3 sizes to H1, H2, H3
    for i, size in enumerate(unique_sizes[:3]):
        size_to_level[size] = f"H{i+1}"
    
    # Create outline
    outline = []
    for candidate in heading_candidates:
        level = size_to_level.get(candidate["size"], "H3")
        outline.append({
            "level": level,
            "text": candidate["text"],
            "page": candidate["page"]
        })
    
    return outline

def process_pdf(input_path):
    """Process single PDF file"""
    with fitz.open(input_path) as doc:
        return {
            "title": extract_title(doc[0]),
            "outline": extract_headings(doc)
        }

if __name__ == "__main__":
    input_dir = Path("/app/input")      
    output_dir = Path("/app/output") 
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for pdf_file in input_dir.glob("*.pdf"):
        try:
            print(f"Processing {pdf_file.name}...")
            result = process_pdf(str(pdf_file))
            output_file = output_dir / f"{pdf_file.stem}.json"
            
            with output_file.open("w") as f:
                json.dump(result, f, indent=2)
                
            print(f"Created {output_file.name}")
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {str(e)}")