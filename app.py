from search import get_search_results, get_chat_response
import streamlit as st
from streamlit_searchbox import st_searchbox
from duckduckgo_search import DDGS
from streamlit_extras import card
from streamlit_extras.add_vertical_space import add_vertical_space
import time

MAX_SEARCH_RESULTS = 3

st.set_page_config(
    layout="wide",
    page_title="DuckDuckLLM",
    page_icon="🦆",
)


def get_response(user_query, results):
    if not user_query:
        return
    chunks = ""
    for token in get_chat_response(user_query, results):
        chunks += token
        yield chunks


def autocomplete_callback(user_input):
    suggestions = []
    with DDGS() as ddgs:
        for r in ddgs.suggestions(user_input):
            suggestions.append(r)
    return [user_input] + [s["phrase"] for s in suggestions]


st.title(
    """🦆 DuckDuckLLM""",
)

if "autocomplete" not in st.session_state:
    st.session_state.autocomplete = ["a"]
# if "query" not in st.session_state:
#     st.session_state.query = ""
if "results" not in st.session_state:
    st.session_state.results = []
if "recent_queries" not in st.session_state:
    st.session_state.recent_queries = []
if "memory" not in st.session_state:
    st.session_state.memory = {}
if "thread" not in st.session_state:
    st.session_state.thread = []


def display_sources(results):
    with st.container():
        rows = [st.columns(3) for _ in range(len(results) // 3 + 1)]
        ts = time.time()
        for idx, r in enumerate(results):
            with rows[idx // 3][idx % 3]:
                _ = card.card(
                    key=f"card_{ts}_{idx}",
                    title=r["title"],
                    text=r["body"],
                    url=r["href"],
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "80%",
                            "border-radius": "5px",
                            "padding": "1em",
                            "margin-top": "1em",
                            "box-shadow": "0px 0px 10px 0px rgba(0,0,0,0.1)",
                        },
                        "filter": {
                            "backgroundColor": "cream",
                        },
                        "text": {
                            "color": "gray",
                            "font-weight": "lighter",
                            "font-size": "0.7rem",
                        },
                        "title": {
                            "font-size": "0.8rem",
                            "font-weight": "bold",
                            "color": "purple",
                            "font-family": "Monospace",
                            "margin-top": "1em",
                        },
                    },
                )


with st.sidebar:
    st.slider("Search results", 1, 10, MAX_SEARCH_RESULTS, 1, key="max_results")
    add_vertical_space()

    st.subheader("Recent queries")
    queries = st.session_state.recent_queries[::-1]
    if len(queries) == 0:
        st.caption("Nothing here yet...")
    # remove duplicates but keep order
    seen = set()
    seen_add = seen.add
    queries = [x for x in queries if not (x in seen or seen_add(x))]
    for query in queries:
        st.caption(f"- {query}")


if query := st_searchbox(
    autocomplete_callback,
    key="duckduckgo_suggestions",
    placeholder="Ask me anything...",
    clear_on_submit=True,
    label="",
    default_options=["Why is the meaning of life?"],
):
    st.session_state.results = []
    st.subheader("> " + query.strip())
    st.session_state.results = get_search_results(query, max_results=MAX_SEARCH_RESULTS)
    response = ""
    if query in st.session_state.memory:
        response = st.session_state.memory[query]["answer"]
        st.markdown(response)
    else:
        st.session_state.response = st.empty()
        for chunk in get_response(query, st.session_state.results):
            st.session_state.response.markdown(chunk)
        # cache the results
        st.session_state.memory[query] = {
            "answer": chunk,
            "results": st.session_state.results,
        }
        response = chunk
        st.session_state.thread.append(
            {
                "query": query,
                "answer": response,
                "results": st.session_state.results[:],
            }
        )
    st.session_state.recent_queries.append(query)
    display_sources(st.session_state.results)
    for search_item in st.session_state.thread[::-1][1:]:
        st.subheader("> " + search_item["query"].strip())
        st.markdown(search_item["answer"])
        display_sources(search_item["results"])

# TODO: keep all results in a session and keep appending them at the top
# TODO: highlight the LLM response
