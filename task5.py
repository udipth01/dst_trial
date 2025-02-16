import os

def get_first_line_of_file(filepath):
    """Read the first line of the given file"""
    with open(filepath, 'r') as file:
        return file.readline().strip()

def task_a5():
    log_directory = "/data/logs/"
    output_filepath = "/data/logs-recent.txt"

    try:
        # List all .log files in the directory
        log_files = [os.path.join(log_directory, f) for f in os.listdir(log_directory) if f.endswith('.log')]

        # Sort the files by modification time, most recent first
        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # Get the first line of the 10 most recent .log files
        recent_lines = []
        for log_file in log_files[:10]:
            first_line = get_first_line_of_file(log_file)
            recent_lines.append(first_line)

        # Write the first lines to the output file
        with open(output_filepath, 'w') as output_file:
            for line in recent_lines:
                output_file.write(line + '\n')

        print(f"The first lines of the 10 most recent .log files have been written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    task_a5()
