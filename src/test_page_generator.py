import unittest

import page_generator

class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = "# 1234"
        title = page_generator.extract_title(md)
        self.assertEqual(title, "1234")

if __name__ == "__main__":
    unittest.main()
