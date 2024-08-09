import os
from langchain_chroma import Chroma
from langchain_fireworks import FireworksEmbeddings
from langchain_community.document_loaders import PyPDFium2Loader
from typing import List
# ZXcm4g_fWxyLi_B
def get_all_file_paths(directory) -> List[os.PathLike | str]:
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings to form the full file path.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


data = []
target_directory = "./resources/Buku Paket SMK/"
all_files = get_all_file_paths(target_directory)

for file in all_files:
    if file.endswith(".pdf"): # bc of ds_store
        loader = PyPDFium2Loader(file).load_and_split()
        print(f"{file}: {len(loader)}")
        data = [*data, *loader]

# Initialize the embedding function
embedding_function = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5", fireworks_api_key="pfS623hAge5hEPUKymOYIGaWYIO7ruiuLk8EDIlvwGWJGXGp")

# Define batch size
batch_size = 256

# Function to batch documents
def batch_documents(documents, batch_size):
    for i in range(0, len(documents), batch_size):
        yield documents[i:i + batch_size]

# Load existing database or create a new one
try:
    db = Chroma.load(persist_directory="./smk_super.db")
except:
    db = Chroma(embedding_function=embedding_function, persist_directory="./smk_super.db")

# Process documents in batches
for batch in batch_documents(data, batch_size):
    db.add_documents(batch)  # Add documents to the existing collection


# Optionally, print a message indicating completion
print("Documents added to Chroma database successfully.")
