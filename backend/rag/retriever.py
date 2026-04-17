import logging
from rank_bm25 import BM25Okapi
from backend.rag.embeddings import get_embedding_model, get_collection

logger = logging.getLogger(__name__)

def semantic_search(query: str, n_results: int = 10) -> list:
    model      = get_embedding_model()
    collection = get_collection()
    total      = collection.count()

    if total == 0:
        return []

    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, total),
        include=["documents", "metadatas", "distances"],
    )

    docs = []
    for i, doc in enumerate(results["documents"][0]):
        docs.append({
            "text":     doc,
            "metadata": results["metadatas"][0][i],
            "score":    float(1 - results["distances"][0][i]),
        })
    return docs

def bm25_search(query: str, n_results: int = 10) -> list:
    collection = get_collection()

    # only load top 200 most recent for BM25 to keep it fast
    all_data = collection.get(
        include=["documents", "metadatas"],
        limit=200,
    )

    if not all_data["documents"]:
        return []

    tokenized_docs = [doc.lower().split() for doc in all_data["documents"]]
    bm25           = BM25Okapi(tokenized_docs)
    scores         = bm25.get_scores(query.lower().split())

    ranked = sorted(
        zip(scores, all_data["documents"], all_data["metadatas"]),
        key=lambda x: x[0],
        reverse=True
    )[:n_results]

    return [
        {"text": doc, "metadata": meta, "score": float(score)}
        for score, doc, meta in ranked
        if score > 0
    ]

def hybrid_search(query: str, n_results: int = 5) -> list:
    semantic_results = semantic_search(query, n_results * 2)
    bm25_results     = bm25_search(query, n_results * 2)

    seen = {}
    for result in semantic_results:
        key = result["text"][:50]
        seen[key] = result

    for result in bm25_results:
        key = result["text"][:50]
        if key not in seen:
            seen[key] = result
        else:
            seen[key]["score"] = (seen[key]["score"] + float(result["score"])) / 2

    merged = sorted(
        seen.values(),
        key=lambda x: float(x["score"]),
        reverse=True
    )
    return merged[:n_results]