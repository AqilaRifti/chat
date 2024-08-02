from package.embeddings import get_embedding_content_kurmer_smp
from package.providers import fireworks_chat_provider, FIREWORKS_MISTRAL_8X7B_INSTRUCT

ENGLISH_PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


INDONESIAN_PROMPT_TEMPLATE = """
Jawab pertanyaan berikut berdasarkan informasi berikut:

{context}

---

Jawab pertanyaan ini berdasarkan konteks diatas: {question}
"""

def get_indonesian_prompt_template(context: str, question: str) -> str:
    return INDONESIAN_PROMPT_TEMPLATE.replace(
        "{context}", context
        ).replace(
        "{question}", question
    )


def generate_response_with_embedding(query: str) -> str:
    processed_query = query
    embedding_result = get_embedding_content_kurmer_smp(processed_query)
    if embedding_result.answer_in_context:
        return fireworks_chat_provider(
            api_key="noHEU8RG9UdiN5kMHxmyKjxvOb6kaURXwy8qxbcmzKaYHuCn",
            model=FIREWORKS_MISTRAL_8X7B_INSTRUCT,
            max_tokens=4064,
            top_p=1,
            top_k=40,
            presence_penalty=0,
            frequency_penalty=0,
            temperature=0.6,
            messages=[{"role": "user", "content": get_indonesian_prompt_template(embedding_result.answer, processed_query)}]
        )
    else:
        return fireworks_chat_provider(
            api_key="noHEU8RG9UdiN5kMHxmyKjxvOb6kaURXwy8qxbcmzKaYHuCn",
            model=FIREWORKS_MISTRAL_8X7B_INSTRUCT,
            max_tokens=4064,
            top_p=1,
            top_k=40,
            presence_penalty=0,
            frequency_penalty=0,
            temperature=0.6,
            messages=[{"role": "user", "content": processed_query}]
        )