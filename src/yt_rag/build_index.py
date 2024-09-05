from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import os
from tqdm.auto import tqdm
from ast import literal_eval
import numpy as np
from dotenv import load_dotenv
import pickle

from yt_info.yt_video_data import get_channel_videos, Video

load_dotenv()

embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")

es_endpoint = os.getenv("LOCAL_ES_URL")
es_client = Elasticsearch(es_endpoint)


def embed_title_description(video: Video) -> np.array:

    video_text = f"{video.title} {video.description}".strip()

    return embedding_model.encode(video_text)


def embed_title(video: Video) -> np.array:

    video_text = f"{video.title}".strip()

    return embedding_model.encode(video_text)


def create_embeddings(
    videos: list[Video], embedding_function=embed_title_description
) -> list[np.array]:
    embeddings = []
    print("Starting embedding...")
    for video in tqdm(videos):
        embeddings.append(embedding_function(video))
    print("...embedding done.")
    return embeddings


def build_index(videos: list[Video], embeddings, index_name, es_client=es_client):

    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "is_short": {"type": "text"},
                "description": {"type": "text"},
                "video_id": {"type": "keyword"},
                "title_description_vector": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }

    es_client.indices.delete(index=index_name, ignore_unavailable=True)
    es_client.indices.create(index=index_name, body=index_settings)

    print("Started indexing...")
    for video, emb in zip(tqdm(videos), embeddings):
        es_client.index(
            index=index_name,
            document={**video.__dict__, **{"title_description_vector": emb}},
        )

    print("...indexing done.")


def get_yt_videos():
    channels = literal_eval(os.getenv("YT_CHANNELS"))
    yt_api_key = os.getenv("YT_API_KEY")
    videos = get_channel_videos(
        channel_id=channels["Joshua Weissman"], api_key=yt_api_key
    )
    return videos


def main():
    index_name = os.getenv("ES_INDEX_NAME")

    if not es_client.indices.exists(index=index_name):

        # avoid indexing from youtube, use pre-downloaded data instead

        with open("./data/yt_videos_details.pkl", "rb") as f:
            videos = pickle.load(f)

        embeddings = create_embeddings(videos)
        build_index(videos, embeddings, index_name)


if __name__ == "__main__":
    main()
