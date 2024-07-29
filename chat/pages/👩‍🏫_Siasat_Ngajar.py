import streamlit as st
import json
import requests
import time
import itertools

model_id = "7qk9kpe3"
api_key = "noHEU8RG9UdiN5kMHxmyKjxvOb6kaURXwy8qxbcmzKaYHuCn"

hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    #root > div > div > div > div > header {background: none !important;}
</style>
"""

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.set_page_config(
    page_title="Siasat Ngajar",
    page_icon="👩‍🏫",
    initial_sidebar_state="collapsed",
    layout="centered",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.markdown(hide_img_fs, unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def answer_generator(messages: str):
    print(messages)
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/mixtral-8x22b-instruct",
        "max_tokens": 4064,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [{"role": "user", "content": "Kamu adalah seorang asisten guru yang akan membantu menyiapkan pembelajaran mulai dari sekarang"}, {"role": "assistant", "content": "Baik saya akan membantu guru sebagai asisten, ada yang bisa saya bantu?"}, *messages],
        "stream": False
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    resp = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(resp.json())
    for word in [*resp.json()["choices"][0]["message"]["content"]]:
        yield word
        time.sleep(0.01)


if "siasat_ngajar_messages" not in st.session_state:
    st.session_state["siasat_ngajar_messages"] = []


def send_message(message):
    st.session_state["siasat_ngajar_messages"].append(message)


with st.container(border=True):
    spacer, jenjang_option, kurikulum_option = st.columns((1.7, 1.2, 1.3))
    spacer.image("https://asistenpelajarindonesia.netlify.app/icon.svg", width=50)
    jenjang_option.selectbox(
        "jenjang",
        ("SD", "SMP", "SMA"),
        index=1,
        label_visibility="collapsed"
    )
    kurikulum_option.selectbox(
        "kurikulum",
        ("Kurmer", "Kurtilas"),
        label_visibility="collapsed"
    )


if prompt := st.chat_input():
    send_message({"role": "user", "content": prompt})
    send_message({"role": "assistant", "content": prompt})


for index, message in enumerate(st.session_state["siasat_ngajar_messages"]):
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        if message["content"] == st.session_state["siasat_ngajar_messages"][index-1]["content"]:
            with st.chat_message("assistant"):
                st.write("Bot thinking...")
                gen_for_data, gen_for_stream =itertools.tee(answer_generator(st.session_state["siasat_ngajar_messages"]))
                st.write_stream(gen_for_stream)
                message["content"] = "".join(list(gen_for_data))
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
