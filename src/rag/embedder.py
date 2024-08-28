import csv
from collections import namedtuple
from pathlib import Path

import numpy as np
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.config import get_settings, get_vector_database_settings
from src.logger import logger
from src.rag.constants import FAQ_PATH, INTERMEDIARY_PATH

FAQRow = namedtuple("FAQRow", ["heading", "question", "answer"])


def _load_data(filepath) -> list[FAQRow]:
    """
    Load data from the CSV file
    """
    with filepath.open(newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        next(csv_reader)  # Skip the header row
        return [
            FAQRow(heading=row[0], question=row[1], answer=row[2]) for row in csv_reader
        ]


def _compute_embeddings_single(question: str):
    """
    Compute embeddings for the question.
    """
    openai_client = OpenAI(
        api_key=get_settings().openai_dev_service_account,
        project=get_settings().openai_project_id,
    )
    response = openai_client.embeddings.create(
        input=question, model=get_vector_database_settings().openai_embedder_name
    )
    return response.data[0].embedding


def get_query_vector(query: str):
    """
    Alias for _compute_embeddings_single for use with qdrant.py
    """
    embedding = _compute_embeddings_single(query)
    return embedding


def _compute_embeddings_batch(questions: list[str]):
    embeddings = []
    for question in questions:
        embedding = _compute_embeddings_single(question)
        embeddings.append(embedding)
    return embeddings


def compute_embeddings():
    faq_rows = _load_data(FAQ_PATH)
    questions = [faq_row.question for faq_row in faq_rows]
    embeddings = _compute_embeddings_batch(questions)
    # save to a file
    embeddings_np = np.array(embeddings)
    np.save(INTERMEDIARY_PATH.as_posix(), embeddings_np, allow_pickle=False)
    logger.info("Embeddings saved to intermediary file")
    logger.info(f"Embedding shape: {embeddings_np.shape}")


if __name__ == "__main__":
    compute_embeddings()
