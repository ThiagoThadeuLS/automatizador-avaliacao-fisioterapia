import streamlit as st

page_1 = st.Page("home.py", title="Home", icon="🏠")
page_2 = st.Page("avaliacao.py", title="Avaliação", icon="🧾")
# page_3 = st.Page("consultar_atleta.py", title="Consultar atleta", icon="🔍")

pg = st.navigation([page_1, page_2])

pg.run()