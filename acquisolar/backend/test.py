import searchengine
import server
#import classification

search_query = "Is the letter of intent exclusive?"

response = searchengine.query(search_query, './index_storage')

print(response)










