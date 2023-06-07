from unittest import TestCase
import unittest
import os
import src.transform

class TestTransform (TestCase):
    def test_convert_file(self):
        """
        Test the 'convert_file' method.
        This method tests the functionality of the 'convert_file' method by verifying if it correctly converts a PDF document
        into a Document format.
        """

        path_file = os.path.join(os.getcwd(), "dataset/3d-systems-corp/NASDAQ_DDD_2017.pdf")
        doc_transform = src.transform.convert_file(path_file)
        doc_dic = doc_transform.to_dict()

        expected_structure = {
            'content': str,
            'content_type': str,
            'score': type(None),
            'meta': dict,
            'id_hash_keys': list,
            'embedding': type(None),
            'id': str
        }

        for key, value_type in expected_structure.items():
            self.assertIn(key, doc_dic)
            self.assertIsInstance(doc_dic[key], value_type)

    def test_preprocess_doc(self):
        """
        Test the 'preprocess_doc' method.
        This method tests the functionality of the 'preprocess_doc' method by verifying if it correctly preprocesses a list of documents.
        """

        path_file = os.path.join(os.getcwd(), "dataset/3d-systems-corp/NASDAQ_DDD_2017.pdf")
        doc_transform = src.transform.convert_file(path_file)
        list_documents = [doc_transform]

        result= src.transform.preprocess_doc(list_documents)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result),1)

if __name__ == '__main__':
    unittest.main()

    