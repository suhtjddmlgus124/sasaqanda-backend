import os
import dotenv
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
dotenv.load_dotenv()

API_KEY = os.getenv("GPT_API_KEY")

def call_gpt_api(content):
    client = openai.OpenAI(api_key=API_KEY)
    response = client.embeddings.create(
        input=[content],
        model="text-embedding-ada-002",
    )
    return response.data[0].embedding


def get_most_similar_question(question_queryset, target_vector):
    vectors = np.array([np.array(q.vector) for q in question_queryset])
    similartities = cosine_similarity([target_vector], vectors)
    max_index = similartities.argmax()
    return question_queryset[max_index]