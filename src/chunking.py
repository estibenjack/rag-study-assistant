def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[str]:
    """Split text into overlapping word-based chunks.

    This implementation uses words for simplicity. In production, chunking is
    typically performed using model tokens to better match LLM context windows.
    """
    chunks = []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    words = text.split()
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        words_to_join = words[start:start + chunk_size]
        joined_str = " ".join(words_to_join)
        chunks.append(joined_str)

    return chunks


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> list[dict[str]]:
    """Split document pages into chunks while preserving metadata."""
    chunks = []

    for document in documents:
        chunked_texts = chunk_text(
            document["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk_index, chunk_text_value in enumerate(chunked_texts, start=1):
            chunks.append({
                "chunk_id": (
                    f"{document['source']}-"
                    f"page-{document['page']}-"
                    f"chunk-{chunk_index}"
                ),
                "text": chunk_text_value,
                "page": document['page'],
                "source": document['source']
            })

    return chunks


if __name__ == "__main__":
    # text = "The quick brown fox jumped over the lazy dog and ran away happily."

    # chunks = chunk_text(
    #     text=text,
    #     chunk_size=4,
    #     overlap=1
    # )

    # for i, chunk in enumerate(chunks, start=1):
    #     print(f"Chunk {i}:")
    #     print(chunk)
    #     print()

    from pathlib import Path
    from ingest import load_documents

    documents = load_documents(Path("data/documents"))

    chunks = chunk_documents(
        documents,
        chunk_size=100,
        overlap=20
    )

    # if len(chunks) >= 2:
    #     print("End of chunk 1:")
    #     print(chunks[0]["text"].split()[-20:])

    #     print("\nStart of chunk 2:")
    #     print(chunks[1]["text"].split()[:20])

    print(f"Pages loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}\n")

    if chunks:
        print("First chunk:")
        print(chunks[0])
