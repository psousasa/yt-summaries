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