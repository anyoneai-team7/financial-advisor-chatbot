from unittest import TestCase
from unittest.mock import Mock
import os
import unittest
import src.extract
import logging
import glob

logging.basicConfig(level=logging.INFO, format="%(processName)s %(message)s")

class TestExtract (TestCase):

    def test_get_top_company_list(self):
        """
        Test the 'get_top_company_list' method.

        This method verifies the functionality of the 'get_top_company_list' method by checking if it correctly
        returns the top companies by file count from a list of S3 objects.
        """
        mock_objects = [
            Mock(key="dataset/american-resources-corporation/file1.pdf"),
            Mock(key="dataset/american-resources-corporation/file2.pdf"),
            Mock(key="dataset/acelrx-pharmaceuticals/file3.pdf"),
            Mock(key="dataset/atomera-inc/file4.pdf"),
            Mock(key="dataset/acelrx-pharmaceuticals/file5.pdf"),
            Mock(key="dataset/acelrx-pharmaceuticals/file6.pdf"),
            Mock(key="dataset/atomera-inc/file7.pdf"),
            Mock(key="dataset/Independent-bank-corporation/file8.pdf"),
            Mock(key="dataset/Independent-bank-group-Inc/file9.pdf"),
            Mock(key="dataset/Inogen-Inc/file11.pdf"),
            Mock(key="dataset/Insmed-Incorporated/file12.pdf"),
            Mock(key="dataset/Insulet-corporation/file13.pdf"),
            Mock(key="dataset/Intersect-ENT-Inc/file14.pdf"),
            Mock(key="dataset/Intra-Cellular-therapies-Inc/file15.pdf"),
            Mock(key="dataset/Investors-Bancorp-Inc/file16.pdf"),
            Mock(key="dataset/Independent-bank-corporation/file17.pdf"),
            Mock(key="dataset/Independent-bank-group-Inc/file18.pdf"),
            Mock(key="dataset/Innospec-Inc/file19.pdf"),
            Mock(key="dataset/Inogen-Inc/file20.pdf"),
            Mock(key="dataset/Insmed-Incorporated/file21.pdf"),
            Mock(key="dataset/Intersect-ENT-Inc/file23.pdf"),
            Mock(key="dataset/Independent-bank-corporation/file24.pdf"),
            Mock(key="dataset/Independent-bank-group-Inc/file25.pdf"),
            Mock(key="dataset/Innospec-Inc/file26.pdf"),
            Mock(key="dataset/Inogen-Inc/file27.pdf"),
            Mock(key="dataset/Insmed-Incorporated/file28.pdf"),
            Mock(key="dataset/Insulet-corporation/file29.pdf"),
            Mock(key="dataset/Investors-Bancorp-Inc/file30.pdf"),
            Mock(key="dataset/Independent-bank-corporation/file31.pdf"),
            Mock(key="dataset/Independent-bank-group-Inc/file32.pdf"),
        ]
        companies = src.extract._get_top_company_list(mock_objects, top = 5)
        expected_companies = [
            'Independent-bank-corporation', 'Independent-bank-group-Inc', 'Insmed-Incorporated', 'Inogen-Inc', 'acelrx-pharmaceuticals'
        ]

        self.assertTrue(all(element in expected_companies for element in companies))
        self.assertEqual(len(companies), 5)
        self.assertTrue(isinstance(companies, list))


    def test_extract_docs(self):
        """
            Test the 'extract_docs' method.
            This method tests the functionality of the 'extract_docs' method by verifying if it correctly downloads
            the contents of a specified folder directory from an S3 bucket to the local machine.
        """
        path_files = os.path.join(os.getcwd(), "dataset")
        tam_files = 0

        if os.path.exists(path_files):
            files = glob.glob(os.path.join(path_files, "*/*_*.pdf"))
            tam_files = len(files)

        self.assertTrue(os.path.exists(path_files))
        self.assertGreater(tam_files,1)


if __name__ == '__main__':
    unittest.main()