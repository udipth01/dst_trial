import subprocess
import os

def format_file_with_prettier(filepath):
    """Format the file with Prettier"""
    command = f"prettier --write {filepath}"
    subprocess.run(command, shell=True, check=True)

def task_a2():
    filepath = "/data/format.md"
    # Ensure the file exists
    if os.path.exists(filepath):
        format_file_with_prettier(filepath)
    else:
        print(f"File {filepath} does not exist")

if __name__ == "__main__":
    task_a2()
