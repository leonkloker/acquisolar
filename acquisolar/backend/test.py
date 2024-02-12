import searchengine

index_dir = './index_storage'
query = "What is a brief summary of the interconnection agreement?"
response_gen, source = searchengine.query(query, index_dir)

for word in response_gen:
    print(word, end="", flush=True)





