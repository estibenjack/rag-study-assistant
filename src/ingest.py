from pathlib import Path
import pymupdf


def load_pdf(file_path: Path) -> list[dict]:
    """Extract text and metadata from each non-empty page of a PDF."""
    pages_list = []

    pdf = pymupdf.open(file_path)

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        page_text = page.get_text().strip()

        if not page_text:
            continue

        pages_list.append({
            "page": page_num + 1,
            "text": page_text,
            "source": file_path.name
        })

    pdf.close()
    return pages_list


def load_documents(directory: str | Path) -> list[dict]:
    """Load all PDF files from a directory."""
    pass


# test block
if __name__ == "__main__":
    test_pdf_path = Path(
        "data/documents/Databricks-Certified-Generative-AI-Engineer-Associate-Exam-Guide-Mar26.pdf"
    )

    pages = load_pdf(test_pdf_path)

    print(f"Number of extracted pages: {len(pages)}\n")

    if pages:
        print("First extracted page:\n")
        print(pages[0])
