import os
import json
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime


def load_input(input_path):
    with open(input_path, "r") as f:
        return json.load(f)


def get_keywords(job_description):
    # Simple keyword extraction: words longer than 3 characters
    words = job_description.lower().replace(",", "").split()
    keywords = [word for word in words if len(word) > 3]
    return keywords


def extract_relevant_sections(pdf_path, keywords):
    doc = fitz.open(pdf_path)
    relevant = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4].strip()
            if not text:
                continue

            lower_text = text.lower()
            score = sum(kw in lower_text for kw in keywords)

            if score > 0:
                section_title = text.split("\n")[0][:80]
                relevant.append({
                    "document": os.path.basename(pdf_path),
                    "page": page_num + 1,
                    "section_title": section_title,
                    "refined_text": text,
                    "importance_score": score
                })

    return relevant


def rank_sections(all_sections):
    ranked = sorted(all_sections, key=lambda x: -x["importance_score"])
    top_sections = ranked[:5]

    extracted = []
    analysis = []

    for rank, sec in enumerate(top_sections, 1):
        extracted.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": rank,
            "page_number": sec["page"]
        })

        analysis.append({
            "document": sec["document"],
            "refined_text": sec["refined_text"],
            "page_number": sec["page"]
        })

    return extracted, analysis


def main():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    input_json = load_input(input_dir / "challenge1b_input.json")
    persona = input_json["persona"]["role"]
    job = input_json["job_to_be_done"]["task"]
    documents = input_json["documents"]

    keywords = get_keywords(job)
    all_sections = []

    for doc in documents:
        pdf_path = input_dir / "PDFs" / doc["filename"]
        if not pdf_path.exists():
            print(f"❌ Warning: {pdf_path} not found.")
            continue
        all_sections.extend(extract_relevant_sections(pdf_path, keywords))

    extracted, analysis = rank_sections(all_sections)

    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted,
        "subsection_analysis": analysis
    }

    output_path = output_dir / "challenge1b_output.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print("✅ challenge1b_output.json created.")


if __name__ == "__main__":
    main()
