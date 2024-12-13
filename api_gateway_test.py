import requests
import json

# API Gateway URL
url = "<enter-invoke-url-here>/generate-meal-plan"

# Headers to indicate the content type is JSON
headers = {
    "Content-Type": "application/json"
}

# Body content as a JSON string, similar to your Lambda test
body = {
    "userInput": "What should I eat for breakfast?",
    "conversationHistory": [
        #{"role": "system", "content": "You are a helpful meal prep assistant."}
    ]
}

# Make the POST request to the API Gateway endpoint
response = requests.post(url, headers=headers, data=json.dumps(body))

# Print the response status code and the JSON response from Lambda (API Gateway)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
