import streamlit as st


pg = st.navigation([st.Page('main.py', title='Main'), st.Page('presensi.py', title='Presensi Generator')])
pg.run()
