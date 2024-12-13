import os
import json
from openai import OpenAI


# Initialize OpenAI client using environment variables
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    organization=os.environ["OPENAI_ORGANIZATION_KEY"],
)

def chatgpt_chatbot(messages, model):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    answer = completion.choices[0].message.content.strip()
    return answer
MAX_HISTORY_LENGTH = 7
def lambda_handler(event, context):
    """
    AWS Lambda handler to process user input and generate a response from GPT-4.
    """
    try:
        # Parse the incoming HTTP POST request body
        body = json.loads(event["body"])
        user_input = body.get("userInput", "")  # Expecting 'userInput' in the JSON payload

        if not user_input:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "User input is required."})
            }

        # Get the conversation history from the incoming request
        conversation_history = body.get("conversationHistory", [])
        
        # If conversation history is empty, initialize it with a system message
        if not conversation_history:
            conversation_history = [
                {"role": "system", "content": "You are a helpful meal prep assistant."},
            ]
        if len(conversation_history) > MAX_HISTORY_LENGTH:
            conversation_history = conversation_history[-MAX_HISTORY_LENGTH:]    

        # Add the new user input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Call the GPT-4 model to get a response based on the conversation history
        response = chatgpt_chatbot(conversation_history, model="gpt-4o")

        # Add GPT-4's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})

        # Return the generated response and updated conversation history to the client
        return {
            "statusCode": 200,
            "body": json.dumps({
                "meal_plan": response# Updated conversation history
            })
        }
    
    except Exception as e:
        # Handle any errors and return a 500 response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
