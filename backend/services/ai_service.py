from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Initialize the QA pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Set the path to the knowledge base file
knowledge_base_path = "services/knowledge_base.json"

# Check if the knowledge base file exists
if not os.path.exists(knowledge_base_path):
    raise FileNotFoundError(f"The knowledge base file '{knowledge_base_path}' was not found.")

# Load the knowledge base from the JSON file with UTF-8 encoding
with open(knowledge_base_path, "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

def retrieve_relevant_context(question: str, knowledge_base: list, top_k: int = 1) -> str:
    """
    Retrieves the most relevant context from the knowledge base for a given question.

    Args:
        question (str): The question to retrieve context for.
        knowledge_base (list): A list of documents or facts.
        top_k (int): The number of top contexts to retrieve.

    Returns:
        str: The most relevant context.
    """
    # Use TF-IDF to find the most relevant context
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(knowledge_base + [question])
    question_vector = tfidf_matrix[-1]  # The last vector is the question
    context_vectors = tfidf_matrix[:-1]  # The rest are the knowledge base contexts

    # Compute cosine similarity between the question and each context
    similarities = cosine_similarity(question_vector, context_vectors).flatten()

    # Get the index of the most relevant context
    most_relevant_index = similarities.argsort()[-top_k:][::-1][0]
    return knowledge_base[most_relevant_index]

def make_response_friendly(answer: str, full_context: str) -> str:
    """
    Makes the AI's response more friendly and includes the full context.

    Args:
        answer (str): The raw answer from the AI.
        full_context (str): The full context from the knowledge base.

    Returns:
        str: A friendly version of the answer with full context.
    """
    # Add a friendly prefix and include the full context
    friendly_response = (
        f"Sure! Here's what I found: {answer}.\n\n"
        f"Here's the full information:\n{full_context}"
    )
    return friendly_response

def ask_ai(question: str) -> str:
    """
    Sends a question to the AI and returns the response.

    Args:
        question (str): The question to ask the AI.

    Returns:
        str: The AI's response.
    """
    try:
        # Retrieve the most relevant context from the knowledge base
        full_context = retrieve_relevant_context(question, knowledge_base)

        # Use the QA pipeline to get an answer
        result = qa_pipeline(question=question, context=full_context)
        raw_answer = result["answer"]

        # Make the response more friendly and include the full context
        friendly_answer = make_response_friendly(raw_answer, full_context)
        return friendly_answer
    except Exception as e:
        print(f"Error in AI service: {e}")
        return "Sorry, I couldn't process your request."