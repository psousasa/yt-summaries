from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import os
import numpy as np
from dotenv import load_dotenv
import time
from openai import OpenAI

from yt_info.yt_video_data import Video, get_video_transcript

load_dotenv()

embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")

ES_URL = os.getenv("ES_URL")
INDEX_NAME = os.getenv("ES_INDEX_NAME")
es_client = Elasticsearch(ES_URL)


OLLAMA_URL = os.getenv("OLLAMA_URL")
ollama_client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")


def elastic_search_knn(field, vector, es_client=es_client):
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

    es_results = es_client.search(index=INDEX_NAME, body=search_query)

    result_docs = []

    for hit in es_results["hits"]["hits"]:
        result_docs.append(hit["_source"])

    return result_docs


def title_description_vector_knn(question: str) -> list[dict]:

    vector = embedding_model.encode(question)

    return elastic_search_knn("title_description_vector", vector)


def build_prompt(query, videos: list[Video], transcripts: str) -> str:
    prompt_template = """
You are a professional cook and recipe developer. Answer the QUESTION using only the information provided in the CONTEXT from the video transcript.
Do not include any information, assumptions, or details not present in the CONTEXT. If the CONTEXT does not provide enough information to answer the QUESTION, acknowledge the limitation.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

    context = "\n\n".join(
        [
            f"video title: {video.title}\ndescription: {video.description}\ntranscript: {transcript}"
            for video, transcript in zip(videos, transcripts)
        ]
    )
    return prompt_template.format(question=query, context=context).strip()


def llm(prompt, client=ollama_client):
    start_time = time.time()
    response = client.chat.completions.create(
        model="phi3", messages=[{"role": "user", "content": prompt}], temperature=0
    )
    answer = response.choices[0].message.content
    tokens = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    end_time = time.time()
    response_time = end_time - start_time

    return answer


def get_answer(query):

    videos = title_description_vector_knn(query)
    videos = [Video(**video) for video in videos]

    transcripts = []
    for video in videos[:1]:
        transcript = get_video_transcript(video)
        transcripts.append("\n".join([line["text"] for line in transcript]))

    prompt = build_prompt(query, videos[:1], transcripts)
    answer = llm(prompt)

    return answer
