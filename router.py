import streamlit as st


pg = st.navigation([st.Page('app/main.py', title='Main'), st.Page('app/presensi.py', title='Presensi Generator')])
pg.run()
