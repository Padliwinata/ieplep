import deta
import streamlit as st


deta_obj = deta.Deta(st.secrets['DATA_KEY'])
db_user = deta_obj.Base("mahasiswa")

