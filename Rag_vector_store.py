from langchain_community.vectorstores import FAISS
import csv
from uuid import uuid4
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS  # or Chroma
from langchain.embeddings import OpenAIEmbeddings
import os

from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into environment

# api_key =  put the key over here

# Step 1: Initialize HuggingFace Embeddings
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")



vector_store_cake = FAISS.load_local(
    folder_path="faiss_index_bge/faiss_index_bge_500_chunks",
    embeddings=embeddings,
    index_name="index",  # Default name
    allow_dangerous_deserialization=True
)




# === 0. Setup ===
# === 2. Create Retriever ===

retriever = vector_store_cake.as_retriever(search_kwargs={"k": 5})

# === 3. Define LLM ===
llm = ChatOpenAI(model="gpt-4.1-nano")  # or gpt-3.5-turbo

# === 4. Format retrieved docs with metadata citations ===
def format_docs_with_citations(docs):
    seen_sources = {}
    formatted_chunks = []
    source_counter = 1

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        if source not in seen_sources:
            seen_sources[source] = source_counter
            source_counter += 1
        citation_num = seen_sources[source]
        formatted_chunks.append(f"{doc.page_content.strip()} [SOURCE {citation_num}]")

    return "\n\n".join(formatted_chunks), seen_sources

# === 5. Ask Query and Generate Answer ===
def ask_rag(query):
    # Retrieve docs
    retrieved_docs = retriever.get_relevant_documents(query)

    # Format context and collect citation mapping
    context, source_map = format_docs_with_citations(retrieved_docs)

    # Build prompt
    prompt = f"""
You are an intelligent assistant helping answer questions using the provided context.

Instructions:
- Only use information from the context below.
- Cite your claims with [<number>] inline where relevant
- At the end of your answer,  Like in research papers

Context:
{context}

Question: {query}

Answer:
"""

    # Run LLM
    response = llm.invoke(prompt)

    # Output answer and sources
    print("\n=== Answer ===\n")
    print(response.content)

    print("\n=== Sources ===")
    text_sources = "Sources: \n"
    for link, num in source_map.items():
        text_sources += f"\n[{num}] -> {link}\n"
        print(f"[{num}] -> {link}")
    
    return  response.content + "\n\n"+ text_sources

# # === 6. Run Example ===
# final=ask_rag("find me details for btech acadmic calender 2025")
# print("\n\n\n")
# print(final)