import random

import tiktoken

from src.config import MSG_PROCESSING_MESSAGES


def get_random_processing_message():
    """Get a random processing message."""
    return random.choice(MSG_PROCESSING_MESSAGES)


def estimate_tokens(text):
    """
    Estimate the number of tokens in a text using tiktoken.

    Args:
        text (str): The text to estimate tokens for

    Returns:
        int: Estimated number of tokens
    """
    try:
        # Use cl100k_base encoding (used by GPT-3.5 and GPT-4)
        # This is a reasonable approximation for most LLMs
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        # Fallback to simple heuristic if tiktoken fails
        return len(text) // 4
