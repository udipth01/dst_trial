import os
import json

def extract_first_h1(filepath):
    """Extract the first H1 header from the given Markdown file"""
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('# '):
                return line.strip('# ').strip()
    return None

def task_a6():
    docs_directory = "/data/docs/"
    output_filepath = "/data/docs/index.json"

    try:
        index = {}
        # List all .md files in the directory
        md_files = [f for f in os.listdir(docs_directory) if f.endswith('.md')]

        # Extract the first H1 header from each file
        for md_file in md_files:
            filepath = os.path.join(docs_directory, md_file)
            title = extract_first_h1(filepath)
            if title:
                index[md_file] = title

        # Write the index to the output file
        with open(output_filepath, 'w') as output_file:
            json.dump(index, output_file, indent=4)

        print(f"The index file has been written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    task_a6()
