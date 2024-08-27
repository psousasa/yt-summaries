# yt-summaries
RAG implementation to provide relevant info on video transcripts from specific YT channels

## Idea
Get key info from video transcripts.
1. List all videos from a given list of YT Channels and retrieve relevant info:
- title
- video id
- description
- if it is a short format video).

2. Index the RAG on the video title and descriptions. 
3. Return the summarized transcripts from the top matches.


~~~
Note: Short format often have no description and have less structured dialogue, making them less structured for this RAG.
~~~

## Scoring Objectives

* Problem description
    * [ ] 2 points: The problem is well-described and it's clear what problem the project solves
* RAG flow
    * [ ] 2 points: Both a knowledge base and an LLM are used in the RAG flow 
* Retrieval evaluation
    * [ ] 0 points: No evaluation of retrieval is provided
    * [ ] 1 point: Only one retrieval approach is evaluated
    * [ ] 2 points: Multiple retrieval approaches are evaluated, and the best one is used
* RAG evaluation
    * [ ] 0 points: No evaluation of RAG is provided
    * [ ] 1 point: Only one RAG approach (e.g., one prompt) is evaluated
    * [ ] 2 points: Multiple RAG approaches are evaluated, and the best one is used
* Interface
    * [ ] 2 points: UI (e.g., Streamlit), web application (e.g., Django), or an API (e.g., built with FastAPI) 
* Ingestion pipeline
    * [ ] 2 points: Automated ingestion with a Python script or a special tool (e.g., Mage, dlt, Airflow, Prefect)
* Monitoring
    * [ ] 0 points: No monitoring
    * [ ] 1 point: User feedback is collected OR there's a monitoring dashboard
    * [ ] 2 points: User feedback is collected and there's a dashboard with at least 5 charts
* Containerization
    * [ ] 2 points: Everything is in docker-compose
* Reproducibility
    * [ ] 0 points: No instructions on how to run the code, the data is missing, or it's unclear how to access it
    * [ ] 1 point: Some instructions are provided but are incomplete, OR instructions are clear and complete, the code works, but the data is missing
    * [ ] 2 points: Instructions are clear, the dataset is accessible, it's easy to run the code, and it works. The versions for all dependencies are specified.
* Best practices
    * [ ] Hybrid search: combining both text and vector search (at least evaluating it) (1 point)
    * [ ] Document re-ranking (1 point)
    * [ ] User query rewriting (1 point)
* Bonus points (not covered in the course)
    * [ ] Deployment to the cloud (2 points)