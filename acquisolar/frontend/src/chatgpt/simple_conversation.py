from model_api import *

def main():
    print("\nStarting conversation with GPT-3.5 (ChatGPT)")
    print("Type 'Bye!' to end the conversation")
    print("--------------------------------------\n")
    conversation = []
    while True:
        message = input("You: ")
        if message == "Bye!":
            break
        get_response(message, conversation)
        #save_conversation(conversation, filename = "simple_conversation.txt")
        print("ChatGPT: ", conversation[-1].content)
        

if __name__=="__main__":
    main()