import searchengine

index_dir = './storage'
query = "What is a brief summary of the interconnection agreement?"
response = searchengine.query(query, index_dir)
print(str(response))


