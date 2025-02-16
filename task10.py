import sqlite3

def calculate_total_sales(db_path, ticket_type, output_filepath):
    """Calculate the total sales for a specific ticket type and write to a file"""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Run the SQL query to calculate total sales for the specified ticket type
        query = """
        SELECT SUM(units * price)
        FROM tickets
        WHERE type = ?
        """
        cursor.execute(query, (ticket_type,))
        total_sales = cursor.fetchone()[0]

        # Write the total sales to the output file
        with open(output_filepath, 'w') as file:
            file.write(str(total_sales))

        print(f"The total sales for {ticket_type} tickets have been written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

def task_a10():
    db_path = "/data/ticket-sales.db"
    ticket_type = "Gold"
    output_filepath = "/data/ticket-sales-gold.txt"
    calculate_total_sales(db_path, ticket_type, output_filepath)

if __name__ == "__main__":
    task_a10()
