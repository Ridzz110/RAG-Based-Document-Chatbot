from typing import Dict, List
from sentence_transformers import SentenceTransformer
from vector_store import load_index

def retrieve_relevant_chunks (query: str, model: SentenceTransformer, top_k: int = 5) -> List[Dict]:
    index, data = load_index()
    texts = data["texts"]
    metadatas = data["metadata"]
    query_embedding = model.encode(
        [query],
        convert_to_numpy= True,
        normalize_embeddings= True
    )
    scores, indices = index.search(query_embedding, top_k)
    retrieved_chunks = []
    for score, idx in zip(scores[0], indices[0]):
        retrieved_chunks.append(
            {
                "text": texts[idx],
                "metadata": metadatas[idx],
                "score": float(score)
            }
        )

    return retrieved_chunks

