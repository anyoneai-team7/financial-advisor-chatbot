from haystack.utils import convert_files_to_docs
import os
import json
import re


def convert_pdf_jason(pdf_directory, json_directory):
    """
    convert a PDF dataset to text and save as text dataset
    Args:
        pdf_directory (str): path of the dataset folder with companies sub-folders
        json_directory(str): directory path where save de json

    """
    document_list = []
    # Traverses the subfolders in the main directory
    for folder_name in os.listdir(pdf_directory):
        folder_path = os.path.join(pdf_directory, folder_name)

        # Checks if the path is a subfolder
        if os.path.isdir(folder_path):
            # Gets the company name from the subfolder name
            company_name = folder_name

            # Convert PDF files into documents using Haystack
            docs = convert_files_to_docs(dir_path=folder_path)

            # Processes each generated document
            for doc_pdf in docs:
                filename = doc_pdf.meta["name"]

                # Gets the year in the file name
                pattern = r"\d{4}"  # Search for a 4-digit sequence
                match = re.search(pattern, filename)

                if match:
                    year = match.group()
                else:
                    year = "unknown"

                # Crea el diccionario de metadatos y contenido del documento
                document_dict = {
                    "content": doc_pdf.content,
                    "meta": {
                        "company": company_name,
                        "name": filename,
                        "year": year,
                        "file_type": "pdf",
                        "id": doc_pdf.id,
                    },
                }

                # Adds the dictionary to the list of documents
                document_list.append(document_dict)

    # Create the directory to store the list of documents as a json.
    if not os.path.exists(json_directory):
        os.makedirs(json_directory)

    # Save documents in the file json_dataset.json
    json_file_path = os.path.join(json_directory, "json_dataset.json")
    with open(json_file_path, "w") as f:
        json.dump(document_list, f)
