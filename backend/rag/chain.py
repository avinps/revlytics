import logging
from backend.rag.retriever import hybrid_search

logger = logging.getLogger(__name__)

def build_context(results: list) -> str:
    context_parts = []
    for i, result in enumerate(results):
        meta = result["metadata"]
        context_parts.append(
            f"Review {i+1}:\n"
            f"Product: {meta.get('product_name', 'Unknown')}\n"
            f"Stars: {meta.get('star_rating', '?')}/5\n"
            f"Sentiment: {meta.get('sentiment_label', 'unknown')}\n"
            f"Topics: {meta.get('topics', 'none')}\n"
            f"Text: {result['text']}\n"
        )
    return "\n---\n".join(context_parts)

def answer_question(question: str, n_results: int = 5) -> dict:
    try:
        results = hybrid_search(question, n_results)

        if not results:
            return {
                "answer":  "No relevant reviews found for your question.",
                "sources": [],
                "query":   question,
            }

        context = build_context(results)

        positive = sum(1 for r in results if r["metadata"].get("sentiment_label") == "positive")
        negative = sum(1 for r in results if r["metadata"].get("sentiment_label") == "negative")
        avg_stars = sum(r["metadata"].get("star_rating", 0) for r in results) / len(results)

        topics_mentioned = []
        for r in results:
            topics = r["metadata"].get("topics", "")
            if topics:
                topics_mentioned.extend(topics.split(","))
        top_topics = list(set(topics_mentioned))[:5]

        answer = generate_answer(question, results, positive, negative, avg_stars, top_topics)

        return {
            "answer":     answer,
            "sources":    [
                {
                    "text":      r["text"][:200],
                    "product":   r["metadata"].get("product_name"),
                    "stars":     r["metadata"].get("star_rating"),
                    "sentiment": r["metadata"].get("sentiment_label"),
                    "topics":    r["metadata"].get("topics"),
                    "score":     round(r["score"], 3),
                }
                for r in results
            ],
            "query":      question,
            "stats": {
                "total_sources": len(results),
                "positive":      positive,
                "negative":      negative,
                "avg_stars":     round(avg_stars, 1),
                "topics":        top_topics,
            }
        }

    except Exception as e:
        logger.error(f"RAG chain error: {e}")
        return {
            "answer":  f"Error processing question: {str(e)}",
            "sources": [],
            "query":   question,
        }

def generate_answer(question, results, positive, negative, avg_stars, topics) -> str:
    total     = len(results)
    sentiment = "mostly positive" if positive > negative else "mostly negative" if negative > positive else "mixed"

    products  = list(set(r["metadata"].get("product_name", "") for r in results))
    products_str = ", ".join(products[:3])

    answer = f"Based on {total} relevant reviews"
    if products_str:
        answer += f" about {products_str}"
    answer += f", the sentiment is {sentiment} "
    answer += f"(avg rating: {round(avg_stars, 1)}/5, "
    answer += f"{positive} positive, {negative} negative). "

    if topics:
        answer += f"Key topics mentioned: {', '.join(topics)}. "

    if negative > positive:
        neg_reviews = [r for r in results if r["metadata"].get("sentiment_label") == "negative"]
        if neg_reviews:
            answer += f"Main concern: \"{neg_reviews[0]['text'][:120]}...\""
    else:
        pos_reviews = [r for r in results if r["metadata"].get("sentiment_label") == "positive"]
        if pos_reviews:
            answer += f"Customers say: \"{pos_reviews[0]['text'][:120]}...\""

    return answer