from typing import List
from haystack.nodes import PreProcessor, PDFToTextConverter
from src.utils.text_normalizer import normalize_text
from haystack import Document
import logging


def convert_file(path: str) -> List[Document]:
    """Converts file in path to haystack document

    Args:
        path (str): path of file to convert

    Returns:
        Document: Haystack document from pdd todument
    """
    logging.info(f"Converting file in {path} to haystack docs")
    converter = PDFToTextConverter(valid_languages=["en"])
    pdf_doc = converter.convert(path)[0]
    pdf_doc.content = normalize_text(pdf_doc.content)
    return pdf_doc


def preprocess_doc(document: Document) -> List[Document]:
    """Preprocesses document for indexing

    Args:
        document_list (List[Document])

    Returns:
        List[Document]
    """
    logging.info("Preprocessing documents for indexing")
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_length=500,
        split_overlap=20,
        split_respect_sentence_boundary=False,
    )

    docs_processed = preprocessor.process(document)
    return docs_processed
