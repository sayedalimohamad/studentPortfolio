from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Initialize the QA pipeline
qa_pipeline = pipeline(
    "question-answering", model="distilbert-base-cased-distilled-squad"
)

# Set the path to the knowledge base file
knowledge_base_path = "services/knowledge_base.json"

# Check if the knowledge base file exists
if not os.path.exists(knowledge_base_path):
    raise FileNotFoundError(
        f"The knowledge base file '{knowledge_base_path}' was not found."
    )

# Load the knowledge base from the JSON file with UTF-8 encoding
with open(knowledge_base_path, "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)


def retrieve_relevant_context(
    question: str,
    knowledge_base: list,
    top_k: int = 1,
    similarity_threshold: float = 0.2,
) -> tuple:
    """
    Retrieves the most relevant context from the knowledge base for a given question.

    Args:
        question (str): The question to retrieve context for.
        knowledge_base (list): A list of documents or facts.
        top_k (int): The number of top contexts to retrieve.
        similarity_threshold (float): The minimum similarity score for a context to be considered relevant.

    Returns:
        tuple: A tuple containing:
            - The most relevant context (or a fallback message if no relevant context is found).
            - A list of nearby topics (top N similar contexts).
    """
    # Use TF-IDF to find the most relevant context
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(knowledge_base + [question])
    question_vector = tfidf_matrix[-1]  # The last vector is the question
    context_vectors = tfidf_matrix[:-1]  # The rest are the knowledge base contexts

    # Compute cosine similarity between the question and each context
    similarities = cosine_similarity(question_vector, context_vectors).flatten()

    # Get the indices of the top N most similar contexts
    top_indices = similarities.argsort()[-top_k:][::-1]
    most_relevant_index = top_indices[0]
    most_relevant_similarity = similarities[most_relevant_index]

    # Check if the similarity score meets the threshold
    if most_relevant_similarity < similarity_threshold:
        # Retrieve the top N nearby topics
        nearby_topics = [knowledge_base[i] for i in top_indices]
        return "I don't have enough information to answer that question.", nearby_topics
    return knowledge_base[most_relevant_index], []


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


def find_similar_questions(
    question: str, knowledge_base: list, max_recommendations: int = 5
) -> list:
    """
    Finds similar questions or topics by splitting the question into words and comparing them to the knowledge base.

    Args:
        question (str): The question to find similar topics for.
        knowledge_base (list): A list of documents or facts.
        max_recommendations (int): The maximum number of recommendations to return.

    Returns:
        list: A list of recommended topics (up to max_recommendations).
    """
    # Split the question into words
    question_words = question.lower().split()

    # Use TF-IDF to find similar topics
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(knowledge_base + [" ".join(question_words)])
    question_vector = tfidf_matrix[-1]  # The last vector is the question
    context_vectors = tfidf_matrix[:-1]  # The rest are the knowledge base contexts

    # Compute cosine similarity between the question and each context
    similarities = cosine_similarity(question_vector, context_vectors).flatten()

    # Get the indices of the top N most similar contexts
    top_indices = similarities.argsort()[-max_recommendations:][::-1]
    similar_topics = [knowledge_base[i] for i in top_indices if similarities[i] > 0]

    return similar_topics


def ask_ai(question: str) -> str:
    """
    Sends a question to the AI and returns the response.

    Args:
        question (str): The question to ask the AI.

    Returns:
        str: The AI's response.
    """
    try:
        # Retrieve the most relevant context and nearby topics from the knowledge base
        full_context, nearby_topics = retrieve_relevant_context(
            question, knowledge_base
        )

        # If no relevant context is found, suggest nearby topics
        if full_context == "I don't have enough information to answer that question.":
            if nearby_topics:
                response = (
                    f"{full_context}\n\n"
                    f"Here are some topics that might be related to your question:\n"
                )
                for i, topic in enumerate(nearby_topics, 1):
                    response += f"{i}. {topic}\n"
                return response
            else:
                return full_context

        # Use the QA pipeline to get an answer
        result = qa_pipeline(question=question, context=full_context)
        raw_answer = result["answer"]

        # Make the response more friendly and include the full context
        friendly_answer = make_response_friendly(raw_answer, full_context)

        # Find similar questions or topics based on the question words
        similar_topics = find_similar_questions(
            question, knowledge_base, max_recommendations=5
        )
        if similar_topics:
            # Exclude the current context from the recommended topics
            similar_topics = [
                topic for topic in similar_topics if topic != full_context
            ]
            if similar_topics:  # Check if there are still topics to recommend
                friendly_answer += (
                    "\n\nHere are some recommended topics based on your question:\n"
                )
                for i, topic in enumerate(similar_topics, 1):
                    friendly_answer += f"{i}. {topic}\n"

        return friendly_answer
    except Exception as e:
        print(f"Error in AI service: {e}")
        return "Sorry, I couldn't process your request."
