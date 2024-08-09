import os
from langchain_chroma import Chroma
from langchain_ai21 import AI21Embeddings
from langchain_community.document_loaders import PyPDFium2Loader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List

def get_all_file_paths(directory) -> List[os.PathLike | str]:
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings to form the full file path.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


data = []
target_directory = "./resources/Buku Paket SMK/kimia_analisis"
all_files = get_all_file_paths(target_directory)

for file in all_files:
    if file.endswith(".pdf"): # bc of ds_store
        loader = PyPDFium2Loader(file).load()
        print(f"{file}: {len(loader)}")
        data = [*data, *loader]

# Initialize the embedding function
embedding_function = AI21Embeddings(api_key="MsrTPdY71iukVx0ScFBMFWPFr2jNHDOd")
def split_text(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

# Define batch size
batch_size = 128

# Function to batch documents
def batch_documents(documents, batch_size):
    for i in range(0, len(documents), batch_size):
        yield documents[i:i + batch_size]

# Load existing database or create a new one
try:
    db = Chroma.load(persist_directory="./batch/smk_kimia_analisis.db")
except:
    db = Chroma(embedding_function=embedding_function, persist_directory="./batch/smk_kimia_analisis.db")

# Process documents in batches
for batch in batch_documents(split_text(data), batch_size):
    db.add_documents(batch)  # Add documents to the existing collection


# Optionally, print a message indicating completion
print("Documents added to Chroma database successfully.")
