from typing import List, Tuple, Optional
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_ai21 import AI21Embeddings
from langchain_core.embeddings import Embeddings
from langchain_fireworks import FireworksEmbeddings

ai21_embedding_function_example = AI21Embeddings(api_key="MsrTPdY71iukVx0ScFBMFWPFr2jNHDOd")
nomic_embedding_function_example = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5", fireworks_api_key="fpbRTHn1iqBjdjGEvbkGxozyvvwMwYzxDpumZKH2TUQuNjbt")


def similarity_search_embedding(
        db_directory: str,
        query: str,
        embedding_function: Embeddings,
        k: Optional[int] = 3
    ) -> List[Document]:
    return Chroma(
        persist_directory=db_directory,
        embedding_function=embedding_function
        ).similarity_search(
            query,
            k=k
        )


def similarity_search_with_relevance_scores_embedding(
        db_directory: str,
        query: str,
        embedding_function: Embeddings,
        k: Optional[int] = 3
    ) -> List[Tuple[Document, float]]:
    return Chroma(
        persist_directory=db_directory,
        embedding_function=embedding_function
        ).similarity_search_with_relevance_scores(
            query=query,
            k=k
        )

