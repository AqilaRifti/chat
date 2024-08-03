from langchain_chroma import Chroma
from langchain_fireworks import FireworksEmbeddings
embedding_function = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5", fireworks_api_key="fpbRTHn1iqBjdjGEvbkGxozyvvwMwYzxDpumZKH2TUQuNjbt")

db = Chroma(persist_directory="./smk_tata_boga.db", embedding_function=embedding_function)
query = "Hidangan adalah"
docs = db.similarity_search(query)
for doc in docs:
    print(doc.page_content)