import openai
import os
import logging
import sys
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


"""Start: Metadata extraction imports and setup"""
from llama_index.node_parser import SentenceSplitter
from llama_index.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
    EntityExtractor,
)
from llama_index.ingestion import IngestionPipeline

transformations = [
    SentenceSplitter(),
    #TitleExtractor(nodes=5),
    QuestionsAnsweredExtractor(questions=3),
    #SummaryExtractor(summaries=["prev", "self"]),
    #KeywordExtractor(keywords=10),
    #EntityExtractor(prediction_threshold=0.5),
]
pipeline = IngestionPipeline(transformations=transformations)

"""End: Metadata extraction imports and setup"""


#logging to show what is happening under the hood
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # replace DEBUG with INFO for less output
#logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


#Select llm
#llm = OpenAI(model="gpt-4", temperature=0) # gpt 3.5 default
#service_context = ServiceContext.from_defaults(llm_predictor=llm)

# Change the working directory my local one
target_directory = r'C:\Users\MBAUser\AcquiSolar\magnus_searchengine'
os.chdir(target_directory)
print("Current working directory:", os.getcwd())


# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("./data").load_data()
    vector_index = VectorStoreIndex.from_documents(documents) # add service context if chatgpt 4
    # store it for later
    vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    vector_index = load_index_from_storage(storage_context)


query_engine = vector_index.as_query_engine(response_mode="compact")

# prompting
input_question = "When does this contract terminate?" #This is the variable we should be receiving from Zara

# output_locate is what you look up in the ctrl + F field
prompt_locate = "The GPT should find the text in the doucment that answers the following question. The GPT should not summarize the answer, it should state the most precise sentence in the document to provide the answer. It should state this word for word. It is important that this is precise. If the answer cannot be found, the GPT should not respond with anything"
output_locate = query_engine.query(prompt_locate+input_question)
print("This is what you should search for in the doucment:",output_locate)

# output_answer is the answer to the question
prompt_answer = "The GPT should output the answer in 3 sentences of the following quesiton: "
output_answer = query_engine.query(prompt_answer+input_question)
print("This is the answer to the question:", output_answer)

# output_summary is a summary of the document
prompt_summarize = "Summarize what type of document this is in 2 sentences"
output_summary = query_engine.query(prompt_summarize)
print("This is a summary of the document:", output_summary)

# name of the document that the answer was found in
# this does not work yet. because metadata is not saved yet. 
#It should be saved as documents are imported
#nodes = pipeline.run(documents=documents)
#print(nodes['document_title'])