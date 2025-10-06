import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

st.title('📊 Desafio')
st.markdown("""
## A proposta exigiu que fizéssemos as análises dos seguintes dados:

- Características clínicas dos sintomas;
- Características da população;
- Características da sociedade;

A partir dessas condições, trouxemos uma breve análise dessas informações, explicitando o modo como organizamos o banco de dados, o porquê da seleção das melhores perguntas que trariam as melhores respostas e, por fim, as ações mais efetivas que o hospital deverá tomar em caso de um novo surto de COVID-19.
""")

# Carregar as credenciais dos segredos do Streamlit
usuario_pg = st.secrets["POSTGRES_USER_PNAD"]
senha_pg = st.secrets["POSTGRES_PASSWORD_PNAD"]
host_pg = st.secrets["POSTGRES_HOST_PNAD"]
porta_pg = st.secrets["POSTGRES_PORT_PNAD"]
banco_pg = st.secrets["POSTGRES_DB_PNAD"]

@st.cache_resource
def get_database_connection():
    """Cria e retorna a engine de conexão com o banco de dados."""
    engine = create_engine(f"postgresql+psycopg2://{usuario_pg}:{senha_pg}@{host_pg}:{porta_pg}/{banco_pg}")
    return engine

def load_data():
    """Carrega os dados do banco de dados e realiza o pré-processamento."""
    engine = get_database_connection()
    query = "SELECT * FROM questionario_covid;"
    df = pd.read_sql_query(query, con=engine)
    
    # Ajusta coluna de 'moradia'
    df.rename(columns={'a006': 'situacao_escolar', 'modaria':'moradia'}, inplace=True)
    df['situacao_escolar'] = df['situacao_escolar'].apply(lambda x: 'Sim' if x == 1 else 'Não' if x == 2 else 'Desconhecido')
    
    # Ajusta respostas de moradia
    mapeamento_moradia = {1: 'Própria', 2: 'Própria', 3: 'Aluguel', 4: 'Cedido', 5: 'Cedido', 6: 'Cedido'}
    df['moradia'] = df['moradia'].map(mapeamento_moradia).fillna('Desconhecido')
    
    # Coluna para identificar se teve ao menos 1 sintoma
    colunas_sintomas = [
        'frebre_semana_anterior',
        'tosse_semana_anterior',
        'dificuldade_de_respirar_semana_anterior',
        'perda_olfato_paladar_semana_anterior'
    ]
    df['sintoma_semana_anterior'] = df[colunas_sintomas].apply(lambda x: 1 if 'Sim' in x.values else 0, axis=1)

    # Filtrando apenas quem teve sintoma
    df_filtrado = df[df['sintoma_semana_anterior'] == 1].copy()

    return df_filtrado

# Funções de customização de gráficos
def grafico_vertical(ax, valor, titulo):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_ylim(0, valor.max() * 1.1)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('', fontsize=10)
    ax.set_xlabel('', fontsize=10)
    ax.yaxis.set_ticks([])
    ax.yaxis.set_ticklabels([])
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.set_title(titulo, fontweight='bold', fontsize=12)
    plt.tight_layout()

def grafico_horizontal(ax, valor, titulo):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xlim(0, valor.max() * 1.1)
    ax.yaxis.set_ticks_position('none')
    ax.set_ylabel('', fontsize=10)
    ax.set_xlabel('', fontsize=10)
    ax.xaxis.set_ticks([])
    ax.xaxis.set_ticklabels([])
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.set_title(titulo, fontweight='bold', fontsize=12)
    plt.tight_layout()

# Configuração da página Streamlit
st.set_page_config(layout="wide")
st.title("Análises do Questionário COVID-19")
st.markdown("---")

# Carregar os dados
df_filtrado = load_data()

# --- Análise Exploratória ---
st.header("Análise Exploratória")

st.subheader("Informações do DataFrame filtrado (somente com sintomas)")
st.write(f"Linhas: {df_filtrado.shape[0]}, Colunas: {df_filtrado.shape[1]}")
st.markdown("---")

# --- Caracterização dos sintomas clínicos da população ---
st.header("Caracterização dos sintomas clínicos da população")

st.write(
    """
    **Sintomas, diagnóstico e tratamento:** 

    - A maioria dos entrevistados com sintomas relatou tosse (45,7%) e febre (28,8%), enquanto sintomas como dificuldade de respirar e perda de olfato/paladar foram menos frequentes. Mesmo com esses sintomas, a maior parte das pessoas não buscou auxílio médico. Dos que procuraram atendimento e foram diagnosticados, o teste de Swab foi o mais utilizado para confirmação (47,6%), enquanto o de sangue do dedo foi o menos comum (24,2%). A necessidade de internação (2,2%) ou sedação (0,5%) foi a minoria dos casos.

    **Conclusão:** 

    - Há uma clara discrepância entre a ocorrência de sintomas e a busca por ajuda profissional. A maioria da população se autodiagnosticou ou tratou os sintomas em casa, com febre e tosse sendo as manifestações mais comuns. A baixa taxa de internação e sedação sugere que os casos foram majoritariamente leves ou moderados, ou que a busca por tratamento ocorreu em estágios avançados, o que não é possível saber com os dados.
    
    Veja as análises gráficas abaixo.
    """
)

col1, col2 = st.columns(2)

with col1:
    # Gráfico 1: Sintomas mais comuns
    colunas_sintomas = ['frebre_semana_anterior', 'tosse_semana_anterior', 'dificuldade_de_respirar_semana_anterior', 'perda_olfato_paladar_semana_anterior']
    nomes_sintomas = {'frebre_semana_anterior': 'Febre', 'tosse_semana_anterior': 'Tosse', 'dificuldade_de_respirar_semana_anterior': 'Dificuldade de respirar', 'perda_olfato_paladar_semana_anterior': 'Perda de olfato/paladar'}
    contagem_sintomas = df_filtrado[colunas_sintomas].apply(lambda x: (x == 'Sim').sum())
    total_sintomas_contados = contagem_sintomas.sum()
    percentual_sintomas = (contagem_sintomas / total_sintomas_contados * 100).sort_values(ascending=False)
    percentual_sintomas.index = [nomes_sintomas[col] for col in percentual_sintomas.index]
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=percentual_sintomas.index, y=percentual_sintomas.values, color='sienna', ax=ax1)
    for p in ax1.patches:
        ax1.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax1, percentual_sintomas, 'Distribuição dos sintomas mais comuns (em %)')
    st.pyplot(fig1)

with col2:
    # Gráfico 2: Resultados positivos por tipo de teste
    colunas_testes = ['resultado_teste_swab', 'resultado_teste_dedo', 'resultado_teste_veia']
    nomes_testes = {'resultado_teste_swab': 'Swab', 'resultado_teste_dedo': 'Dedo', 'resultado_teste_veia': 'Veia'}
    contagem_testes = df_filtrado[colunas_testes].apply(lambda x: (x == 'Positivo').sum())
    total_testes_positivos = contagem_testes.sum()
    percentual_testes = (contagem_testes / total_testes_positivos * 100).sort_values(ascending=False)
    percentual_testes.index = [nomes_testes[col] for col in percentual_testes.index]
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=percentual_testes.index, y=percentual_testes.values, color='sienna', ax=ax2)
    for p in ax2.patches:
        ax2.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax2, percentual_testes, 'Resultados positivos por tipo de teste (em %)')
    st.pyplot(fig2)

col3, col4 = st.columns(2)

with col3:
    # Gráfico 3: Busca por auxílio médico
    contagem_auxilio = df_filtrado['buscou_auxilio_medico'].value_counts(normalize=True) * 100
    contagem_auxilio.sort_values(ascending=False, inplace=True)
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=contagem_auxilio.index, y=contagem_auxilio.values, color='sienna', ax=ax3)
    for p in ax3.patches:
        ax3.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax3, contagem_auxilio, 'Buscas por auxílio médico (em %)')
    st.pyplot(fig3)

with col4:
    # Gráfico 4: Internação
    contagem_internacao = df_filtrado['precisou_de_internacao'].value_counts(normalize=True) * 100
    contagem_internacao.sort_values(ascending=False, inplace=True)
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=contagem_internacao.index, y=contagem_internacao.values, color='sienna', ax=ax4)
    for p in ax4.patches:
        ax4.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax4, contagem_internacao, 'Necessidade de internação (em %)')
    st.pyplot(fig4)

contagem_sedacao = df_filtrado['precisou_de_sedacao'].value_counts(normalize=True) * 100
contagem_sedacao.sort_values(ascending=False, inplace=True)
fig5, ax5 = plt.subplots(figsize=(8, 6))  # Aumenta o tamanho para ocupar a linha inteira
sns.barplot(x=contagem_sedacao.index, y=contagem_sedacao.values, color='sienna', ax=ax5)
for p in ax5.patches:
    ax5.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
grafico_vertical(ax5, contagem_sedacao, 'Necessidade de sedação (em %)')
st.pyplot(fig5)

# Macro Tema: Comportamento da População na Pandemia

st.markdown("---")

st.subheader("Comportamento da População na Pandemia")

st.write(
    """
    **Isolamento social e Renda:** 

    - Apenas 40,2% da população com sintomas ficou rigorosamente em casa. A maioria dos entrevistados residia em casa própria (52,2%), o que sugere um certo nível de estabilidade, mas não impediu a exposição.

    - A faixa de renda mais comum entre os entrevistados com sintomas desconsiderando as respostas desconhecidas, é a de 800 - 1.600 (17,1%), que seria classificada como renda baixa, o que justica os 50,6% da população que reportou ter recebido auxílio emergencial, mesmo que maioria dos entrevistados esteja trabalhando atualmente.

    **Conclusão:** 

    - O isolamento social rigoroso não foi uma opção para a maioria dos entrevistados. A baixa escolaridade e as faixas de renda mostram uma vulnerabilidade social e econômica na amostra, o que, somado à baixa utilização do auxílio emergencial, sugere que as necessidades financeiras foram um fator decisivo para a manutenção de atividades fora de casa, mesmo com sintomas.
    
    Veja as análises gráficas abaixo.
    """
)


# Gráfico 6: Isolamento social
isolamento_social = df_filtrado['isolamento_social'].value_counts(normalize=True) * 100
isolamento_social.sort_values(ascending=False, inplace=True)
fig6, ax6 = plt.subplots(figsize=(8, 6))
sns.barplot(x=isolamento_social.values, y=isolamento_social.index, color='sienna', ax=ax6)
for p in ax6.patches:
    ax6.annotate(f'{p.get_width():.1f}%', (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2), ha='center', va='center', xytext=(25, 0), textcoords='offset points', fontsize=8)
grafico_horizontal(ax6, isolamento_social, 'Isolamento social dos entrevistados (em %)')
st.pyplot(fig6)


col7, col8 = st.columns(2)

with col7:
    # Gráfico 7: Situação empregatícia
    trabalha_atualmente = df_filtrado['trabalha_atualmente'].value_counts(normalize=True) * 100
    trabalha_atualmente.sort_values(ascending=False, inplace=True)
    fig7, ax7 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=trabalha_atualmente.index, y=trabalha_atualmente.values, color='sienna', ax=ax7)
    for p in ax7.patches:
        ax7.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax7, trabalha_atualmente, 'Situação empregatícia dos entrevistados (em %)')
    st.pyplot(fig7)


with col8:
    # Gráfico 8: Auxílio emergencial
    auxilio_emergencial = df_filtrado['auxilio_emergencial'].value_counts(normalize=True) * 100
    auxilio_emergencial.sort_values(ascending=False, inplace=True)
    fig8, ax8 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=auxilio_emergencial.index, y=auxilio_emergencial.values, color='sienna', ax=ax8)
    for p in ax8.patches:
        ax8.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax8, auxilio_emergencial, 'Utilização de auxílio emergencial (em %)')
    st.pyplot(fig8)


col9, col10 = st.columns(2)

with col9:
    # Gráfico 9: Faixa de renda
    faixa_salarial = df_filtrado['faixa_salarial'].value_counts(normalize=True) * 100
    faixa_salarial.sort_values(ascending=False, inplace=True)
    fig9, ax9 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=faixa_salarial.values, y=faixa_salarial.index, color='sienna', ax=ax9)
    for p in ax9.patches:
        ax9.annotate(f'{p.get_width():.1f}%', (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2), ha='center', va='center', xytext=(25, 0), textcoords='offset points', fontsize=8)
    grafico_horizontal(ax9, faixa_salarial, 'Faixa de renda dos entrevistados (em %)')
    st.pyplot(fig9)

with col10:
    # Gráfico 10: Moradia
    moradia = df_filtrado['moradia'].value_counts(normalize=True) * 100
    moradia.sort_values(ascending=False, inplace=True)
    fig10, ax10 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=moradia.values, y=moradia.index, color='sienna', ax=ax10)
    for p in ax10.patches:
        ax10.annotate(f'{p.get_width():.1f}%', (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2), ha='center', va='center', xytext=(25, 0), textcoords='offset points', fontsize=8)
    grafico_horizontal(ax10, moradia, 'Situação de moradia dos entrevistados (em %)')
    st.pyplot(fig10)


st.markdown("---")

st.subheader("Características Sócio-Demográficas")

st.write(
    """
    **Idade, Gênero e Escolaridade:** 

    - As faixas etárias mais afetadas foram as de 31-40 anos (16,4%), 41-50 anos (14,5%) e 21-30 anos (13,9%). Os dados mostram que a incidência de sintomas foi ligeiramente maior em mulheres (55,3%) do que em homens (44,7%). Em relação à escolaridade, a maioria das pessoas que sentiram sintomas tinham até o Ensino Fundamental incompleto (31.6%).
    
    **Conclusão:** 

    - As pessoas em idade economicamente ativa foram as que mais reportaram sintomas. Isso pode ser um reflexo de uma maior exposição social e profissional, já que esses grupos não puderam aderir completamente ao isolamento social.

    Veja as análises gráficas abaixo.
    """
)

col11, col12 = st.columns(2)

with col11:
    # Gráfico 11: Idade dos entrevistados
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 120]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
    df_filtrado['faixa_etaria'] = pd.cut(df_filtrado['idade'], bins=bins, labels=labels, right=True, include_lowest=True)
    contagem_idade = df_filtrado['faixa_etaria'].value_counts(normalize=True) * 100
    contagem_idade.sort_values(ascending=False, inplace=True)
    fig11, ax11 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=contagem_idade.index, y=contagem_idade.values, color='sienna', ax=ax11)
    for p in ax11.patches:
        ax11.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax11, contagem_idade, 'Idade dos entrevistados (em %)')
    st.pyplot(fig11)

with col12:
    # Gráfico 12: Gênero
    contagem_sexo = df_filtrado['sexo'].value_counts(normalize=True) * 100
    contagem_sexo.sort_values(ascending=False, inplace=True)
    fig12, ax12 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=contagem_sexo.index, y=contagem_sexo.values, color='sienna', ax=ax12)
    for p in ax12.patches:
        ax12.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax12, contagem_sexo, 'Gênero dos entrevistados (em %)')
    st.pyplot(fig12)

col13, col14 = st.columns(2)

with col13:
    # Gráfico 13: Cor/Raça
    contagem_cor = df_filtrado['cor'].value_counts(normalize=True) * 100
    contagem_cor.sort_values(ascending=False, inplace=True)
    fig13, ax13 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=contagem_cor.index, y=contagem_cor.values, color='sienna', ax=ax13)
    for p in ax13.patches:
        ax13.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    grafico_vertical(ax13, contagem_cor, 'Cor/Raça dos entrevistados (em %)')
    st.pyplot(fig13)

with col14:
    # Gráfico 14: Escolaridade
    contagem_escolaridade = df_filtrado['escolaridade'].value_counts(normalize=True) * 100
    contagem_escolaridade.sort_values(ascending=False, inplace=True)
    fig14, ax14 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=contagem_escolaridade.values, y=contagem_escolaridade.index, color='sienna', ax=ax14)
    for p in ax14.patches:
        ax14.annotate(f'{p.get_width():.1f}%', (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2), ha='center', va='center', xytext=(25, 0), textcoords='offset points', fontsize=8)
    grafico_horizontal(ax14, contagem_escolaridade, 'Escolaridade dos entrevistados (em %)')
    st.pyplot(fig14)

st.markdown("---")

st.info("Todos os dados e análises foram gerados a partir do `analises_covid.ipynb`.")
