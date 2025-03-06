import pandas as pd
import os
from pathlib import Path
import mimetypes
from datetime import datetime
import logging
from src.utils import detect_encoding

logger = logging.getLogger(__name__)

def extract_metadata(file_path, chunk_size=1000):
    """extract metadata from a given file
    
    args:
        file_path: str, path to the file
        chunk_size: int, number of rows to sample for large files
        
    returns:    
        metadata: dict, metadata extracted from the file
    
    """
    
    metadata = {
        "file_path": file_path,
        "file_type": mimetypes.guess_type(file_path)[0] or "unknown",
        "file_size_bytes": os.path.getsize(file_path),
        "creation_time": datetime.fromtimestamp(Path(file_path).stat().st_birthtime).strftime('%Y-%m-%d %H:%M:%S'),
        "modification_time": datetime.fromtimestamp(Path(file_path).stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # validate file accessibility and emptiness
    if not os.access(file_path, os.R_OK):
        metadata["error"] = "permission denied"
        return metadata
    if metadata["file_size_bytes"] == 0:
        metadata["error"] = "empty file"
        return metadata
    
    # process based on the extension
    file_ext = file_path.lower().split(".")[-1]
    try:
        if file_ext == 'csv':
            encoding = detect_encoding(file_path)
            logger.info(f"Detected encoding for {file_path}: {encoding}")
            # Use chunks for large files
            chunk = next(pd.read_csv(file_path, chunksize=chunk_size, encoding=encoding))
            metadata["rows"] = "Estimated (use full analysis for exact count)"
            metadata["columns"] = chunk.shape[1]
            metadata["column_names"] = list(chunk.columns)
            metadata["data_types"] = chunk.dtypes.astype(str).to_dict()  # Convert dtypes to strings
            metadata["missing_values"] = chunk.isnull().sum().to_dict()
            metadata["sample_rows"] = chunk_size

        elif file_ext == 'xlsx':
            df = pd.read_excel(file_path, nrows=chunk_size)
            metadata["rows"] = "full count requires full load" if len(df) == chunk_size else len(df)
            metadata["columns"] = df.shape[1]
            metadata["column_names"] = list(df.columns)
            metadata["data_types"] = df.dtypes.astype(str).to_dict()
            metadata["missing_values"] = df.isnull().sum().to_dict()
            metadata["sample_rows"] = chunk_size

        else:
            metadata["note"] = f"unsupported file type: .{file_ext}"
            if metadata["file_type"].startswith("text"):
                with open(file_path, 'r', encoding=detect_encoding(file_path)) as f:
                    metadata["line_count"] = sum(1 for _ in f)

    except pd.errors.EmptyDataError:
        metadata["error"] = "file is empty or has no valid data"
    except pd.errors.ParserError:
        metadata["error"] = "file is malformed or not in expected format"
    except UnicodeDecodeError:
        metadata["error"] = "encoding issue detected; file may be corrupted"
    except Exception as e:
        metadata["error"] = f"processing failed: {str(e)}"

    return metadata

def display_metadata(metadata):
    """display metadata in a formatted way."""
    logger.info("\n=== Dataset Metadata ===")
    for key, value in metadata.items():
        logger.info(f"{key.replace('_', ' ').title()}: {value}")
    logger.info("=====================\n")