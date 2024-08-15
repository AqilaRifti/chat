import time
import itertools
import streamlit as st
from typing import List
from package.generate_response import fireworks_chat_provider
from package.embeddings import (
    get_embedding_content_k13_smp,
    get_embedding_content_k13_sma,
    get_embedding_content_kurmer_smp,
    get_embedding_content_kurmer_sma,
    LibraryAnswerResponse
)
from include.loader import (
    similarity_search_embedding,
    ai21_embedding_function_example,
    similarity_search_with_relevance_scores_embedding
)

INDONESIAN_PROMPT_TEMPLATE = """
Jawab pertanyaan berdasarkan informasi berikut:

{context}

---

Jawab pertanyaan ini berdasarkan konteks diatas (Jawablah dalam Bahasa Indonesia): {question}
"""

api_key = "pfS623hAge5hEPUKymOYIGaWYIO7ruiuLk8EDIlvwGWJGXGp"

DEFAULT_PAGE_ICON = "❓"
DEFAULT_LAYOUT = "centered"
DEFAULT_PAGE_TITLE = "Milarian Jawaban"
DEFAULT_INITIAL_SIDEBAR_STATE = "collapsed"

THINKING_MESSAGE = "Sedang berpikir..."
HIDE_STREAMLIT_STYLE = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0.5rem;}
    #root > div > div > div > div > header {background: none !important;}
    button[title="View fullscreen"]{visibility: hidden;}
    header {visibility: hidden;}
    @media (max-width: 50.5rem) {
        #root > div:nth-child(1) > div > div > div > div > section > div  {
            max-width: 100vw !important;
        }
    }
</style>
"""

SLOGAN_AND_MOTTO = """
Slogan:
"Membangun Masa Depan, Satu Langkah Sekaligus"

(Translation: "Building the Future, One Step at a Time")

Motto:
"Ilmu, Inovasi, Integritas: Membentuk Generasi Emas Indonesia"

(Translation: "Knowledge, Innovation, Integrity: Shaping Indonesia's Golden Generation")
"""


INITIAL_MESSAGES = [
    {
        "role": "user",
        "content": f"Every time someone ask you who is your creator/maker/developer/builder your gonna answer the Educational Organization \"Asisten Pelajar Indonesia\" that aims  to prepare and help indonesia reach its golden generation through high quality education! {SLOGAN_AND_MOTTO}"
    },
    {
        "role": "assistant",
        "content": "I'm ready to respond accordingly. Go ahead and ask me who my creator/maker/developer/builder is!\n\n(And just to confirm, my response will be: \"My creator/maker/developer/builder is the Educational Organization 'Asisten Pelajar Indonesia' that aims to prepare and help Indonesia reach its golden generation through high-quality education!\")"
    },
    {
        "role": "user",
        "content": "After this prompt, you are now going to help students learn. Go help them in their learning. They are gonna speak Indonesian Language"
    },
    {
        "role": "assistant",
        "content": "Alright, im proud to help i will do my best answering many topics in Indonesian Language"
    }
]
st.set_page_config(
    page_title=DEFAULT_PAGE_TITLE,
    page_icon=DEFAULT_PAGE_ICON,
    initial_sidebar_state=DEFAULT_INITIAL_SIDEBAR_STATE,
    layout=DEFAULT_LAYOUT
)


if "milarian_jawaban_messages" not in st.session_state:
    st.session_state["milarian_jawaban_messages"] = []


def send_message(message):
    st.session_state["milarian_jawaban_messages"].append(message)

icon = ""
with open("chat/icon.svg", "r") as icon_reader:
    icon = icon_reader.read()

link_url = "http://google.com.au"
html_content = f'''
<a href="{link_url}" target="_blank">
    {icon}
</a>
'''

with st.container(border=True):
    brand, jenjang_option, kurikulum_option = st.columns((1.7, 1.1, 1.6))
    brand.markdown(html_content, unsafe_allow_html=True)

    selected_jenjang = jenjang_option.selectbox(
        "jenjang",
        ( "SMP", "SMA", "SMK"),
        index=0,
        label_visibility="collapsed"
    )

    if selected_jenjang == "SMK":
        selected_kurikulum = kurikulum_option.selectbox(
            "kurikulum",
            (
                "Akuntansi",
                "Administrasi Perkantoran",
                "Farmasi",
                "Keperawatan",
                "Teknik Komputer Jaringan",
                "Teknik Elektronika Industri",
                "Teknik Kendaraan Ringan Otomotif",
                "Bisnis dan Pemasaran",
                "Pelayaran",
                "Perhotelan",
                "Tata Boga",
                "Tata Busana",
                "Tata Kecantikan",
                "Kimia Analisis"
            ),
            label_visibility="collapsed"
        )

    if selected_jenjang == "SMP":
        selected_kurikulum = kurikulum_option.selectbox(
            "kurikulum",
            ("Kurmer", "K13"),
            label_visibility="collapsed"
        )

    if selected_jenjang == "SMA":
        selected_kurikulum = kurikulum_option.selectbox(
            "kurikulum",
            ("Kurmer", "K13 (Coming Soon)"), # TODO: Add K13 Curricullum as an option
            label_visibility="collapsed"
        )



def smp_k13_handler(query: str):
    embedding: LibraryAnswerResponse = get_embedding_content_k13_smp(query)
    if embedding.answer_in_context:
        return INDONESIAN_PROMPT_TEMPLATE.format(
            context=embedding.answer,
            question=query
        )
    else:
        return f"(Jawablah pertanyaan ini dengan Bahasa Indonesia) {query}"

def smp_kurmer_handler(query: str):
    embedding: LibraryAnswerResponse = get_embedding_content_kurmer_smp(query)
    if embedding.answer_in_context:
        return INDONESIAN_PROMPT_TEMPLATE.format(
            context=embedding.answer,
            question=query
        )
    else:
        return f"(Jawablah pertanyaan ini dengan Bahasa Indonesia) {query}"

def sma_kurmer_handler(query: str):
    embedding: LibraryAnswerResponse = get_embedding_content_kurmer_sma(query)
    if embedding.answer_in_context:
        return INDONESIAN_PROMPT_TEMPLATE.format(
            context=embedding.answer,
            question=query
        )
    else:
        return f"(Jawablah pertanyaan ini dengan Bahasa Indonesia) {query}"

def sma_k13_handler(query: str):
    return "Coming Soon"

def smk_handler(query: str, selected_kurikulum: str):
    embedding_data = []
    for document in similarity_search_embedding(f"batch/smk_{selected_kurikulum.lower().replace(' ', '_')}.db", query, ai21_embedding_function_example):
        print(document.page_content)
        embedding_data.append(document.page_content)
    return INDONESIAN_PROMPT_TEMPLATE.format(
            context="".join(embedding_data),
            question=query
        )

def generate_prompt_indonesia(query: str, selected_jenjang: str, selected_kurikulum: str) -> str:
    if selected_jenjang == "SMK":
        return smk_handler(query, selected_kurikulum)

    elif selected_jenjang == "SMA":
        if selected_kurikulum == "K13":
            return sma_k13_handler(query)
        elif selected_kurikulum == "Kurmer":
            return sma_kurmer_handler(query)
        else:
            return "ERROR: INVALID CURRICULLUM"

    elif selected_jenjang == "SMP":
        if selected_kurikulum == "K13":
            return smp_k13_handler(query)
        elif selected_kurikulum == "Kurmer":
            return smp_kurmer_handler(query)
        else:
            return "ERROR: INVALID CURRICULLUM"

    else:
        return "ERROR: INVALID GRADE"

def answer_generator(messages: List[str], selected_jenjang: str, selected_kurikulum: str):
    modified_message = {"role": "user", "content": generate_prompt_indonesia(messages[-1]["content"], selected_jenjang, selected_kurikulum)}
    new_messages = messages.copy()
    new_messages.pop()
    new_messages.append(modified_message)

    payload = {
        "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
        "max_tokens": 16384,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [*INITIAL_MESSAGES, *new_messages]
    }
    resp = fireworks_chat_provider(api_key=api_key, **payload)

    for word in [*resp["choices"][0]["message"]["content"]]:
        yield word
        time.sleep(0.001)



st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

if prompt := st.chat_input():
    send_message({"role": "user", "content": prompt})
    send_message({"role": "assistant", "content": prompt})

for index, message in enumerate(st.session_state["milarian_jawaban_messages"]):
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        if message["content"] == st.session_state["milarian_jawaban_messages"][index-1]["content"]:
            with st.chat_message("assistant"):
                st.write(THINKING_MESSAGE)
                gen_for_data, gen_for_stream = itertools.tee(
                    answer_generator(
                        st.session_state["milarian_jawaban_messages"],
                        selected_jenjang,
                        selected_kurikulum
                    ))
                st.write_stream(gen_for_stream)
                st.write(":blue[**Bersumber dari Buku Paket Kementerian Pendidikan Dan Kebudayaan Indonesia**]")
                message["content"] = "".join(list(gen_for_data))
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
                st.write(":blue[**Bersumber dari Buku Paket Kementerian Pendidikan Dan Kebudayaan Indonesia**]")
