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

st.set_page_config(page_title="Avaliação fisioterapêutica", page_icon="🦴", layout="centered")

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


    st.subheader("🏋🏼 Prontidão para atividade física")

    questionario_parq = st.text_input("Questionário PAR-Q")

    questionario_risco_doencas_coronarias = st.text_input("Questionário Risco para Doenças Coronarianas")

    st.divider()


    st.subheader("🎯 Objetivos")

    principal = st.text_area("Principal", height=100)

    secundarios = st.text_area("Secundários", height=150)

    st.divider()


    st.subheader("📊 Nível esportivo")

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

    st.divider()


   
    st.header("Controle de saúde", text_alignment="center")
   
   
    queixas_atuais =st.text_area("Queixas atuais (história atual, mecanismo de lesão, exames, fatores atenuantes e agravantes,… )", height=150)

    historia_pregressa = st.text_area("História pregressa (dores/lesões prévias, histórico de cirurgias,…)", height=150)

    historico_saude = st.text_area("Histórico de saúde)", height=150)

    medicamentos_uso = st.text_area("Medicamenros em uso", height=100)

    st.subheader("🩺 Parâmetros de saúde")
   
    nivel_hidratação = st.slider("Nível de hidratação (L) | 0-5", 0, 5)

    col1, col2 = st.columns(2)
    with col1:
        qualidade_sono = st.slider("Qualidade do sono | 0-10", 0, 10)
        
        qualidade_alimentacao = st.slider("Qualidade da alimentação | 0-10", 0, 10)
    with col2:
        nivel_stress = st.slider("Nível de stress | 0-10", 0, 10)
        
        nivel_disposicao = st.slider("Nível de disposição | 0-10", 0, 10)

    st.subheader("Postura de trabalho")
    
    col1, col2, col3, col4, col5 = st.columns([1, 0.17, 0.17, 0.17, 1], gap=None)
    with col2:
        st.image("cadeira_full_branco.png", width="content")
    with col3:
        st.image("pessoas_full_branco.png", width="content")
    with col4:
        st.image("andar_full_branco.png", width="content")
    
    col1, col2, col3 = st.columns([1.6,1.1,1.6])
    with col2:
        postura_de_trabalho = st.radio(" ", options=[1, 2, 3], horizontal=True, width="stretch", label_visibility="collapsed")

    st.divider()

    st.header("Composição corporal", text_alignment="center")



    # O botão de submit do formulário
    submitted = st.form_submit_button("Gerar Prévia")

if submitted:
    if not (nome and idade and ocupacao and email and telefone and questionario_parq and questionario_risco_doencas_coronarias and principal and secundarios and nivel_atividade_fisica and historico_esportivo and frequencia and dias and tempo_disponivel and turno and queixas_atuais and historia_pregressa and historico_saude and medicamentos_uso and nivel_hidratação and qualidade_sono and nivel_stress and nivel_disposicao and postura_de_trabalho):
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
            "Turno": turno,
            "Queixas atuais": queixas_atuais,
            "História pregressa": historia_pregressa,
            "Histórico de saúde": historico_saude,
            "Medicamentos em uso": medicamentos_uso,
            "Nível de hidratação": nivel_hidratação,
            "Qualidade do sono": qualidade_sono,
            "Nível de stress": nivel_stress,
            "Nível de disposição": nivel_disposicao,
            "Postura de Trabalho": postura_de_trabalho
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

    
        