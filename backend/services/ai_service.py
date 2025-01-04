from openai import OpenAI
from config import Config
from functools import lru_cache
from typing import Optional

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

@lru_cache(maxsize=100)  # Cache responses to reduce API calls
def ask_ai(question: str) -> str:
    """
    Sends a question to the OpenAI API and returns the response.

    Args:
        question (str): The question to ask the AI.

    Returns:
        str: The AI's response.
    """
    try:
        response = client.completions.create(
            model="text-davinci-003",  # Use the new `model` parameter
            prompt=question,
            max_tokens=150,  # Limit the response length
            temperature=0.7,  # Control creativity (0 = deterministic, 1 = creative)
        )
        return response.choices[0].text.strip()
    except Exception as e:
        # Log the error for debugging
        print(f"Error in AI service: {e}")
        return "Sorry, I couldn't process your request."


def get_learning_recommendations(user_id: int) -> Optional[str]:
    """
    Generates personalized learning recommendations based on user data.

    Args:
        user_id (int): The ID of the user for whom recommendations are generated.

    Returns:
        Optional[str]: The AI-generated recommendations, or None if an error occurs.
    """
    try:
        # Fetch user data from the database (e.g., skills, interests, etc.)
        # For now, we'll use a placeholder prompt.
        prompt = f"Generate learning recommendations for user {user_id} based on their portfolio."
        response = client.completions.create(
            model="text-davinci-003",  # Use the new `model` parameter
            prompt=prompt,
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        # Log the error for debugging
        print(f"Error in AI service: {e}")
        return None