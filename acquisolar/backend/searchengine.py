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

#from llama_index.llms import OpenAI, Replicate
from llama_index.llms.openai import OpenAI
#from llama_index.query_engine import RouterQueryEngine, RetrieverQueryEngine, CitationQueryEngine

"""
from llama_index.tools import (
    QueryEngineTool,
    ToolMetadata,
)
from llama_index.response.notebook_utils import display_response
from llama_index.prompts import PromptTemplate
"""

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

def query(text, index_dir = './index_storage'):
    if not os.path.exists(index_dir):
        return "Index does not exist"

    # load the existing storage
    vector_storage_context = StorageContext.from_defaults(persist_dir=index_dir)

    # load the index from storage
    vector_index = load_index_from_storage(vector_storage_context, service_context=SERVICE_CONTEXT)

    """ # either way we can now query the index
    vector_tool = QueryEngineTool(
        vector_index.as_query_engine(similarity_top_k=5, response_mode='compact', streaming=True),
        metadata=ToolMetadata(
            name="vector_search",
            description="Useful for searching for specific facts."
        )
    ) """

    """ summary_tool = QueryEngineTool(
        vector_index.as_query_engine(similarity_top_k=5, response_mode='tree_summarize', streaming=True),
        metadata=ToolMetadata(
            name="summary_search",
            description="Useful for searching for general summary information."
        )
    ) """
    
    """ query_engine = RouterQueryEngine.from_defaults(
        [vector_tool, summary_tool],
        service_context=SERVICE_CONTEXT,
        select_multi=True,
    ) """

    query_engine = vector_index.as_query_engine(similarity_top_k=3, response_mode='compact', streaming=True)

    """ query_engine = CitationQueryEngine.from_args(
        vector_index,
        similarity_top_k=3,
        citation_chunk_size=1024,
        streaming=True
    ) """

    response = query_engine.query(text)

    return response.response_gen, response.source_nodes

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
