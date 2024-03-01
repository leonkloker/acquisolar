# AcquiSolar
## Summary Sprint 3

Leon:
* Familiarized with frontend engineering (especially using graphical design tools like Webflow) and hosting a frontend on e.g. an AWS S3 bucket using CI/CD frameworks. Helped Zara design the website.
* Hosting website, helping to clean up the UI and integrate with the backend, improve the performance of RAG for querying documents

Zara:
* Accomplished Sprint 3: Using Magnus' figma design to redevelop the website in a more accessible and professional way and worked on some backend functionality to improve user flow.
* Plan for Sprint 4: Finishing up this UI redesign and cleaning up code, allowing the backend to search more effectively through pdfs (temporarily not working because of redesign)

Jürgen:
* Accomplished Sprint 3: Setting up a structure to test and evaluate the sorting. Splitting up data-files, manually annotating them and looking for patterns and heuristics to feed into the prompt. Searching the web for alternative data sources and trying to generate some ourselves. 
* Plan for Sprint 4: Implement the insights from the data-research process into different versions of prompts and test them. Implement a multi dimensional prompt design to have more control over how the sorting performs. 

Magnus:
* Accomplished Sprint 3: Minor code adjustments to fit with the frontend. For instance altering functions to create the directory so you can view how files load. Did several interviews to understand directoin going forward. Attended a 2 day course on M&A to understand the process and what you look for in documents.
* Plan for Sprint 4: Setting up interviews to test the software. Create and test new visual prototypes with users.

## Summary Sprint 2

Setup instructions:
cd into backend

install necessary modules using pip install -r requirements.txt

run python server.py and copy url link and paste in URL

Magnus: 
* Accomplished in Sprint 2: created a visual mockup to guide further development. coded the pipeline from a document coming in, metadata and information being extracted, and the files being placed in a new folder structure. created functions to format directories for the frontend and move and rename files
* Plan for Sprint 3:
* set up calls to teat initial functionality with users. complete visual prototype. optimize summary and title generation

Leon: 
* Accomplished in Sprint 2: Connected backend to frontend with a python flask based backend. Decided on going with LlamaIndex for RAG. Implemented server endpoints for querying the vector database and streaming the response back to the frontend together with the sources, uploading documents to the backend, returning the folder structure and metadata after each document is processed, clasified and summarized. Looked into some UI development to help Zara. Set up an AWS instance to host the backend on a AWS server and the frontend on some frontend server for clearer separation and encapsulation for development.
* Plan for Sprint 3: Be even more involved in the frontend development. Optimize the document processing and query engine and keep track of which documents have already been indexed or summarized and which still have to be processed. Present the layout to interviewees to get feedback on layout and functionality.

Zara:
* Accomplished in Sprint 2: Integrated backend and frontend for file uploads and data retrieval in javascript that Leon converted to python. Implemented the UI side for displaying and allowing users to search for specific text in pdf documents. 4 screens file upload - search - suggested folder structure - folder contents look. Researching the best practices for secure and efficient file storage.  
* Plan for Sprint 3: A more professional UI design and finish up integrating the backend fully. Also need to determine the best way to store a user's files efficiently. Allowing a user to search through multiple files for text content.  

Jürgen:
* Accomplished in Sprint 2:
Primary responsibility is to explore how to build a file-classification and summary process. 
- Developed a workflow to read and process pdf (status: functional and effective)
- tokenize them (status: functional, but not optimized)
- prompt GPT to classify them (status: currently using few-shot prompting)

This included data anotation in reports to create rules and heuristics for GPT to use to classify. 

* Plan for Sprint 3:
Optimize the file-classification and summary until >95% accurate:
- Implementing the new version of few-shot prompting into the architecture
- Finding and generating more data that we can use to 1) create few-shot examples 2) create a hold-out dataset to measure our accuracy
- Experimenting with LDA and LangChain to improve the summary




-- 

## Summary Sprint 1

Magnus: 
* Accomplished in Sprint 1: Interviewed potential users, acquired data to work with, did a bit of work on the backend but Leon carried that part.
* Plan for Sprint 2:

Leon:
* Accomplished in Sprint 1: Market research in Solar M&A and research on existing intelligent search engines. Worked on the backend using LlamaIndex, i.e. the document indexing and retrieval system as well as the response generation.
* Plan for Sprint 2: Properly connect backend to the frontend, also try to incorporate re-ranking functionality to the document retrieval mechanism and exploring the usage of Vectara (an existing RAG service) as a backend. Helping Zara to improve the UI. Continue doing market research by conduting interviews with the goal of finding some actionable paint points in the solar M&A process such that we can build a solution around that (working on product-market fit).

Zara:
* Accomplished in Sprint 1: Coded a basic frontend and backend for the website. Working on integration with Leon and Magnus' RAG code. Coded some tools that use OpenAI API but haven't been integrated.
* Plan for Sprint 2:

Jürgen:
* Accomplished in Sprint 1: Talked to engineers about architecture best-practice, attend "Create Embeddings on Real-Time Data with OpenAI", experiment with having Anthropic and OpenAI fill out the checklist based on documentation provided (failed), created BasePrompt
* Plan for Sprint 2: 1) Implement base prompt; 2) Create an evaluation system to test changes to prompting in qualitative performance & accuracy 
