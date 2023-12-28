# DuckDuckLLM

DuckDuckLLM = DuckDuckGo + Open-source LLM

## How does it work?

It simply searches duckduckgo for the query and then creates a stuffed prompt for the LLM. The LLM generates a response based on the user query and the reference articles.

For v0, we simply pass the title and the body of the top-3 articles to the LLM.

## Dependencies

- Python 3.10+
- Poetry

## Installation

```bash
poetry shell
poetry install
```

## Usage

```bash
streamlit run app.py
```