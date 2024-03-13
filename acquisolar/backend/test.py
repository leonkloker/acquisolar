import searchengine
import server
import sys
import classification
doc_dir = 'test_doc_dir'
index_dir = 'test_index_dir'
query = 'Is there a description of company interconnection facilities?'
add_doc_paths = ['2014-0359 (PPA on p37).pdf']

#searchengine.index(doc_dir=doc_dir, index_dir=index_dir)
#searchengine.add_documents(add_doc_paths, index_dir)
#searchengine.delete_documents(add_doc_paths, index_dir)
#response, source, pages, docs = searchengine.query(query, index_dir=index_dir, generator=False)
#classification.find_and_create_zip_structure('preferences', 'structured_data', 'project')
#classification.generate_directory_json('structured_data', 'project', 'documents')
print(server.calculate_folders())












