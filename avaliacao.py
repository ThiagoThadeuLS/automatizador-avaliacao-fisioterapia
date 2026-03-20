import streamlit as st
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# Define a cor verde padrão para o relatório
COR_VERDE_RGB = (0, 128, 0)

def limpar_texto(txt):
    """Remove caracteres que o Latin-1 não suporta e trata aspas curvas."""
    if not txt: return ""
    txt = str(txt)
    mapa = {"\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'", "\u2013": "-", "\u2014": "-"}
    for u, l in mapa.items():
        txt = txt.replace(u, l)
    # Tenta codificar para latin-1, substituindo o que não conseguir por '?'
    return txt.encode('latin-1', 'replace').decode('latin-1')

def criar_cabecalho(pdf, titulo_doc):
    # Título do Documento com fundo VERDE
    pdf.set_fill_color(*COR_VERDE_RGB) # Aplica o verde (0, 128, 0)
    pdf.set_text_color(255, 255, 255) # Texto branco para contrastar
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 12, limpar_texto(titulo_doc), border=1, ln=True, align='C', fill=True)
    
    # Restaura cor do texto para preto e define info de data
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 8, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='R')
    pdf.ln(5)

def secao_caixa(pdf, titulo, conteudo_dict):
    """Cria uma seção visual com bordas e rótulos alinhados."""
    # Configuração do título da seção (Fundo Verde, Texto Branco)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(255, 255, 255) # Texto branco
    pdf.set_fill_color(*COR_VERDE_RGB) # Fundo Verde (0, 128, 0)
    
    # Borda da 'caixa' do título também em verde para uniformidade
    pdf.set_draw_color(*COR_VERDE_RGB)
    pdf.set_line_width(0.3)
    
    # Célula do título preenchida
    pdf.cell(0, 8, f"  {limpar_texto(titulo)}", ln=True, fill=True, border=1)
    
    # Configuração do conteúdo (Fundo Branco, Texto Preto)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    # Prepara o texto do bloco
    texto_bloco = ""
    for label, valor in conteudo_dict.items():
        texto_bloco += f"{label}: {valor}\n"
    
    # multi_cell para o conteúdo com bordas laterais e inferior
    # Usamos draw_color verde definido acima para as bordas
    pdf.multi_cell(0, 7, limpar_texto(texto_bloco), border='LRB')
    
    # Restaura a cor de desenho padrão (preto) para outros elementos se houver
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(4)
    pdf.ln(4)

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
            "Nome": nome,
            "Idade": idade,
            "Ocupacao": ocupacao,
            "Email": email,
            "Telefone": telefone,
            "Questionario PAR-Q": questionario_parq,
            "Questionario risco doencas coronarias": questionario_risco_doencas_coronarias,
            "Principal": principal,
            "Secundarios": secundarios,
            "Nivel atividade fisica": nivel_atividade_fisica,
            "Historico esportivo": historico_esportivo,
            "Frequencia": frequencia,
            "Dias": dias,
            "Tempo disponivel": tempo_disponivel,
            "Turno": turno
        }

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # 1. Cabeçalho
        criar_cabecalho(pdf, "RELATÓRIO DE AVALIAÇÃO FISIOTERAPÊUTICA")
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "ANAMNESE", ln=True, align='C')

        # 2. Seção: Identificação
        secao_caixa(pdf, "1. IDENTIFICAÇÃO", {
            "Nome": nome,
            "Idade": f"{idade} anos",
            "Ocupação": ocupacao,
            "E-mail": email,
            "Telefone": telefone
        })

        # 3. Seção: Prontidão Física
        secao_caixa(pdf, "2. PRONTIDÃO FÍSICA", {
            "PAR-Q": questionario_parq,
            "Risco Coronariano": questionario_risco_doencas_coronarias
        })

        # 4. Seção: Objetivos
        secao_caixa(pdf, "3. OBJETIVOS", {
            "Principal": principal,
            "Secundários": secundarios
        })

        # 5. Seção: Histórico e Atividade
        secao_caixa(pdf, "4. HISTÓRICO E NÍVEL DE ATIVIDADE", {
            "Nível Atual": nivel_atividade_fisica,
            "Histórico Esportivo": historico_esportivo
        })

        # 6. Seção: Rotina
        secao_caixa(pdf, "5. ROTINA E DISPONIBILIDADE", {
            "Frequência": f"{frequencia}x na semana",
            "Dias": dias,
            "Tempo disponível": tempo_disponivel,
            "Turno": turno
        })

        # Rodapé Simples
        pdf.set_y(-25)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, limpar_texto(f"Avaliação de {nome} - Confidencial"), border='T', align='C')

        # Geração dos bytes para o Streamlit
        pdf_bytes = bytes(pdf.output())

        st.success("✅ PDF estruturado com sucesso!")
        st.download_button(
            label="📥 Baixar Avaliação Profissional",
            data=pdf_bytes,
            file_name=f"Avaliacao_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

    
        