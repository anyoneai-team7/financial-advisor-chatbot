from haystack.nodes import PDFToTextConverter
from haystack.utils import convert_files_to_docs
import os
import json


def convert_pdf_jason(pdf_directory, json_directory):
    """
    convert a PDF dataset to text and save as text dataset
    Args:
        pdf_directory (str): pdf dataset path in the local file system
        json_directory(str): directory path where save de jason

    """
    # Crear un convertidor PDFToTextConverter
    converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])

    # Cargar los archivos PDF y guardarlos como un dataset JSON
    documents = []
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            # Convertir el PDF a texto
            doc_pdf = converter.convert(
                os.path.join(pdf_directory, filename), meta=None
            )[0]
            # Create a document dictionary with the text of the PDF and other metadata

            document_dict = {
                "content": doc_pdf.content,
                "meta": {"name": filename, "file_type": "pdf", "id": doc_pdf.id},
            }
            # Add the document to the dataset
            documents.append(document_dict)
    # return documents
    # Save dicts to JSON file
    if not os.path.exists(json_directory):
        os.makedirs(json_directory)

    json_file_path = os.path.join(json_directory, "json_dataset.json")

    with open(json_file_path, "w") as f:
        json.dump(documents, f)
