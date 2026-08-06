from pathlib import Path
import pymupdf


def load_pdf(file_path: Path) -> list[dict]:
    """Extract text and metadata from each non-empty page of a PDF."""
    pages = []

    pdf = pymupdf.open(file_path)

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        page_text = page.get_text().strip()

        if not page_text:
            continue

        pages.append({
            "page": page_num + 1,
            "text": page_text,
            "source": file_path.name
        })

    pdf.close()
    return pages


def load_documents(directory: str | Path) -> list[dict]:
    """Load all PDF files from a directory."""
    directory = Path(directory)
    documents = []

    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Invalid directory: '{directory}'")

    pdf_files = directory.glob("*.pdf")

    for pdf_file in pdf_files:
        documents.extend(load_pdf(pdf_file))

    return documents


"""
Documents structure for ref:
[
    {"page": 1, "text": "...", "source": "guide.pdf"},
    {"page": 2, "text": "...", "source": "guide.pdf"},
    {"page": 1, "text": "...", "source": "notes.pdf"}
]
"""


# test block
if __name__ == "__main__":
    # test_pdf_path = Path(
    #     "data/documents/Databricks-Certified-Generative-AI-Engineer-Associate-Exam-Guide-Mar26.pdf"
    # )

    # pages = load_pdf(test_pdf_path)

    # print(f"Number of extracted pages: {len(pages)}\n")

    # if pages:
    #     print("First extracted page:\n")
    #     print(pages[0])

    documents = load_documents(Path("data/documents"))

    print(f"Total extracted pages: {len(documents)}")

    if documents:
        print(documents[0])
