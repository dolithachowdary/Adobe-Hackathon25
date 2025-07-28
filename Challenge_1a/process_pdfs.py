
import os
import json
import re
import fitz  # PyMuPDF
import numpy as np
from collections import defaultdict

def clean_text(text):
    """Clean and normalize text by removing extra spaces and special characters"""
    # Replace multiple spaces with single space
    cleaned = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing non-alphanumeric characters
    cleaned = re.sub(r'^[^\w]+|[^\w]+$', '', cleaned)
    # Remove control characters and special formatting
    cleaned = re.sub(r'[\x00-\x1F]', '', cleaned)
    return cleaned.strip()

def extract_structure(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    headings = []
    font_sizes = []
    page_dimensions = []
    
    # First pass: Collect global font statistics
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_dimensions.append((page.rect.width, page.rect.height))
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip():
                        font_sizes.append(span["size"])
    
    if not font_sizes:
        doc.close()
        return "", []
    
    # Calculate global font statistics
    global_median = np.median(font_sizes)
    global_std = np.std(font_sizes) if len(font_sizes) > 1 else 2.0
    
    # Process first page for title
    if len(doc) > 0:
        first_page = doc[0]
        title_candidates = []
        blocks = first_page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        
        for block in blocks:
            # Consider only top 25% of page for title
            if block["bbox"][1] < first_page.rect.height * 0.25:
                block_text = ""
                block_font_sizes = []
                
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            block_text += text + " "
                            block_font_sizes.append(span["size"])
                
                if block_text and block_font_sizes:
                    avg_size = np.mean(block_font_sizes)
                    # Only consider significantly larger text
                    if avg_size > global_median + global_std:
                        clean_block = clean_text(block_text)
                        if clean_block and len(clean_block) > 5:
                            title_candidates.append((clean_block, avg_size))
        
        # Select best title candidate
        if title_candidates:
            # Prefer candidates with largest font size
            title_candidate = max(title_candidates, key=lambda x: x[1])
            title = title_candidate[0]
    
    # Process all pages for headings
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_width, page_height = page_dimensions[page_num]
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        
        for block in blocks:
            # Skip blocks in header/footer regions
            if (block["bbox"][1] < page_height * 0.1 or 
                block["bbox"][3] > page_height * 0.9):
                continue
                
            block_text = ""
            font_sizes = []
            is_bold = False
            is_centered = False
            line_count = 0
            
            for line in block["lines"]:
                line_count += 1
                line_text = ""
                line_font_sizes = []
                
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        line_text += text + " "
                        line_font_sizes.append(span["size"])
                        # Check for bold formatting
                        if "bold" in span["font"].lower() or span["flags"] & 2**4:
                            is_bold = True
                
                if line_text:
                    # Calculate line positioning
                    x0 = min(span["bbox"][0] for span in line["spans"])
                    x1 = max(span["bbox"][2] for span in line["spans"])
                    line_center = (x0 + x1) / 2
                    is_centered = abs(line_center - page_width/2) < (page_width * 0.2)
                    
                    block_text += line_text
                    font_sizes.extend(line_font_sizes)
            
            clean_block = clean_text(block_text)
            if not clean_block or clean_block == title:
                continue
                
            # Skip obvious non-headings
            if (len(clean_block) < 3 or  # Too short
                len(clean_block.split()) > 15 or  # Too long
                re.match(r'^\d{1,2}[-–/]\d{1,2}[-–/]\d{2,4}$', clean_block) or  # Dates
                re.match(r'^\d+$', clean_block) or  # Page numbers
                clean_block.lower() in ["confidential", "draft", "internal use"] or
                (not is_bold and not is_centered) or  # Formatting requirements
                line_count > 3):  # Too many lines
                continue
                
            # Calculate block statistics
            if not font_sizes:
                continue
                
            avg_size = np.mean(font_sizes)
            size_diff = avg_size - global_median
            
            # Determine heading level
            level = None
            if size_diff > 3 * global_std:
                level = "H1"
            elif size_diff > 2 * global_std:
                level = "H2"
            elif size_diff > global_std:
                level = "H3"
            elif size_diff > 0.5 * global_std:
                level = "H4"
                
            if level:
                headings.append({
                    "level": level,
                    "text": clean_block,
                    "page": page_num + 1  # 1-indexed page numbers
                })
    
    doc.close()
    return title, headings

def process_directory(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            try:
                title, outline = extract_structure(pdf_path)
                output_data = {
                    "title": title,
                    "outline": outline
                }
                
                json_filename = f"{os.path.splitext(filename)[0]}.json"
                output_path = os.path.join(output_dir, json_filename)
                
                with open(output_path, 'w') as json_file:
                    json.dump(output_data, json_file, indent=2)
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    # input_dir = 'sample_dataset/pdfs'
    # output_dir = 'sample_dataset/outputs'
    input_dir = Path("/app/input")      
    output_dir = Path("/app/output") 
    
    
    os.makedirs(output_dir, exist_ok=True)
    process_directory(input_dir, output_dir)


