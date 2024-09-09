import streamlit as st
import json
import requests
import time
import itertools

API_KEY = "fw_3ZQCex4kceQGgfweNB7bF1Wk"
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
THINKING_MESSAGE = "Sedang berpikir..."
IMAGE_STYLE_MANIPULATION = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
img {
    border-radius: 1.2rem;
}
/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) {...}

/* Small devices (portrait tablets and large phones, 600px and up) */
@media only screen and (min-width: 600px) {...}

/* Medium devices (landscape tablets, 768px and up) */
@media only screen and (min-width: 768px) {
img {
    width: 700px !important;
}
}

/* Large devices (laptops/desktops, 992px and up) */
@media only screen and (min-width: 992px) {
img {
    width: 700px !important;
}
}

/* Extra large devices (large laptops and desktops, 1200px and up) */
@media only screen and (min-width: 1200px) {
img {
    width: 700px !important;
}
}
</style>
'''

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
        "content": "After this prompt, you are now going to talk to people. Go help them in their journey. They are gonna speak Indonesian Language"
    },
    {
        "role": "assistant",
        "content": "Alright, im proud to help i will do my best answering many topics in Indonesian Language"
    }
]

st.set_page_config(
    page_title="Siasat Ngajar",
    page_icon="👩‍🏫",
    initial_sidebar_state="collapsed",
    layout="centered",
)
st.markdown(IMAGE_STYLE_MANIPULATION, unsafe_allow_html=True)
st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

def answer_generator(messages: str):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
        "max_tokens": 16384,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [*INITIAL_MESSAGES, *messages],
        "stream": False
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    resp = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(resp.json())
    for word in [*resp.json()["choices"][0]["message"]["content"]]:
        yield word
        time.sleep(0.01)


st.image("chat/assets/hiji-ka-hiji.png")

if "hiji_ka_hiji_messages" not in st.session_state:
    st.session_state["hiji_ka_hiji_messages"] = []


def send_message(message):
    st.session_state["hiji_ka_hiji_messages"].append(message)


if prompt := st.chat_input():
    send_message({"role": "user", "content": prompt})
    send_message({"role": "assistant", "content": prompt})


for index, message in enumerate(st.session_state["hiji_ka_hiji_messages"]):
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        if message["content"] == st.session_state["hiji_ka_hiji_messages"][index-1]["content"]:
            with st.chat_message("assistant"):
                st.write(THINKING_MESSAGE)
                gen_for_data, gen_for_stream =itertools.tee(answer_generator(st.session_state["hiji_ka_hiji_messages"]))
                st.write_stream(gen_for_stream)
                message["content"] = "".join(list(gen_for_data))
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
