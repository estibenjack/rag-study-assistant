from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model() -> SentenceTransformer:
    """Load and return the embedding model."""
    model = SentenceTransformer(MODEL_NAME)
    return model


def embed_texts(
    texts: list[str],
    model: SentenceTransformer
) -> list[list[float]]:
    """Generate embeddings for a list of text strings."""
    embeddings = model.encode(texts)
    return embeddings.tolist()


def embed_chunks(
    chunks: list[dict],
    model: SentenceTransformer
) -> list[dict]:
    """Add embeddings to chunks while preserving metadata."""
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embed_texts(texts, model)

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            **chunk,
            "embedding": embedding
        })

    return embedded_chunks


if __name__ == "__main__":
    from pathlib import Path
    from ingest import load_documents
    from chunking import chunk_documents

    model = load_embedding_model()

    documents = load_documents(Path("data/documents"))

    chunks = chunk_documents(
        documents,
        chunk_size=100,
        overlap=20
    )

    embedded_chunks = embed_chunks(chunks, model)

    print(f"Pages: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embedded chunks: {len(embedded_chunks)}")
    print(f"Embedding dimensions: {len(embedded_chunks[0]['embedding'])}")
