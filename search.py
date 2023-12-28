# Refactored code
import os
import sys
from openai import OpenAI
from duckduckgo_search import DDGS
import streamlit as st
import datetime

from datetime import datetime

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")


current_date = datetime.now().isoformat()
SYSTEM_MESSAGE = f"""
You are DuckDuckLLM - a search engine for answering user queries based on DuckDuckGo search results.
You will be given the results from DuckDuckGo (inside <duckduckgo> </duckduckgo>) and you will have to answer the user's query based on the search results.
First you must read the search results, rank them in order of relevance (internally) and then answer the user's query.
Not all search results are relevant to the user's query.
Keep your answers accurate, meaningful and concise.
Depending on the user's query, you may have to answer with a short sentence or a long paragraph.
Avoid using adjectives in your answer.

----
Current date: {current_date}.
----
"""


@st.cache_data(show_spinner=False, persist=True)
def get_search_results(user_query, max_results=3, timelimit="m", safesearch="on"):
    results = []
    with DDGS() as ddgs:
        results = [
            r
            for r in ddgs.text(
                user_query,
                safesearch=safesearch,
                backend="lite",
                max_results=max_results,
                timelimit=timelimit,
            )
        ]

    return results


def generate_prompt(results, user_query):
    results_str = "\n".join(
        [f"""[{idx+1}] {r['title']}\n{r['body']}""" for idx, r in enumerate(results)]
    )

    prompt = f"""<duckduckgo>
    {results_str}
    </duckduckgo>
    question: {user_query}
    answer:
    """
    return prompt


def get_chat_response(user_query, results):
    prompt = generate_prompt(results, user_query)
    response = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=[
            {
                "role": "system",
                "content": SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        stream=True,
        max_tokens=1024,
    )

    for chunk in response:
        if chunk.choices[0].finish_reason == "stop":
            yield "\n"
            break
        yield chunk.choices[0].delta.content


# Usage

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python search.py <user_query>")
        sys.exit(1)
    user_query = sys.argv[1]
    results = get_search_results(user_query)
    prompt = generate_prompt(results, user_query)
    get_chat_response(prompt)
