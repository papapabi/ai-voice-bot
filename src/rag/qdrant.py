import uuid

import numpy as np
from qdrant_client import QdrantClient, models

from src.config import get_vector_database_settings
from src.rag.embedder import _load_data, get_query_vector
from src.rag.constants import FAQ_PATH, INTERMEDIARY_PATH


def create_collection(collection_name: str):
    host = get_vector_database_settings().qdrant_host
    port = get_vector_database_settings().qdrant_rest_api_port

    client = QdrantClient(f"http://{host}:{port}")

    size = get_vector_database_settings().openai_embedder_size

    client.recreate_collection(
        collection_name, models.VectorParams(size=size, distance=models.Distance.COSINE)
    )

    embeddings = np.load(INTERMEDIARY_PATH.as_posix())
    faq_rows = _load_data(FAQ_PATH)
    for faq_row, embedding in zip(faq_rows, embeddings):
        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "heading": faq_row.heading,
                        "question": faq_row.question,
                        "answer": faq_row.answer,
                    },
                )
            ],
        )


def search(q: str, limit=3) -> list[dict[str, str]]:
    """
    Perform a vector similarity search over the specified collection.

    Args:
        q: The query string.
        collection_name: The name of the collection to search.
        limit: The maximum number of results to return.
    
    Returns:
        A list of dictionaries containing the search results.
        They contain similarity score, answer, and match fields.
    """
    collection_name = get_vector_database_settings().collection_name
    host = get_vector_database_settings().qdrant_host
    port = get_vector_database_settings().qdrant_rest_api_port
    client = QdrantClient(f"http://{host}:{port}")

    query_vector = get_query_vector(q)

    # pertinent fields for search_result are:
    # 1. id - id of stored point
    # 2. score - similarity score
    # 3. payload - dictionary containing the payload for each stored point
    search_results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=None,
        search_params=models.SearchParams(exact=False),
        limit=limit,
    )
    search_results = search_results.points

    final_results = []
    for result in search_results:
        final_results.append(
            {
                "score": result.score,
                "answer": result.payload["answer"],
                "match": result.payload["question"],
            }
        )

    return final_results


if __name__ == "__main__":
    # create_collection(collection_name)
    response = search(
        "Good morning! Just want to ask, how can I pay my billease bill?",
    )
    print(response)
