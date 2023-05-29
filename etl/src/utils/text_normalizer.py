import re
from typing import Optional


def remove_special_chars(text: str) -> str:
    """
    Remove non-alphanumeric characters from input string.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    pattern = r"[^a-zA-Z0-9\s\/\.,\-\&\n\t\$\%€]"
    text = re.sub(pattern, "", text)
    return text


def remove_extra_new_lines(text: str) -> str:
    """
    Remove extra new lines or tab from input string.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    return re.sub(r"[\n\t]+", "\n", text)


def remove_extra_whitespace(text: str) -> str:
    """
    Remove any whitespace from input string.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    return re.sub(r"\s+", " ", text)


def normalize_text(
    text: str,
    text_lower_case: Optional[bool] = False,
) -> str:
    """
    Normalize text

    Args:
        text : str
            Text to normalize.
        text_lower_case : bool
            Text lower case,
        special_char_removal : bool
            Special char removal,
        remove_digits : bool
            Remove digits,

    Return:
        str
            Normalized text.
    """
    # Normalize each doc in the corpus

    # Remove extra newlines
    doc = remove_extra_new_lines(text)

    doc = remove_special_chars(doc)

    # Remove extra whitespace
    doc = remove_extra_whitespace(doc)

    # Lowercase the text
    if text_lower_case:
        doc = doc.lower()

    doc = doc.strip()

    return doc
