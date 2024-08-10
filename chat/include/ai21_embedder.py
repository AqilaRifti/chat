import os
import sys
import dotenv
import pathlib
from typing import List
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_ai21 import AI21Embeddings
from langchain_community.document_loaders import PyPDFium2Loader
from langchain.text_splitter import RecursiveCharacterTextSplitter

dotenv.load_dotenv()

AI21_API_KEY = os.getenv("AI21_API_KEY")
BATCH_SIZE = 128
embedding_function = AI21Embeddings(api_key=AI21_API_KEY)


def get_all_file_paths(directory: str) -> List[os.PathLike | str]:
    file_paths = []
    for root, _directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings to form the full file path.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

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


def ai21_embed(source_directory: str, target_directory: str) -> None:
    data = []
    all_files = get_all_file_paths(pathlib.Path(source_directory))
    for file in all_files:
        if file.endswith(".pdf"):
            loader = PyPDFium2Loader(file).load()
            print(f"{file}: {len(loader)}")
            data = [*data, *loader]

    def batch_documents(documents: List[Document], batch_size: int):
        for i in range(0, len(documents), batch_size):
            yield documents[i:i + batch_size]

    try:
        db = Chroma.load(persist_directory=target_directory)
    except:
        db = Chroma(embedding_function=embedding_function, persist_directory=target_directory)

    for index, batch in enumerate(batch_documents(split_text(data), BATCH_SIZE)):
        db.add_documents(batch)
        print(f"{index} embedded to db")

    print("Documents added to Chroma database successfully.")

def main():
    source_directory: str = str(sys.argv[0])
    target_directory: str = str(sys.argv[1])
    ai21_embed(source_directory, target_directory)

if __name__ == "__main__":
    main()