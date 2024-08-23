from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import os
import numpy as np
from dotenv import load_dotenv

# from yt_info.yt_video_data import get_video_transcript, Video
from yt_rag.build_index import embed

load_dotenv()

embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")

es_endpoint = os.getenv("ES_ENDPOINT")
es_client = Elasticsearch(es_endpoint)

index_name = os.getenv("ES_INDEX_NAME")


def elastic_search_knn(field, vector):
    knn = {
        "field": field,
        "query_vector": vector,
        "k": 20,
        "num_candidates": 10000,
    }

    search_query = {
        "knn": knn,
        "_source": ["title", "is_short", "description", "course", "video_id"],
    }

    es_results = es_client.search(index=index_name, body=search_query)

    result_docs = []

    for hit in es_results["hits"]["hits"]:
        result_docs.append(hit["_source"])

    return result_docs


def title_description_vector_knn(question: str) -> list[dict]:

    vector = embedding_model.encode(question)

    return elastic_search_knn("title_description_vector", vector)
