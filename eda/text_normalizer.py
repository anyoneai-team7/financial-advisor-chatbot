import re
import unicodedata
from typing import List, Optional

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer

from contractions import CONTRACTION_MAP

# Download the models used
nltk.download("stopwords")
nltk.download("punkt")

# Load NLP models
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words("english")


def stem_text(text: str) -> str:
    """
    Stem input string.
    (*) Hint:
        - Use `nltk.porter.PorterStemmer` to pass this test.
        - Use `nltk.tokenize.word_tokenize` for tokenizing the sentence.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    tokens = word_tokenize(text)
    stemmer = nltk.porter.PorterStemmer()
    stemmed = [stemmer.stem(token) for token in tokens]

    return " ".join(stemmed)


def remove_accented_chars(text: str) -> str:
    """
    Remove accents from input string.

    Args:
        text : str
            Input string.

    Return:
        str
            Output string.
    """
    return "".join(
        [
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        ]
    )


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


def remove_stopwords(
    text: str,
    is_lower_case: Optional[bool] = False,
    stopwords: Optional[List[str]] = stopword_list,
) -> str:
    """
    Remove stop words using list from input string.
    (*) Hint: Use tokenizer (ToktokTokenizer) defined in the beginning for
    tokenization.

    Args:
        text : str
            Input string.
        is_lower_case : bool
            Flag for lowercase.
        stopwords : List[str]
            Stopword list.

    Return:
        str
            Output string.
    """
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(text)
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopwords]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
    filtered_text = " ".join(filtered_tokens)

    return filtered_text


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


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP) -> str:
    """
    Expand english contractions on input string.

    Args:
        text : str
            Input string.
    Return:
        str
            Output string.
    """
    contractions_pattern = re.compile(
        "({})".format("|".join(contraction_mapping.keys())),
        flags=re.IGNORECASE | re.DOTALL,
    )

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = (
            contraction_mapping.get(match)
            if contraction_mapping.get(match)
            else contraction_mapping.get(match.lower())
        )
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    text = re.sub("'", "", expanded_text)

    return text


def normalize_corpus(
    corpus: List[str],
    contraction_expansion: Optional[bool] = True,
    accented_char_removal: Optional[bool] = True,
    text_lower_case: Optional[bool] = True,
    text_stemming: Optional[bool] = False,
    special_char_removal: Optional[bool] = True,
    remove_digits: Optional[bool] = True,
    stopword_removal: Optional[bool] = True,
    stopwords: Optional[List[str]] = stopword_list,
) -> List[str]:
    """
    Normalize list of strings (corpus)

    Args:
        corpus : List[str]
            Text corpus.
        html_stripping : bool
            Html stripping,
        contraction_expansion : bool
            Contraction expansion,
        accented_char_removal : bool
            accented char removal,
        text_lower_case : bool
            Text lower case,
        text_stemming : bool
            Text stemming,
        text_lemmatization : bool
            Text lemmatization,
        special_char_removal : bool
            Special char removal,
        remove_digits : bool
            Remove digits,
        stopword_removal : bool
            Stopword removal,
        stopwords : List[str]
            Stopword list.

    Return:
        List[str]
            Normalized corpus.
    """
    normalized_corpus = []

    # Normalize each doc in the corpus
    for doc in corpus:
        # Remove extra newlines
        doc = remove_extra_new_lines(doc)

        # Remove accented chars
        if accented_char_removal:
            doc = remove_accented_chars(doc)

        # Expand contractions
        if contraction_expansion:
            doc = expand_contractions(doc)

        # Stemming text
        if text_stemming:
            doc = stem_text(doc)

        # Remove special chars and\or digits
        if special_char_removal:
            doc = remove_special_chars(doc, remove_digits=remove_digits)

        # Remove extra whitespace
        doc = remove_extra_whitespace(doc)

        # Lowercase the text
        if text_lower_case:
            doc = doc.lower()

        # Remove stopwords
        if stopword_removal:
            doc = remove_stopwords(
                doc, is_lower_case=text_lower_case, stopwords=stopwords
            )

        # Remove extra whitespace
        doc = remove_extra_whitespace(doc)
        doc = doc.strip()

        normalized_corpus.append(doc)

    return normalized_corpus


def normalize_text(
    text: str,
    contraction_expansion: Optional[bool] = True,
    accented_char_removal: Optional[bool] = False,
    text_lower_case: Optional[bool] = True,
    text_stemming: Optional[bool] = False,
    special_char_removal: Optional[bool] = True,
    remove_digits: Optional[bool] = True,
    stopword_removal: Optional[bool] = False,
    stopwords: Optional[List[str]] = stopword_list,
) -> str:
    """
    Normalize text

    Args:
        text : str
            Text to normalize.
        html_stripping : bool
            Html stripping,
        contraction_expansion : bool
            Contraction expansion,
        accented_char_removal : bool
            accented char removal,
        text_lower_case : bool
            Text lower case,
        text_stemming : bool
            Text stemming,
        text_lemmatization : bool
            Text lemmatization,
        special_char_removal : bool
            Special char removal,
        remove_digits : bool
            Remove digits,
        stopword_removal : bool
            Stopword removal,
        stopwords : List[str]
            Stopword list.

    Return:
        str
            Normalized text.
    """
    # Normalize each doc in the corpus

    # Remove extra newlines
    doc = remove_extra_new_lines(text)

    # Remove accented chars
    if accented_char_removal:
        doc = remove_accented_chars(doc)

        # Expand contractions
    if contraction_expansion:
        doc = expand_contractions(doc)

        # Stemming text
    if text_stemming:
        doc = stem_text(doc)

        # Remove special chars and\or digits
    if special_char_removal:
        doc = remove_special_chars(doc, remove_digits=remove_digits)

        # Remove extra whitespace
    doc = remove_extra_whitespace(doc)

    # Lowercase the text
    if text_lower_case:
        doc = doc.lower()

        # Remove stopwords
    if stopword_removal:
        doc = remove_stopwords(doc, is_lower_case=text_lower_case, stopwords=stopwords)

        # Remove extra whitespace
    doc = remove_extra_whitespace(doc)
    doc = doc.strip()

    return doc


def remove_tokenized_stopwords(
    tokens: List[str],
    is_lower_case: Optional[bool] = False,
    stopwords: Optional[List[str]] = stopword_list,
) -> str:
    """
    Remove stop words using list from input string.
    (*) Hint: Use tokenizer (ToktokTokenizer) defined in the beginning for
    tokenization.

    Args:
        text : str
            Input string.
        is_lower_case : bool
            Flag for lowercase.
        stopwords : List[str]
            Stopword list.

    Return:
        str
            Output string.
    """
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopwords]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords]

    return filtered_tokens
