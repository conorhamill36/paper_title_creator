"""Helper functions related to LLM usage"""

from loguru import logger
import openai


def get_api_key(api_key_path: str):
    """
    Gets api key from filepath
    """
    logger.debug(f"Reading API key from {api_key_path}")
    with open(api_key_path) as f:
        api_key = f.readline().strip()
    return api_key


def openai_api_call(client: openai.Client, message: str, model: str = "gpt-3.5-turbo"):
    """
    Makes call to openai API and returns text of response
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": message},
        ],
    )
    return response.choices[0].message.content


PROMPT_CONTEXT = """
    You are a helpful assistant who helps name the files for academic papers.
    The following is text extracted from the first page of an academic paper.
    Return a single slug containing the year, surname of the author and two/three words describing the paper subject, separated by underscores.

"""
