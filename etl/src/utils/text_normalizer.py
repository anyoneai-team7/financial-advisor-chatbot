import re
from typing import Optional


def remove_special_chars(text: str, remove_digits: Optional[bool] = False) -> str:
    """
    Remove non-alphanumeric characters from input string.

    Args:
        text : str
            Input string.
        remove_digits : bool
            Remove digits.

    Return:
        str
            Output string.
    """
    pattern = r"[^a-zA-Z0-9\s]" if not remove_digits else r"[^a-zA-Z\s]"
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
    return re.sub(r"[\n\t]+", " ", text)


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
    special_char_removal: Optional[bool] = True,
    remove_digits: Optional[bool] = False,
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

    if special_char_removal:
        doc = remove_special_chars(doc, remove_digits=remove_digits)

        # Remove extra whitespace
    doc = remove_extra_whitespace(doc)

    # Lowercase the text
    if text_lower_case:
        doc = doc.lower()

        # Remove extra whitespace
    doc = remove_extra_whitespace(doc)
    doc = doc.strip()

    return doc
