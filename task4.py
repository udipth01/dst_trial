import json
import os

def sort_contacts(input_filepath, output_filepath):
    """Sort the contacts by last_name and first_name, and write the sorted list to the output file"""
    try:
        # Read contacts from the file
        with open(input_filepath, 'r') as file:
            contacts = json.load(file)

        # Sort the contacts by last_name and then by first_name
        sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

        # Write the sorted contacts to the output file
        with open(output_filepath, 'w') as file:
            json.dump(sorted_contacts, file, indent=4)

        print(f"Sorted contacts have been written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")

def task_a4():
    input_filepath = "/data/contacts.json"
    output_filepath = "/data/contacts-sorted.json"
    sort_contacts(input_filepath, output_filepath)

if __name__ == "__main__":
    task_a4()
