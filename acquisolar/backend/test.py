import searchengine
import server
import sys
import classification
import os

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
    Settings,
    SummaryIndex,
    get_response_synthesizer,
    download_loader
)

doc_dir = 'test_doc_dir'
index_dir = 'test_index_dir'
add_doc_paths = ['2014-0359 (PPA on p37).pdf']

query = {
  "query_str": ['Is there a description of company interconnection facilities?'],
  "filter": {
    "filename": "example_document.pdf"
  },
  "top_k": 10
}
#searchengine.index(doc_dir=doc_dir, index_dir=index_dir)
#searchengine.add_documents(add_doc_paths, index_dir)
#searchengine.delete_documents(add_doc_paths, index_dir)
searchengine.index(doc_dir, index_dir)
response, source, pages, docs = searchengine.query(query, index_dir=index_dir, generator=False,
                                                   filenames=["test.pdf"])

print(response)

