import streamlit as st
from db import db_user


st.title('Enroll Mahasiswa')


@st.experimental_dialog("Masukkan password")
def get_user():
    kode = st.text_input("Kode")
    if st.button("submit"):
        if kode != 'NipisMadu2324':
            st.session_state.status = 'rejected'
        else:
            st.session_state.status = 'accepted'
        st.rerun()


if "status" not in st.session_state:
    get_user()
else:
    if st.session_state.status == 'rejected':
        st.error('Unauthorized User')
    else:
        nim = st.text_input("NIM")
        file = st.file_uploader(label='List Mahasiswa')
        st.button("submit")

