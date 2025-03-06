# src/utils.py
import chardet
import logging

logger = logging.getLogger(__name__)

def detect_encoding(file_path):
    """
    detect the encoding of a text-based file
    
    args:
        file_path (str): Path to the file.
    
    returns:
        str: detected encoding (e.g., 'utf-8').
    """
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read(1024))
        encoding = result['encoding'] or 'utf-8' # will default to utf-8 if encoding fails
        return encoding
    except Exception as e:
        logger.warning(f"encoding detection failed for {file_path}: {str(e)}. defaulting to utf-8")
        return 'utf-8'