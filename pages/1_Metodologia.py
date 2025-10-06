import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from PIL import Image

#Header
with st.container():

    st.title("📊 Metodologia")
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)

    st.header('Arquitetura dos dados')
    st.write(
        """
        - Fonte dos dados: [PNAD-COVID19 IBGE](https://covid19.ibge.gov.br/pnad-covid/).
        - Período analisado: De Setembro à Novembro de 2020 (3 meses)
        - Ferramentas utilizada: Github, VsCode, AWS RDS (Postgresql), AWS S3, AWS Glue, Python, SQL, Streamlit
        """
    )

    image = Image.open("./imagens/arquitetura_dos_dados.jpg")
    st.image(image)


with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)

    st.header('Etapas realizadas:')
    st.write(
        """
        1. Identificação dos arquivos necessários para utilização.
        2. Upload dos arquivos no repositório do projeto no Github. 
        3. Criação do banco de dado na AWS, buckets no s3 e parametrizações no Glue.
        4. Validações das conexões acima.
        5. Leitura e iteração dos arquivos no Git via requests (Últimos 3 meses).
        6. Criação das das subpastas (Bronze, Silver e Gold) no s3.
        7. Ingestão dos arquivos do git no RDS.
        8. Conexão e ingestão dos dados do RDS para a camada Bronze no s3.
        9. Conexão e ingestão dos dados da Bronze para para a Silver no s3 (Seleção das variáveis).
        10. Conexão e ingestão dos dados da Silver para a Gold no s3 (Enriquecimento e Transformações aplicadas nas variáveis).
        11. Opção 1: Ingestão da tabela da pasta Gold para o RDS (Análise dos dados por RDS e publicação de dataviz via streamlit - Disponibilidade 24/7) - OPÇÃO ESCOLHIDA.
        11. Opção 1: Criação do banco de dados e creawlers no Glue (Análise dos dados pelo Athena e publicação de dataviz via streamlit - Disponibilidade apenas quando o console AWS estivesse conextado).
        """
    )