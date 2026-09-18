RAG-Based AI Chatbot

Overview

This project is a RAG-based chatbot built using Python and Streamlit.

It allows users to upload documents and ask questions about their content. The chatbot searches the uploaded documents for relevant information and uses that context to generate better answers.

I built this project to understand how Retrieval-Augmented Generation, embeddings, vector search, and Large Language Models work together in a real application.

My Role

I built this project myself.

My work included:

- Building the chatbot interface using Streamlit
- Loading and processing uploaded documents
- Splitting text into smaller chunks
- Creating embeddings from the document content
- Storing and searching embeddings
- Retrieving relevant information based on user questions
- Connecting the retrieved content with an LLM
- Managing the API key securely using environment variables
- Testing the chatbot with different questions

This project helped me understand how AI applications can use external data to provide more accurate and relevant answers.

Software and Tools

Programming Language

Python

Development Tools

Visual Studio Code
Streamlit

Libraries and Technologies

LangChain
LLM API
FAISS or ChromaDB
Embeddings
Python-dotenv

How the System Works

- The user uploads a document through the Streamlit application.
- The application reads the document and splits the text into smaller chunks.
- Each chunk is converted into an embedding and stored in a vector database.
- When the user asks a question, the system finds the most relevant document content.
- The retrieved content is sent to the LLM together with the user's question.
- The LLM uses that information to generate a context-aware answer.

Basic Flow

User Question → Vector Search → Relevant Document Content → LLM → Answer


Features

- Document upload through Streamlit
- Question answering based on uploaded documents
- Document processing and text chunking
- Embedding generation
- Vector similarity search
- LLM-powered responses
- Simple chatbot interface
- Secure API key management

Running the Project

Clone the repository:

git clone <repository-url>
cd rag-chatbot

Install the required packages:

pip install -r requirements.txt

Create a .env file in the project folder:

OPENAI_API_KEY=your_api_key_here

Run the application:

streamlit run app.py

The application will usually open at:

http://localhost:8501

API Key Security

The API key is stored in a .env file instead of being written directly in the source code.

Add the following to .gitignore:

.env
venv/
__pycache__/

This prevents the API key from being uploaded to GitHub.

What I Learned

From this project I learned:

- How Retrieval-Augmented Generation works
- How embeddings represent document content
- How vector search finds relevant information
- How LLMs can use external context
- How to build an AI application using Streamlit
- How to work with APIs securely
- How different parts of a RAG pipeline work together

Future Improvements

I would like to add:

- support for multiple documents
- conversation history
- source citations
- support for more file formats
- better document retrieval
- user authentication
- cloud deployment

Why This Project Matters

This project helped me understand how modern AI applications can use external documents instead of relying only on an LLM's existing knowledge.

It also gave me practical experience with Python, Streamlit, APIs, embeddings, vector databases, and LLM integration.
