from flask import Flask, request, send_file, jsonify
import os
import openai
import json
import sqlite3
from PIL import Image
import pytesseract
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import subprocess

app = Flask(__name__)

# Set OpenAI API key and base URL
openai.api_key = os.getenv("AIPROXY_TOKEN")
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"


# Task A1: Install uv and run datagen.py with user email
def task_a1(user_email):
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(["python3", "/usr/src/app/datagen.py", user_email], check=True)


# Task A2: Format file using Prettier
def task_a2():
    subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True)


# Task A3: Count Wednesdays in dates.txt
def task_a3():
    try:
        with open("/data/dates.txt", "r") as file:
            dates = file.readlines()
        wednesdays = sum(1 for date in dates if "Wednesday" in date)
        with open("/data/dates-wednesdays.txt", "w") as file:
            file.write(str(wednesdays))
    except Exception as e:
        print(f"Error in Task A3: {e}")


# Task A4: Sort contacts.json
def task_a4():
    try:
        with open("/data/contacts.json", "r") as file:
            contacts = json.load(file)
        contacts.sort(key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))
        with open("/data/contacts-sorted.json", "w") as file:
            json.dump(contacts, file, indent=4)
    except Exception as e:
        print(f"Error in Task A4: {e}")


# Task A5: Write first line of recent .log files
def task_a5():
    try:
        log_dir = "/data/logs"
        log_files = sorted(
            [f for f in os.listdir(log_dir) if f.endswith(".log")],
            key=lambda x: os.path.getmtime(os.path.join(log_dir, x)),
            reverse=True,
        )[:10]
        with open("/data/logs-recent.txt", "w") as file:
            for log_file in log_files:
                with open(os.path.join(log_dir, log_file), "r") as log:
                    file.write(log.readline())
    except Exception as e:
        print(f"Error in Task A5: {e}")


# Task A6: Create index.json for Markdown files
def task_a6():
    try:
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
    except Exception as e:
        print(f"Error in Task A6: {e}")


# Task A7: Extract Sender's Email Address
def extract_email_address(content):
    messages = [
        {"role": "system", "content": "Extract the sender's email address."},
        {"role": "user", "content": f"Extract the sender's email from:\n\n{content}"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", messages=messages, max_tokens=50, temperature=0
    )
    return response.choices[0]["message"]["content"].strip()


def task_a7():
    try:
        with open("/data/email.txt", "r") as file:
            email_content = file.read()
        sender_email = extract_email_address(email_content)
        with open("/data/email-sender.txt", "w") as file:
            file.write(sender_email)
    except Exception as e:
        print(f"Error in Task A7: {e}")


# Task A8: Extract Credit Card Number
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def task_a8():
    try:
        text = extract_text_from_image("/data/credit_card.png")
        with open("/data/credit_card.txt", "w") as file:
            file.write(text.strip().replace(" ", ""))
    except Exception as e:
        print(f"Error in Task A8: {e}")


# Task A9: Find Most Similar Comments
def get_embeddings(text_list):
    embeddings = []
    for text in text_list:
        response = openai.Embedding.create(
            model="text-embedding-3-small", input=[text]
        )
        embeddings.append(response["data"][0]["embedding"])
    return embeddings


def task_a9():
    try:
        with open("/data/comments.txt", "r") as file:
            comments = [line.strip() for line in file.readlines()]
        embeddings = get_embeddings(comments)
        similarities = cosine_similarity(embeddings)
        np.fill_diagonal(similarities, 0)
        max_sim_index = np.unravel_index(np.argmax(similarities), similarities.shape)
        with open("/data/comments-similar.txt", "w") as file:
            file.write(comments[max_sim_index[0]] + "\n")
            file.write(comments[max_sim_index[1]] + "\n")
    except Exception as e:
        print(f"Error in Task A9: {e}")


# Task A10: Calculate Total Sales for Gold Ticket Type
def calculate_total_sales(db_path, ticket_type, output_filepath):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = ?", (ticket_type,))
        total_sales = cursor.fetchone()[0] or 0
        with open(output_filepath, "w") as file:
            file.write(str(total_sales))
    except Exception as e:
        print(f"Error in Task A10: {e}")
    finally:
        conn.close()


def task_a10():
    calculate_total_sales("/data/ticket-sales.db", "Gold", "/data/ticket-sales-gold.txt")


# Run Task Based on Description
@app.route("/run-task", methods=["POST"])
def run_task():
    try:
        task_description = request.json.get("task_description", "").lower()

        tasks = {
            "format": task_a2,
            "count wednesdays": task_a3,
            "sort contacts": task_a4,
            "recent logs": task_a5,
            "index markdown": task_a6,
            "extract email": task_a7,
            "extract credit card": task_a8,
            "find similar comments": task_a9,
            "total sales gold": task_a10,
        }

        for key, func in tasks.items():
            if key in task_description:
                func()
                return jsonify({"message": f"Task '{key}' executed successfully"}), 200

        if "install" in task_description and "datagen.py" in task_description:
            user_email = task_description.split("with ")[-1].strip()
            task_a1(user_email)
            return jsonify({"message": "Installed uv and ran datagen.py"}), 200

        return jsonify({"error": "Task not recognized"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
