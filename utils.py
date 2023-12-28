from bs4 import BeautifulSoup
import requests
import concurrent.futures


def parse_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all paragraph tags
        paragraphs = soup.find_all("p")

        # Extract text from paragraph tags
        extracted_text = "\n".join([p.get_text() for p in paragraphs])
        return extracted_text
    else:
        return ""


def get_parsed_texts(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(parse_url, urls))
    return results
