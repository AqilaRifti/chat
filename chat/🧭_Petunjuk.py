import streamlit as st
from package.embeddings import RAG_SMP_KURIKULUM_2013_API_KEY
st.set_page_config(
    page_title="Petunjuk",
    page_icon="🧭",
    initial_sidebar_state="collapsed",
    layout="centered"
)

st.write("# Selamat Datang! 👋")

st.markdown(
   f"""
    Asisten Pelajar Indonesia menyediakan berbagai AI untuk membantu para penggunanya dalam berbagai 
    urusan yang dihadapi.
    ### Nama AI dan kegunaannya:
    - ❓ Milarian Jawaban -> Cari jawaban dengan instan
    - 👩‍🏫 Siasat Ngajar -> Rancang strategi mengajar untuk guru
    - 💬 Hiji Ka Hiji -> AI untuk mengobrol dan menemani berbagai hal
    {RAG_SMP_KURIKULUM_2013_API_KEY}
    #### **👈 Langsung saja di coba** untuk melihat berbagai kemampuan API!
    """
)