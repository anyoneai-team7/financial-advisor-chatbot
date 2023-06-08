from unittest import TestCase
import unittest
import src.utils.text_normalizer

class TestUtils (TestCase):
    def test_remove_special_chars(self):
        """
        Test the 'remove_special_chars' method.
        This method tests the functionality of the 'remove_special_chars' method by verifying if it correctly removes special characters from a given text.
        """

        doc_text = (
                "hello? there A-Z-R_T(,**), world, welcome to python. "
                "this **should? the next line #followed- by@ an#other %million^ %%like $this."
            )
        good_text = (
            'hello there A-Z-RT,, world, welcome to python. this should the next line followed- by another %million %%like $this.'
        )
        t1 = src.utils.text_normalizer.remove_special_chars(doc_text)
        assert good_text == t1

    def test_remove_extra_new_lines(self):
        """
        Test the 'remove_extra_new_lines' method.
        This method tests the functionality of the 'remove_extra_new_lines' method by verifying if it correctly removes extra new lines from a given text.
        """

        doc_new_lines = """we\n\n\nuse\na\n\nlot\nof\n\nlines"""
        good_new_lines = "we\nuse\na\nlot\nof\nlines"
        t1 = src.utils.text_normalizer.remove_extra_new_lines(doc_new_lines)
        assert good_new_lines == t1

    def test_remove_extra_whitespace(self):
        """
        Test the 'remove_extra_whitespace' method.
        This method tests the functionality of the 'remove_extra_whitespace' method by verifying if it correctly removes extra whitespace from a given text.
        """

        doc_spaces = "Hello           my      dear          friend"
        good_spaces = "Hello my dear friend"
        t1 = src.utils.text_normalizer.remove_extra_whitespace(doc_spaces)
        assert good_spaces == t1


if __name__ == '__main__':
    unittest.main()