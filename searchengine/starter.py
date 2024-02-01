import openai
import os
import os.path
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
    SummaryIndex,
)
from llama_index.llms import OpenAI, Replicate
from llama_index.query_engine import RouterQueryEngine
from llama_index.tools import (
    QueryEngineTool,
    ToolMetadata,
)
from llama_index.response.notebook_utils import display_response
from llama_index.prompts import PromptTemplate

# check if storage already exists
PERSIST_DIR_ORIG = "./storage/orig"
PERSIST_DIR_SUM = "./storage/sum"

# define LLM to be used and its randomness
#llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
os.environ["REPLICATE_API_TOKEN"] = "r8_JGumNCYSrS3ikipf7vqjvSTLyfYiWtp3cxYjo"
llm = Replicate(
    model="meta/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
    is_chat_model=False
)

# define servicecontext
service_context = ServiceContext.from_defaults(chunk_size=1000, llm=llm)

# TODO if storage exists, index newly created documents and remove index for removed documents

if not os.path.exists(PERSIST_DIR_ORIG):
    # load the documents and create the index
    documents = SimpleDirectoryReader("data").load_data()
    summary_index = SummaryIndex.from_documents(documents, service_context=service_context)
    vector_index = VectorStoreIndex.from_documents(documents, service_context=service_context)

    # store it for later
    summary_index.storage_context.persist(persist_dir=PERSIST_DIR_SUM)
    vector_index.storage_context.persist(persist_dir=PERSIST_DIR_ORIG)
else:
    # load the existing storage
    summary_storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR_SUM)
    vector_storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR_ORIG)

    # load the index from storage
    summary_index = load_index_from_storage(summary_storage_context, service_context=service_context)
    vector_index = load_index_from_storage(vector_storage_context, service_context=service_context)

# either way we can now query the index
vector_tool = QueryEngineTool(
    vector_index.as_query_engine(similarity_top_k=2, response_mode='compact'),
    metadata=ToolMetadata(
        name="vector_search",
        description="Useful for searching for specific facts."
    )
)

summary_tool = QueryEngineTool(
    summary_index.as_query_engine(similarity_top_k=2, response_mode="tree_summarize"),
    metadata=ToolMetadata(
        name="summary",
        description="Useful for summarizing an entire document."
    )
)

query_engine = RouterQueryEngine.from_defaults(
    [vector_tool],#, summary_tool],
    service_context=service_context,
    select_multi=False,
)

response = query_engine.query("Give me a summary of Paul Graham")
print(response)
