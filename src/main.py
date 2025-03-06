# src/main.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import logging
from src.metadata import extract_metadata, display_metadata

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/metadata.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """main function to run the metadata extractor CLI"""
    parser = argparse.ArgumentParser(description="extract metadata from a dataset file.")
    parser.add_argument("file", help="path to the file (e.g., data.csv, data.xlsx)")
    parser.add_argument("--chunk-size", type=int, default=1000, help="number of rows to sample for large files")
    args = parser.parse_args()

    # validation
    if not os.path.exists(args.file):
        logger.error(f"File '{args.file}' not found.")
        return

    # extract metadata
    try:
        metadata = extract_metadata(args.file, chunk_size=args.chunk_size)
        display_metadata(metadata)
    except Exception as e:
        logger.error(f"failed to process file: {str(e)}")

if __name__ == "__main__":
    main()