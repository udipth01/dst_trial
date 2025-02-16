import os
import openai

def extract_email_address(content):
    """Use GPT-4o-Mini to extract the sender's email address from the email content"""
    openai.api_key = os.getenv("AIPROXY_TOKEN")
    openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts the sender's email address from the email content."
        },
        {
            "role": "user",
            "content": f"Extract the sender's email address from the following email content:\n\n{content}\n\nThe sender's email address is:"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=50,
        temperature=0
    )

    # Extract the email address from the response
    email_address = response.choices[0].message['content'].strip()
    return email_address

def task_a7():
    input_filepath = "/data/email.txt"
    output_filepath = "/data/email-sender.txt"

    try:
        # Read the email content from the file
        with open(input_filepath, 'r') as file:
            email_content = file.read()

        # Extract the sender's email address using the LLM
        sender_email = extract_email_address(email_content)

        # Write the extracted email address to the output file
        with open(output_filepath, 'w') as file:
            file.write(sender_email)

        print(f"The sender's email address has been written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    task_a7()
