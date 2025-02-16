import datetime

def parse_date(date_str):
    """Try to parse the date string using multiple formats"""
    formats = [
        "%Y-%m-%d",
        "%d-%b-%Y",
        "%Y/%m/%d %H:%M:%S",
        "%b %d, %Y"
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Date format not recognized: {date_str}")

def count_wednesdays_in_file(input_filepath, output_filepath):
    """Count the number of Wednesdays in the input file and write the count to the output file"""
    try:
        with open(input_filepath, 'r') as file:
            dates = file.readlines()

        wednesday_count = 0
        for date_str in dates:
            date_str = date_str.strip()  # Remove any leading/trailing whitespace
            if date_str:
                date_obj = parse_date(date_str)
                if date_obj.weekday() == 2:  # 0 = Monday, 1 = Tuesday, 2 = Wednesday, ...
                    wednesday_count += 1

        with open(output_filepath, 'w') as file:
            file.write(str(wednesday_count))

        print(f"Count of Wednesdays: {wednesday_count}")

    except Exception as e:
        print(f"An error occurred: {e}")

def task_a3():
    input_filepath = "/data/dates.txt"
    output_filepath = "/data/dates-wednesdays.txt"
    count_wednesdays_in_file(input_filepath, output_filepath)

if __name__ == "__main__":
    task_a3()
