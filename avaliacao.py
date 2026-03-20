import streamlit as st
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Avaliação fisioterapêutica", page_icon="🦴")

st.title("AVALIAÇÃO FISIOTERAPÊUTICA",text_alignment="center")
st.markdown("<p style='text-align: center;'>Preencha todos os campos abaixo para gerar o PDF da avaliação.</p>", unsafe_allow_html=True)


with st.form(key='avaliacao', clear_on_submit=False):
    st.header("Anamnese", text_alignment="center")

    st.subheader("👤 Identificação Inicial")

    nome = st.text_input("Nome Completo", placeholder="Digite seu nome aqui...")
    
    
    col1, col2 = st.columns([1, 2])
    with col1:
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    with col2:
        ocupacao = st.text_input("Ocupação Profissional", placeholder="Ex: Engenheiro, Estudante...")

    
    col3, col4 = st.columns(2)
    with col3:
        email = st.text_input("E-mail", placeholder="seu@email.com")
    with col4:
        telefone = st.text_input("Telefone/WhatsApp", placeholder="(00) 90000-0000")

    st.divider()

    # st.subheader("📋 Questionário de Prontidão Física (PAR-Q)")
    # st.caption("Responda 'Sim' ou 'Não' para as seguintes questões:")
    # q1 = st.radio("1. O seu médico já lhe disse alguma vez que você apresenta um problema cardíaco?", ["Não", "Sim"], horizontal=True)
    # q2 = st.radio("2. Você apresenta dores no peito com frequência?", ["Não", "Sim"], horizontal=True)
    # q3 = st.radio("3. Você apresenta episódios frequentes de tontura ou sensação de desmaio?", ["Não", "Sim"], horizontal=True)
    # q4 = st.radio("4. Seu médico alguma vez já lhe disse que sua pressão sanguínea era muito alta?", ["Não", "Sim"], horizontal=True)
    # q5 = st.radio("5. Você apresenta um problema ósseo ou articular que possa ser agravado pelo exercício?", ["Não", "Sim"], horizontal=True)
    # q6 = st.radio("6. Existe alguma outra razão física que o impeça de praticar atividade física?", ["Não", "Sim"], horizontal=True)
    # q7 = st.radio("7. Você tem mais de 65 anos e não está acostumado a se exercitar vigorosamente?", ["Não", "Sim"], horizontal=True)


    st.subheader("🏋🏼 Prontidão para atividade física")

    questionario_parq = st.text_input("Questionário PAR-Q")
    questionario_risco_doencas_coronarias = st.text_input("Questionário Risco para Doenças Coronarianas")

    st.divider()

    st.subheader("🎯 Objetivos")

    principal = st.text_area("Principal", height=100)

    secundarios = st.text_area("Secundários", height=150)

    st.divider()

    nivel_atividade_fisica = st.text_input("Nível atual de atividade física")
    historico_esportivo = st.text_area("Histórico esportivo", height=150)

    st.divider()

    st.subheader("📆 Rotina")
    col5, col6 = st.columns(2)
    with col5:
        frequencia = st.number_input("Frequência semanal", min_value=0, max_value=7)
        dias = st.text_input("Dias")
    with col6:
        tempo_disponivel = st.text_input("Tempo disponível")
        turno = st.selectbox("Turno",["Manhã", "Tarde", "Noite"])

    # O botão de submit do formulário
    submitted = st.form_submit_button("Gerar Prévia")

if submitted:
    if not (nome and idade and ocupacao and email and telefone and questionario_parq and questionario_risco_doencas_coronarias and principal and secundarios and nivel_atividade_fisica and historico_esportivo and frequencia and dias and tempo_disponivel and turno):
        st.warning("Preencha todos os campos")
    else:
        st.session_state["dados"] = {
            "nome": nome,
            "idade": idade,
            "ocupacao": ocupacao,
            "email": email,
            "telefone": telefone,
            "questionario_parq": questionario_parq,
            "questionario_risco_doencas_coronarias": questionario_risco_doencas_coronarias,
            "principal": principal,
            "secundarios": secundarios,
            "nivel_atividade_fisica": nivel_atividade_fisica,
            "historico_esportivo": historico_esportivo,
            "frequencia": frequencia,
            "dias": dias,
            "tempo_disponivel": tempo_disponivel,
            "turno": turno
        }

        
        

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", style="B", size=16)
        pdf.cell(0, 10, "AVALIAÇÃO FISIOTERAPÊUTICA", ln=True, align='C')

        pdf.set_font("helvetica", style="B", size=16)
        pdf.cell(0, 10, "ANAMNESE", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font('helvetica', size=12)
        identificacao = (
            f"Nome: {st.session_state["dados"]["nome"]}\n"
            f"Idade: {st.session_state["dados"]["idade"]}\n"
            f"Ocupação: {st.session_state["dados"]["ocupacao"]}\n"
            f"email: {st.session_state["dados"]["email"]}\n"
            f"Telefone: {st.session_state["dados"]["telefone"]}"
        )
        pdf.multi_cell(0, 10, identificacao)


        prontidao_atividade_fisica = (
            f"Questionário PAR-Q: {st.session_state["dados"]["questionario_parq"]}\n"
            f"Questionário Risco para Doenças Coronarianas: {st.session_state["dados"]["questionario_risco_doencas_coronarias"]}"
        )
        pdf.multi_cell(0, 10, prontidao_atividade_fisica)


        objetivos = (
            f"Principal: {st.session_state["dados"]["principal"]}\n"
            f"Secundários: {st.session_state["dados"]["secundarios"]}"
        )
        pdf.multi_cell(0, 10, objetivos)


        nivel_atividade = (f"Nível atual de atividade física: {st.session_state["dados"]["nivel_atividade_fisica"]}")
        pdf.cell(0, 10, nivel_atividade)



        historico = (f"Histórico esportivo: {st.session_state["dados"]["historico_esportivo"]}")
        pdf.multi_cell(190, 7, historico)


        preferencias = (
            f"Frequência: {st.session_state["dados"]["frequencia"]}\n"
            f"Dias: {st.session_state["dados"]["dias"]}\n"
            f"Tempo disponível: {st.session_state["dados"]["tempo_disponivel"]}\n"
            f"Turno: {st.session_state["dados"]["turno"]}"
        )
        pdf.multi_cell(0, 10, preferencias)


        pdf_output = pdf.output(dest="S")

        # Converte para bytes reais que o Streamlit entende
        if isinstance(pdf_output, str):
            pdf_bytes = pdf.output(dest='S').encode('latin-1', errors='replace')        
        else:
            pdf_bytes = pdf_output

        st.success("✅ PDF gerado com sucesso!")
        
        # 2. Botão de Download atualizado
        st.download_button(
            label="📥 Baixar Avaliação em PDF",
            data=pdf_bytes,
            file_name=f"Avaliacao_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
        