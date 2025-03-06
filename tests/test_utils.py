import unittest
import os
from src.utils import detect_encoding

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.txt_path = "data/sample.txt"

    def test_detect_encoding(self):
        if os.path.exists(self.txt_path):
            encoding = detect_encoding(self.txt_path)
            self.assertIsInstance(encoding, str)
            self.assertIn(encoding.lower(), ['utf-8', 'ascii', 'latin-1'])  # add more encodings per your needs
        else:
            self.skipTest(f"{self.txt_path} not found.")

    def test_detect_encoding_failure(self):
        # simulate a file that can't be read (e.g., no read permission)
        # for simplicity, im using a nonexistent file
        encoding = detect_encoding("nonexistent.txt")
        self.assertEqual(encoding, 'utf-8')

if __name__ == "__main__":
    unittest.main()