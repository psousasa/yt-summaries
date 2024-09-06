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

ES_URL = os.getenv("LOCAL_ES_URL")
ES_INDEX_NAME = os.getenv("ES_INDEX_NAME")
es_client = Elasticsearch(ES_URL)


OLLAMA_URL = os.getenv("LOCAL_OLLAMA_URL")
ollama_client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

clients = {
    "ollama/phi3:mini": ollama_client,
    "ollama/phi3:medium": ollama_client,
    "openai/gpt-4o-mini": openai_client,
}


prompt_template = """
You are a professional cook and recipe developer. Answer the QUESTION using only the information provided in the CONTEXT from the video transcript.
Do not include any information, assumptions, or details not present in the CONTEXT. If the CONTEXT does not provide enough information to answer the QUESTION, acknowledge the limitation.

QUESTION: {question}

CONTEXT:
{context}
""".strip()


def elastic_search_knn(field, vector, es_client=es_client):
    knn = {
        "field": field,
        "query_vector": vector,
        "k": 5,
        "num_candidates": 10000,
    }

    search_query = {
        "knn": knn,
        "_source": ["title", "is_short", "description", "video_id"],
    }

    es_results = es_client.search(index=ES_INDEX_NAME, body=search_query)

    result_docs = []

    for hit in es_results["hits"]["hits"]:
        result_docs.append(hit["_source"])

    return result_docs


def elastic_search_text(query):
    search_query = {
        "_source": ["title", "is_short", "description", "video_id"],
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description"],
                        "type": "best_fields",
                    }
                },
            }
        },
    }

    response = es_client.search(index=ES_INDEX_NAME, body=search_query)
    return [hit["_source"] for hit in response["hits"]["hits"]]


def title_description_vector_knn(question: str) -> list[dict]:

    vector = embedding_model.encode(question)

    return elastic_search_knn("title_description_vector", vector)


def build_prompt(
    query, videos: list[Video], transcripts: str, prompt_template: str = prompt_template
) -> str:

    context = "\n\n".join(
        [
            f"video title: {video.title}\ndescription: {video.description}\ntranscript: {transcript}"
            for video, transcript in zip(videos, transcripts)
        ]
    )
    return prompt_template.format(question=query, context=context).strip()


def llm(prompt, model_choice):
    client = clients[model_choice]
    model = model_choice.split("/")[1]

    start_time = time.time()
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}], temperature=0
    )
    answer = response.choices[0].message.content
    tokens = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    end_time = time.time()
    response_time = end_time - start_time

    return answer, response_time, tokens


def text_search(query):
    pass


def calculate_openai_cost(model_choice, tokens):
    openai_cost = 0

    if model_choice == "openai/gpt-3.5-turbo":
        openai_cost = (
            tokens["prompt_tokens"] * 0.0015 + tokens["completion_tokens"] * 0.002
        ) / 1000
    elif model_choice in ["openai/gpt-4o", "openai/gpt-4o-mini"]:
        openai_cost = (
            tokens["prompt_tokens"] * 0.03 + tokens["completion_tokens"] * 0.06
        ) / 1000

    return openai_cost


def get_answer(query, model_choice="ollama/phi3:mini", search_type="vector"):

    if search_type == "vector":
        videos = title_description_vector_knn(query)
    elif search_type == "text":
        videos = elastic_search_text(query)
    videos = [Video(**video) for video in videos]

    transcripts = []
    for video in videos[:1]:
        transcript = get_video_transcript(video)
        transcripts.append("\n".join([line["text"] for line in transcript]))

    prompt = build_prompt(query, videos[:1], transcripts)

    answer, response_time, tokens = llm(prompt, model_choice=model_choice)

    openai_cost = calculate_openai_cost(model_choice, tokens)

    return {
        "answer": answer,
        "response_time": response_time,
        "relevance": "NOT_IMPLEMENTED",
        "relevance_explanation": "NOT_IMPLEMENTED",
        "model_used": model_choice,
        "prompt_tokens": tokens["prompt_tokens"],
        "completion_tokens": tokens["completion_tokens"],
        "total_tokens": tokens["total_tokens"],
        "eval_prompt_tokens": 0,  # eval_tokens["prompt_tokens"],
        "eval_completion_tokens": 0,  # eval_tokens["completion_tokens"],
        "eval_total_tokens": 0,  # eval_tokens["total_tokens"],
        "openai_cost": openai_cost,
    }
