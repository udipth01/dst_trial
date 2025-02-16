import os
import openai
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    """Use OCR to extract text from an image"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_credit_card_number(content):
    """Use GPT-4o-Mini to extract the credit card number from the text content"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts the credit card number from text content."
        },
        {
            "role": "user",
            "content": f"Extract the credit card number from the following text content:\n\n{content}\n\nThe credit card number is:"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=50,
        temperature=0
    )

    # Extract the credit card number from the response
    credit_card_number = response.choices[0].message['content'].strip()
    return credit_card_number

def task_a8():
    image_filepath = "/data/credit_card.png"
    output_filepath = "/data/credit_card.txt"

    try:
        # Confirm the environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

        # Extract text from the image using OCR
        image_text = extract_text_from_image(image_filepath)

        # Extract the credit card number using the LLM
        credit_card_number = extract_credit_card_number(image_text)

        # Remove any spaces from the credit card number
        credit_card_number = credit_card_number.replace(" ", "")

        # Write the extracted credit card number to the output file
        with open(output_filepath, 'w') as file:
            file.write(credit_card_number)

        print(f"The credit card number has been written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    task_a8()
