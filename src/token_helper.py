import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """
    Returns the exact number of tokens in a text string using OpenAI's official tokenizer.
    """
    try:
        # Get the specific encoding for the chosen model
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to the standard encoding for newer models if not found
        encoding = tiktoken.get_encoding("o200k_base")
        
    token_count = len(encoding.encode(text))
    return token_count

def estimate_cost(token_count: int, cost_per_1m_tokens: float = 5.00) -> float:
    """Estimates the input cost based on current OpenAI pricing."""
    return (token_count / 1_000_000) * cost_per_1m_tokens

