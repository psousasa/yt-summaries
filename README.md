# yt-summaries

RAG implementation to provide relevant info from video transcripts of specific YT channels.

Initially designed to serve as a cooking assistant, taking in cooking channels and providing recipes based on the video transcripts.

This RAG flow can be easily adapted to other channels and make it quick to create new assistants.


## Idea

Build knowledge base (KB) from YT videos data.
1. List all videos from a given list of YT Channels and build KB from:
- title
- video id
- description
- if it is a short format video.
2. Index the KB on the videos title and description. 
3. Get user query through Streamlit.
4. Query the KB and get relevant videos.
5. Get the transcripts of the relevant videos.
6. Call the LLM, asking it to summarize and retrieve recipes from the transcripts.
7. Output the summary through Streamlit.


~~~
Note: Short format videos often have no description and have less structured dialogue, making them less ideal for this RAG.
~~~


## Dataset

The dataset is made of YT videos info - details and english transcript. The channel(s) from which to retrieve the videos is predefined. \

**Details** retrieved using:
```python
pip install google-api-python-client
```

**Transcripts** retrieved using:
```python
pip install youtube-transcript-api
```

## Setup

### Grafana 
Setting up ```user: 0```because of ownership issues when creating the grafana container.


## How to Run

### Prerequisites

- Docker.
- Python's build module
- <20Gb RAM (using Ollama/Phi3 and for the default YT channel).
- Clone the repo.
- Environment variables:
    1. Create copy of *sample.env* named *.env* in same directory.
    2. Fill in variables.


### Launching the Assistant

1. Open a terminal in the repo root.
2. Build the dist .whl file:
```bash
make build
```
3. Build the container. This will:
```bash
docker compose up
```
- Load the data from the predefined YT channels.
- Feed and index the KB.
    - This is only done if the index doesn't exist in ElasticSearch.
- Launch the Streamlit App in a browser.


### Evaluation

#### Retrieval

Title + descripts and Phi3-Mini yields
```{'hit_rate': 0.6947574718275356, 'mrr': 0.5127479915696481}```


#### RAG

## Scoring Objectives

* Problem description
    * [x] 2 points: The problem is well-described and it's clear what problem the project solves
* RAG flow
    * [x] 2 points: Both a knowledge base and an LLM are used in the RAG flow 
* Retrieval evaluation
    * [x] 1 point: Only one retrieval approach is evaluated
    * [ ] 2 points: Multiple retrieval approaches are evaluated, and the best one is used
* RAG evaluation
    * [ ] 0 points: No evaluation of RAG is provided
    * [ ] 1 point: Only one RAG approach (e.g., one prompt) is evaluated
    * [ ] 2 points: Multiple RAG approaches are evaluated, and the best one is used
* Interface
    * [x] 2 points: UI (e.g., Streamlit), web application (e.g., Django), or an API (e.g., built with FastAPI) 
* Ingestion pipeline
    * [x] 2 points: Automated ingestion with a Python script or a special tool (e.g., Mage, dlt, Airflow, Prefect)
* Monitoring
    * [ ] 0 points: No monitoring
    * [ ] 1 point: User feedback is collected OR there's a monitoring dashboard
    * [ ] 2 points: User feedback is collected and there's a dashboard with at least 5 charts
* Containerization
    * [x] 2 points: Everything is in docker-compose
* Reproducibility
    * [x] 2 points: Instructions are clear, the dataset is accessible, it's easy to run the code, and it works. The versions for all dependencies are specified.
* Best practices
    * [ ] Hybrid search: combining both text and vector search (at least evaluating it) (1 point)
    * [ ] Document re-ranking (1 point)
    * [ ] User query rewriting (1 point)
    * [x] Added tests for the ETL into KB.
* Bonus points (not covered in the course)
    * [ ] Deployment to the cloud (2 points)