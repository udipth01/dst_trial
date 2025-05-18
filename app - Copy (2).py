from flask import Flask, request, jsonify, send_file
import os
import openai
import json
import sqlite3
from PIL import Image
import pytesseract
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Helper functions for tasks
def run_task(task_description):
    try:
        if "format" in task_description.lower() and "prettier" in task_description.lower():
            # Task A2: Format file using Prettier
            os.system("npx prettier@3.4.2 --write /usr/src/app/format.md")
            return "Formatted /usr/src/app/format.md using Prettier", 200
        elif "count wednesdays" in task_description.lower():
            # Task A3: Count Wednesdays in dates.txt
            with open("/data/dat.txt", "r") as file:
                dates = file.readlines()
            wednesdays = sum(1 for date in dates if "Wednesday" in date)
            with open("/data/dates-wednesdays.txt", "w") as file:
                file.write(str(wednesdays))
            return f"Counted {wednesdays} Wednesdays in /data/dates.txt", 200
        elif "sort contacts" in task_description.lower():
            # Task A4: Sort contacts.json
            with open("/data/contacts.json", "r") as file:
                contacts = json.load(file)
            contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
            with open("/data/contacts-sorted.json", "w") as file:
                json.dump(contacts, file, indent=4)
            return "Sorted contacts and written to /data/contacts-sorted.json", 200
        elif "recent logs" in task_description.lower():
            # Task A5: Write first line of recent .log files
            log_files = sorted([f for f in os.listdir("/data/logs") if f.endswith(".log")], key=lambda x: os.path.getmtime(f"/data/logs/{x}"), reverse=True)[:10]
            with open("/data/logs-recent.txt", "w") as file:
                for log_file in log_files:
                    with open(f"/data/logs/{log_file}", "r") as log:
                        file.write(log.readline())
            return "Written first line of 10 most recent .log files to /data/logs-recent.txt", 200
        elif "index markdown" in task_description.lower():
            # Task A6: Create index.json for Markdown files
            index = {}
            for root, _, files in os.walk("/data/docs"):
                for file in files:
                    if file.endswith(".md"):
                        with open(os.path.join(root, file), "r") as md_file:
                            for line in md_file:
                                if line.startswith("# "):
                                    index[file] = line.strip("# ").strip()
                                    break
            with open("/data/docs/index.json", "w") as file:
                json.dump(index, file, indent=4)
            return "Created index.json for Markdown files in /data/docs", 200
        elif "extract email" in task_description.lower():
            # Task A7: Extract sender's email address from email.txt
            with open("/data/email.txt", "r") as file:
                email_content = file.read()
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Extract the sender's email address from this email:\n\n{email_content}"}
                ]
            )
            sender_email = response.choices[0].message['content'].strip()
            with open("/data/email-sender.txt", "w") as file:
                file.write(sender_email)
            return "Extracted sender's email address and written to /data/email-sender.txt", 200
        elif "extract credit card" in task_description.lower():
            # Task A8: Extract credit card number from credit-card.png
            image = Image.open("/data/credit_card.png")
            text = pytesseract.image_to_string(image)
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Extract the credit card number from this text:\n\n{text}"}
                ]
            )
            credit_card_number = response.choices[0].message['content'].strip().replace(" ", "")
            with open("/data/credit-card.txt", "w") as file:
                file.write(credit_card_number)
            return "Extracted credit card number and written to /data/credit-card.txt", 200
        elif "find similar comments" in task_description.lower():
            # Task A9: Find the most similar pair of comments
            with open("/data/comments.txt", "r") as file:
                comments = file.readlines()
            embeddings = [openai.Embedding.create(model="text-embedding-3-small", input=[comment])["data"][0]["embedding"] for comment in comments]
            similarities = cosine_similarity(embeddings)
            np.fill_diagonal(similarities, -np.inf)
            most_similar_pair = np.unravel_index(np.argmax(similarities), similarities.shape)
            with open("/data/comments-similar.txt", "w") as file:
                file.write(comments[most_similar_pair[0]])
                file.write(comments[most_similar_pair[1]])
            return "Found most similar comments and written to /data/comments-similar.txt", 200
        elif "total sales gold" in task_description.lower():
            # Task A10: Calculate total sales for Gold ticket type
            conn = sqlite3.connect("/data/ticket-sales.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
            total_sales = cursor.fetchone()[0]
            with open("/data/ticket-sales-gold.txt", "w") as file:
                file.write(str(total_sales))
            conn.close()
            return f"Total sales for Gold ticket type: {total_sales}", 200
        else:
            return "Task description not recognized or not supported", 400
    except Exception as e:
        return str(e), 500

@app.route('/run', methods=['POST'])
def run():
    task_description = request.args.get('task')
    if not task_description:
        return "Task description is required", 400
    result, status_code = run_task(task_description)
    return result, status_code

@app.route('/read', methods=['GET'])
def read():
    path = request.args.get('path')
    if not path:
        return "File path is required", 400
    try:
        return send_file(path)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
