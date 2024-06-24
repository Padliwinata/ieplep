import streamlit as st

from db import db_user


def increase_user_download():
    db_user.update({'downloaded': True}, st.session_state.key)
    st.rerun()


@st.experimental_dialog("Masukkan NIM dan kode")
def get_nim():
    nim = st.text_input("NIM")
    kode = st.text_input("Kode")
    if st.button("submit"):
        fetch_response = db_user.fetch({'nim': nim, 'kode': kode})
        if fetch_response.count == 0:
            st.session_state.status = 'rejected'
        else:
            st.session_state.nim = nim
            st.session_state.kode = kode
            st.session_state.key = fetch_response.items[0]['key']
            st.session_state.downloaded = fetch_response.items[0]['downloaded']
            st.session_state.status = 'accepted'
        st.rerun()


if "status" not in st.session_state:
    get_nim()
else:
    if st.session_state.status == 'rejected':
        st.error('Credential rejected')
    else:
        if st.session_state.downloaded:
            st.error('User already downloaded the file')
        else:
            with open('soal/alpro/ALPRO1.pdf', 'rb') as file:
                st.download_button(file_name='Soal Alpro SP.pdf',
                                   label='Soal Alpro',
                                   data=file.read(),
                                   on_click=increase_user_download)
            file = st.file_uploader(label='Jawaban')
