import requests

# Define the URL of the Flask route
url = "http://127.0.0.1:5000/api/ask"

# Define the headers (set Content-Type to application/json)
headers = {
    "Content-Type": "application/json"
}

# Define the JSON payload
payload = {
    "question": "What is the capital of France?"
}

try:
    # Send the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Raise an exception for HTTP errors (4xx or 5xx)
    response.raise_for_status()

    # Print the response status code and JSON content
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

except requests.exceptions.HTTPError as err:
    # Handle HTTP errors (e.g., 400, 404, 500)
    print(f"HTTP Error: {err}")
except requests.exceptions.RequestException as err:
    # Handle other request-related errors (e.g., connection errors)
    print(f"Request Error: {err}")