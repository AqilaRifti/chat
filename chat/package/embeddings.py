from ai21 import AI21Client
from ai21.models.responses.library_answer_response import LibraryAnswerResponse

# Access Type A (Expired 17 October 2024)
RAG_SD_KURIKULUM_2013_API_KEY = ""
RAG_SD_KURIKULUM_KURMER_API_KEY = ""
# Access Type B (Expired 16 October 2024)
RAG_SMP_KURIKULUM_2013_API_KEY = "xlDvCjQch5NcZyokpRheEvc3l8QfEU4j"
RAG_SMP_KURIKULUM_MERDEKA_API_KEY = "pgKtMOzWF6itfZdMXKzkpqcelNcjoYRA"
# Access Type C (Expired 16 October 2024)
RAG_SMA_KURIKULUM_2013_API_KEY = "t8pGcgDzZEGbU0TTg5TjSoMILqSCQIYD"
RAG_SMA_KURIKULUM_MERDEKA_API_KEY = "2tyFM3aNl2HqV26326ZkzeDG2CPwAIZs"

def get_embedding_base(query: str, api_key: str) -> LibraryAnswerResponse:
    client = AI21Client(
        api_key=api_key,
    )
    return client.library.answer.create(question=query)

# --- K13 Region ---

def get_embedding_content_k13_sd(query: str) -> LibraryAnswerResponse:
    return get_embedding_base(query, RAG_SMP_KURIKULUM_2013_API_KEY)

def get_embedding_content_k13_smp(query: str) -> LibraryAnswerResponse:
    return get_embedding_base(query, RAG_SMP_KURIKULUM_2013_API_KEY)

def get_embedding_content_k13_sma(query: str) -> LibraryAnswerResponse:
    return get_embedding_base(query, RAG_SMA_KURIKULUM_2013_API_KEY)

# --- Kurmer Region ---

def get_embedding_content_kurmer_sd(query: str) -> LibraryAnswerResponse:
    return get_embedding_base(query, RAG_SMP_KURIKULUM_2013_API_KEY)

def get_embedding_content_kurmer_smp(query: str) -> LibraryAnswerResponse:
    return get_embedding_base(query, RAG_SMP_KURIKULUM_MERDEKA_API_KEY)

def get_embedding_content_kurmer_sma(query: str) -> LibraryAnswerResponse:
    return get_embedding_base(query, RAG_SMA_KURIKULUM_MERDEKA_API_KEY)
