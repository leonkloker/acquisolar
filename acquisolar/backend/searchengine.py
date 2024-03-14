import openai
import os
import os.path
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

from llama_index.llms.openai import OpenAI

# API keys
os.environ["OPENAI_API_KEY"] = "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"
os.environ["REPLICATE_API_TOKEN"] = "r8_JGumNCYSrS3ikipf7vqjvSTLyfYiWtp3cxYjo"

# LLM
""" LLM = Replicate(
    model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
    is_chat_model=False
) """
LLM = OpenAI(temperature=0, model='gpt-3.5-turbo')

# Service context
SERVICE_CONTEXT = ServiceContext.from_defaults(chunk_size=1024, llm=LLM)
SYNTH = get_response_synthesizer(streaming=True)

# Loaders
#loader = download_loader("PDFMinerReader")
#loader = download_loader("UnstructuredReader")

def query(text, index_dir = './index_storage', generator=False, filenames=[]):
    if not os.path.exists(index_dir):
        response = LLM.complete(text).text
        return response, [], [], []

    query_engine = get_query_engine(index_dir, filenames)

    response = query_engine.query(text)
    response_gen = response.response_gen
    source_nodes = response.source_nodes
    source_texts = [source_node.node.text for source_node in source_nodes]
    source_pages = [source_node.node.metadata["page_label"] for source_node in source_nodes]
    source_docs = [source_node.node.metadata["file_path"] for source_node in source_nodes]
    source_docs = ["/".join(doc.split("/")[-2:]) for doc in source_docs]

    if not generator:
        response_gen = "".join(list(response_gen))

    return response_gen, source_texts, source_pages, source_docs

def get_query_engine(index_dir = './index_storage', filenames=[]):
    # load the existing storage
    vector_storage_context = StorageContext.from_defaults(persist_dir=index_dir)

    # load the index from storage
    vector_index = load_index_from_storage(vector_storage_context, service_context=SERVICE_CONTEXT)

    query_engine = vector_index.as_query_engine(similarity_top_k=3, response_mode='compact', streaming=True)

    return query_engine

def index(doc_dir='./documents', index_dir='./index_storage'):
    if not os.path.exists(doc_dir):
        return "Directory does not exist"
    
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    
    # load the documents and create the index
    documents = SimpleDirectoryReader(doc_dir, recursive=True).load_data() #file_extractor={'.pdf': loader()}, recursive=True).load_data()

    vector_index = VectorStoreIndex.from_documents(documents, service_context=SERVICE_CONTEXT)

    # store it for later
    vector_index.storage_context.persist(persist_dir=index_dir)

    return "Index created"

def delete_documents(doc_names, index_dir='./index_storage'):
    if not os.path.exists(index_dir):
        return "Index does not exist"
    
    # load the existing storage
    vector_storage_context = StorageContext.from_defaults(persist_dir=index_dir)

    # load the index from storage
    vector_index = load_index_from_storage(vector_storage_context, service_context=SERVICE_CONTEXT)

    # remove the document from the index
    for idx_id, idx_name in vector_index.docstore.items():
        for doc_name in doc_names:
            if idx_name in doc_name:
                vector_index.remove_documents(idx_id)
                break

    # store it for later
    vector_index.storage_context.persist(persist_dir=index_dir)

    return "Documents removed from index"

def add_documents(doc_paths, index_dir='./index_storage'):
    if not os.path.exists(index_dir):
        return "Index does not exist"
    
    # load the existing storage
    vector_storage_context = StorageContext.from_defaults(persist_dir=index_dir)

    # load the index from storage
    vector_index = load_index_from_storage(vector_storage_context, service_context=SERVICE_CONTEXT)

    # load the documents and create the index
    new_index = SimpleDirectoryReader(input_files=doc_paths, recursive=False).load_data()

    for idx in new_index:
        vector_index.insert(idx)

    # store it for later
    vector_index.storage_context.persist(persist_dir=index_dir)

    return "Documents added to index"
