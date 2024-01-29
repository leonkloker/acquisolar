from model_api import *

A_FANTASTIC_ROLE = "Document analyser"
PROMPT ='''
        TO BE FILLED OUT
        '''


def main():
    print(f"\nStarting conversation with {A_FANTASTIC_ROLE} (ChatGPT)")
    print("Type 'Bye!' to end the conversation")
    print("--------------------------------------\n")
    conversation = []
    get_response(PROMPT, conversation)
    print(f"{A_FANTASTIC_ROLE}: ", conversation[-1].content)
    while True:
        message = input("You: ")
        if message == "Bye!":
            break
        get_response(message, conversation)
        # save_conversation(conversation, filename = "prompted_conversation.txt")
        print(f"{A_FANTASTIC_ROLE}: ", conversation[-1].content)
        

if __name__=="__main__":
    main()