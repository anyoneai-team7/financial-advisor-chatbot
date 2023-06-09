from unittest import TestCase
from src.retriever import BM25RetrieverRanker
import unittest
import src.utils


class Test_Utils(TestCase):
    def test_get_make_retriever(self):
        """
        Test case for the get_make_retriever method.
        This method tests the functionality of the get_make_retriever method.
        It verifies that the method returns an instance of BM25RetrieverRanker.
        """
        result = src.utils.make_retriever()
        self.assertIsInstance(result, BM25RetrieverRanker)

    def test_get_build_message_history(self):
        """
        Test case for the get_build_message_history method.
        This method tests the functionality of the get_build_message_history method.
        It verifies that the method returns a list.
        """
        messages_list = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        result = src.utils.build_message_history(messages_list)
        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()
