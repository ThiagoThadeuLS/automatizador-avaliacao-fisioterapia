import streamlit as st


st.set_page_config(page_title='Bárbara Gosling', page_icon='👩‍⚕️',layout='centered')


st.subheader('Automatizador de PDF', text_alignment='center')
st.divider()
col1, col2, col3 = st.columns([1.5,1.5,1.5])
with col2:
    st.image('barbaraGosling_melhorado.png', width='stretch')
