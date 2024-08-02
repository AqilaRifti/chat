import streamlit as st
import time
import itertools
from typing import List
from package.embeddings import (
    get_embedding_content_k13_sd,
    get_embedding_content_k13_smp,
    get_embedding_content_k13_sma,
    get_embedding_content_kurmer_sd,
    get_embedding_content_kurmer_smp,
    get_embedding_content_kurmer_sma,
    LibraryAnswerResponse
)
from package.generate_response import fireworks_chat_provider
from st_copy_to_clipboard import st_copy_to_clipboard

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

INDONESIAN_PROMPT_TEMPLATE = """
Jawab pertanyaan berdasarkan informasi berikut:

{context}

---

Jawab pertanyaan ini berdasarkan konteks diatas (Jawablah dalam Bahasa Indonesia): {question}
"""

def generate_prompt_english(query: str) -> str:
    return PROMPT_TEMPLATE.format(
        context=query, 
        question=query
    )


model_id = "7qk9kpe3"
api_key = "noHEU8RG9UdiN5kMHxmyKjxvOb6kaURXwy8qxbcmzKaYHuCn"


st.set_page_config(page_title="Milarian Jawaban", page_icon="❓", initial_sidebar_state="collapsed", layout="centered",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


if "milarian_jawaban_messages" not in st.session_state:
    st.session_state["milarian_jawaban_messages"] = []


def send_message(message):
    st.session_state["milarian_jawaban_messages"].append(message)


model_id = "7qk9kpe3"
api_key = "noHEU8RG9UdiN5kMHxmyKjxvOb6kaURXwy8qxbcmzKaYHuCn"

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
        ("SD", "SMP", "SMA", "SMK"),
        index=1,
        label_visibility="collapsed"
    )
    if selected_jenjang == "SMK":
        selected_kurikulum = kurikulum_option.selectbox(
            "kurikulum",
            (
                "Akuntansi",
                "Administrasi Perkantoran",
                "Multimedia",
                "Farmasi",
                "Keperawatan",
                "Teknik Logistik",
                "Teknik Komputer Jaringan",
                "Teknik Elektronika Industri",
                "Bisnis & Pemasaran",
                "Pelayaran",
                "Perhotelan",
                "Tata Boga"
            ),
            label_visibility="collapsed"
        )
    else:
        selected_kurikulum = kurikulum_option.selectbox(
            "kurikulum",
            ("Kurmer", "K13"),
            label_visibility="collapsed"
        )


hide_streamlit_style = """
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

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
THINKING_MESSAGE = "Sedang berpikir..."

def generate_prompt_indonesia(query: str) -> str:
    embedding: LibraryAnswerResponse = eval(f"get_embedding_content_{selected_kurikulum.lower()}_{selected_jenjang.lower()}(query).answer")
    if embedding.answer_in_context:
        return INDONESIAN_PROMPT_TEMPLATE.format(
            context=embedding,
            question=query
        )
    else:
        return f"(Jawablah pertanyaan ini dengan Bahasa Indonesia) {query}"


def answer_generator(messages: List[str]):
    modified_message = {"role": "user", "content": generate_prompt_indonesia(messages[-1]["content"])}
    new_messages = messages.copy()
    new_messages.pop()
    new_messages.append(modified_message)

    payload = {
        "model": "accounts/fireworks/models/llama-v3-70b-instruct",
        "max_tokens": 4064,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": new_messages
    }
    resp = fireworks_chat_provider(api_key=api_key, **payload)


    for word in [*resp["choices"][0]["message"]["content"]]:
        yield word
        time.sleep(0.001)

st_copy_to_clipboard("Copy this to clipboard")

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
                gen_for_data, gen_for_stream =itertools.tee(answer_generator(st.session_state["milarian_jawaban_messages"]))
                st.write_stream(gen_for_stream)
                st.write(":blue[**Bersumber dari Buku Paket Kementerian Pendidikan Dan Kebudayaan Indonesia**]")
                message["content"] = "".join(list(gen_for_data))
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
                st.write(":blue[**Bersumber dari Buku Paket Kementerian Pendidikan Dan Kebudayaan Indonesia**]Bersumber dari Buku Paket Kementerian Pendidikan Dan Kebudayaan Indonesia**")
