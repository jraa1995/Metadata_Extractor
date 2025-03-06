import unittest
import os
from src.metadata import extract_metadata

class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.csv_path = "data/sample.csv"
        self.xlsx_path = "data/sample.xlsx"
        self.txt_path = "data/sample.txt"

    def test_csv_extraction(self):
        if os.path.exists(self.csv_path):
            metadata = extract_metadata(self.csv_path)
            self.assertIn("column_names", metadata)
            self.assertGreater(metadata["columns"], 0)
            self.assertFalse("error" in metadata)
        else:
            self.skipTest(f"{self.csv_path} not found.")

    def test_xlsx_extraction(self):
        if os.path.exists(self.xlsx_path):
            metadata = extract_metadata(self.xlsx_path)
            self.assertIn("column_names", metadata)
            self.assertGreater(metadata["columns"], 0)
            self.assertFalse("error" in metadata)
        else:
            self.skipTest(f"{self.xlsx_path} not found.")

    def test_unsupported_file(self):
        if os.path.exists(self.txt_path):
            metadata = extract_metadata(self.txt_path)
            self.assertIn("line_count", metadata)
            self.assertIn("note", metadata)
            self.assertFalse("error" in metadata)
        else:
            self.skipTest(f"{self.txt_path} not found.")

    def test_nonexistent_file(self):
        metadata = extract_metadata("nonexistent.file")
        self.assertIn("error", metadata)
        self.assertEqual(metadata["error"], "permission denied.")  # will vary per os

if __name__ == "__main__":
    unittest.main()