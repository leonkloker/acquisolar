from constants import OPEN_AI_API_KEY, BASELINE_MESSAGES
import openai
from openai import OpenAI
client = OpenAI(
  api_key= OPEN_AI_API_KEY,
)
def clean_print(text):
    # remove starting and ending blank characters and quotes
    text.content = text.content.strip().strip('"')
    print("Content:\n", text.content)

def process_result(result, conversation = [], save = True):
    msg = result.choices[0].message
    if save:
        conversation.append(msg)
    return msg

def make_message(message, role = "user"):
    return {"role": role, "content": message}

def get_response(message, conversation = []):
    # Combine the previous conversation with the new message
    conversation.append(make_message(message))

    # Call OpenAI GPT-3.5 API to generate a response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )

    # Process the result and return the generated message

    return process_result(completion, conversation)

def save_conversation(conversation, filename = "output.txt"):
    with open(filename, "w") as f:
        for msg in conversation:
            f.write(msg["role"] + ": " + msg["content"] + "\n")
    

