import os
import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentReader:
    def read(self, uploaded_file):
        file_name = uploaded_file.name.lower()

        if file_name.endswith(".pdf"):
            return self.read_pdf(uploaded_file)

        if file_name.endswith(".docx"):
            return self.read_docx(uploaded_file)

        if file_name.endswith(".txt"):
            return self.read_txt(uploaded_file)

        return ""

    def read_pdf(self, uploaded_file):
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    def read_docx(self, uploaded_file):
        document = Document(uploaded_file)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    def read_txt(self, uploaded_file):
        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )


class TextProcessor:
    def __init__(self, chunk_size=1500, overlap=250):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text):
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap

        return chunks


class DocumentRetriever:
    def retrieve(self, question, chunks, top_k=4):
        if not chunks:
            return []

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            chunks + [question]
        )

        document_vectors = vectors[:-1]
        question_vector = vectors[-1]

        similarities = cosine_similarity(
            question_vector,
            document_vectors
        ).flatten()

        best_indexes = similarities.argsort()[
            -top_k:
        ][::-1]

        return [
            chunks[index]
            for index in best_indexes
            if similarities[index] > 0
        ]


class AIChatbot:
    def __init__(self):
        load_dotenv()

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_answer(
        self,
        question,
        context,
        conversation
    ):
        previous_messages = ""

        for message in conversation[-6:]:
            previous_messages += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        prompt = f"""
You are a helpful document assistant.

Use the document context below as your primary source.

Rules:

1. Answer using the uploaded document.
2. Do not invent unsupported information.
3. If the answer is not available, say:
"I could not find that information in the uploaded document."
4. Explain the answer clearly.

DOCUMENT CONTEXT:

{context}

RECENT CONVERSATION:

{previous_messages}

USER QUESTION:

{question}
"""

        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text


class DocumentChatbotApp:
    def __init__(self):
        self.reader = DocumentReader()
        self.processor = TextProcessor()
        self.retriever = DocumentRetriever()
        self.chatbot = AIChatbot()

        self.initialize_session()

    def initialize_session(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "chunks" not in st.session_state:
            st.session_state.chunks = []

        if "document_name" not in st.session_state:
            st.session_state.document_name = None

    def process_document(self, uploaded_file):
        if (
            st.session_state.document_name
            == uploaded_file.name
        ):
            return

        document_text = self.reader.read(
            uploaded_file
        )

        if not document_text.strip():
            st.error(
                "I could not read text from this document."
            )
            return

        st.session_state.chunks = (
            self.processor.split_text(
                document_text
            )
        )

        st.session_state.document_name = (
            uploaded_file.name
        )

        st.session_state.messages = []

        st.success(
            f"Document loaded: {uploaded_file.name}"
        )

    def display_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )

    def handle_question(self, question):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        relevant_chunks = (
            self.retriever.retrieve(
                question,
                st.session_state.chunks
            )
        )

        context = "\n\n---\n\n".join(
            relevant_chunks
        )

        with st.chat_message("assistant"):
            try:
                answer = (
                    self.chatbot.generate_answer(
                        question,
                        context,
                        st.session_state.messages
                    )
                )

                st.markdown(answer)

            except Exception as error:
                answer = f"Error: {error}"
                st.error(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    def run(self):
        st.set_page_config(
            page_title="Document AI Chatbot",
            page_icon="🤖"
        )

        st.title("🤖 Document AI Chatbot")

        uploaded_file = st.file_uploader(
            "Upload a reference document",
            type=["pdf", "docx", "txt"]
        )

        if uploaded_file:
            self.process_document(
                uploaded_file
            )

        self.display_messages()

        if st.session_state.chunks:
            question = st.chat_input(
                "Ask a question about the document"
            )

            if question:
                self.handle_question(question)

        else:
            st.info(
                "Please upload a document first."
            )


if __name__ == "__main__":
    app = DocumentChatbotApp()
    app.run()