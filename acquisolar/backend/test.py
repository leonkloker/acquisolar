import searchengine

index_dir = './index_storage'
query = "What is a brief summary of the interconnection agreement?"
response = searchengine.query(query, index_dir)
for word in response.response_gen:
    print(word, " ")


