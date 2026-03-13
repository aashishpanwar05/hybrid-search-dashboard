import argparse
import json
import os
from datetime import datetime
from pathlib import Path

def ingest_documents(input_dir, output_dir):
    """
    Ingest documents from input directory and save as JSONL.

    Args:
        input_dir: Path to input directory containing .txt and .md files
        output_dir: Path to output directory for JSONL file
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / 'ingested.jsonl'

    with open(output_file, 'w', encoding='utf-8') as f:
        for txt_file in input_path.rglob('*.txt'):
            process_file(txt_file, f)
        for md_file in input_path.rglob('*.md'):
            process_file(md_file, f)

    print(f"Ingestion complete. Output saved to {output_file}")

def process_file(file_path, output_file):
    """
    Process a single file and write to JSONL.

    Args:
        file_path: Path to the file
        output_file: Open file handle for JSONL output
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Generate doc_id from relative path
        relative_path = file_path.relative_to(file_path.parents[-2])  # Assuming input_dir is data/raw
        doc_id = str(relative_path).replace('/', '_').replace('\\', '_')

        # Title from filename without extension
        title = file_path.stem

        # Source as string path
        source = str(file_path)

        # Created_at from file modification time
        created_at = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()

        doc = {
            'doc_id': doc_id,
            'title': title,
            'text': text,
            'source': source,
            'created_at': created_at
        }

        json.dump(doc, output_file, ensure_ascii=False)
        output_file.write('\n')

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents from folder to JSONL")
    parser.add_argument('--input', required=True, help='Input directory containing .txt and .md files')
    parser.add_argument('--out', required=True, help='Output directory for JSONL file')

    args = parser.parse_args()
    ingest_documents(args.input, args.out)
