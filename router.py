import streamlit as st


# if 'user' not in st.session_state:
pg = st.navigation([st.Page('app/main.py', title='Soal Semester Pendek'),
                    st.Page('app/enroll.py', title='Enroll Mahasiswa')])
# else:
# pg = st.navigation([st.Page('app/presensi.py', title='Presensi Generator')])
pg.run()
