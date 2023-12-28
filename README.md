# DuckDuckLLM

DuckDuckLLM = DuckDuckGo + Open-source LLM

## How does it work?

It simply searches duckduckgo for the query and then creates a stuffed prompt for the LLM. The LLM generates a response based on the user query and the reference articles.

For v0, we simply pass the title and the body of the top-3 articles to the LLM.

## Dependencies

- Python 3.10+
- Poetry
- [LM Studio](https://lmstudio.ai/)

## Installation

- Download model: You could use any model you want. For this app, I am using openhermes-2.5-mistral-7b.Q5_K_M.gguf.
- Start LM Studio Server (OpenAI-compatible API)
- Run streamlit app
    ```bash
    poetry shell
    poetry install
    ```

## Usage

```bash
streamlit run app.py
```