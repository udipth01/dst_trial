import os
import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_embeddings(text_list):
    """Use GPT-4o-Mini to get embeddings for a list of texts"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
    
    embeddings = []
    for text in text_list:
        response = openai.Embedding.create(
            model="text-embedding-3-small",
            input=[text]
        )
        embeddings.append(response['data'][0]['embedding'])
    
    return embeddings

def task_a9():
    input_filepath = "/data/comments.txt"
    output_filepath = "/data/comments-similar.txt"

    try:
        # Read comments from the file
        with open(input_filepath, 'r') as file:
            comments = [line.strip() for line in file.readlines()]

        # Generate embeddings for the comments
        embeddings = get_embeddings(comments)

        # Calculate similarity between each pair of comment embeddings
        similarities = cosine_similarity(embeddings)
        np.fill_diagonal(similarities, 0)  # Remove self-similarity

        # Find the indices of the most similar pair of comments
        max_sim_index = np.unravel_index(np.argmax(similarities, axis=None), similarities.shape)
        most_similar_pair = (comments[max_sim_index[0]], comments[max_sim_index[1]])

        # Write the most similar pair of comments to the output file
        with open(output_filepath, 'w') as file:
            file.write(most_similar_pair[0] + '\n')
            file.write(most_similar_pair[1] + '\n')

        print(f"The most similar pair of comments have been written to {output_filepath}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    task_a9()
