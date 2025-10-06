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

    st.write("---")
with st.container():
    st.header("Conclusão Geral e Ações Estratégicas")
    st.write("A análise do questionário revela que a população que experimentou sintomas de COVID-19 em 2020 era majoritariamente composta por pessoas em idade economicamente ativa (entre 21 e 50 anos), com uma incidência levemente maior em mulheres. A maioria desses indivíduos se autodeclarou Parda e possuía até o Ensino Médio completo, com renda baixa ou desempregada. A tosse e a febre foram os sintomas mais comuns, mas, notavelmente, uma grande parte dessa população não buscou auxílio médico, e os casos que evoluíram para internação ou sedação foram minoria. Essa falta de busca por atendimento, aliada a fatores socioeconômicos, sugere que o acesso à saúde foi um desafio significativo.")
    st.markdown("### Ações Estratégicas para o Hospital em um Novo Surto")
    st.markdown("Com base nessas conclusões, um hospital pode adotar as seguintes ações para se preparar para um novo surto de forma mais eficaz:")
    
    st.markdown("""
    **1. Otimização dos Protocolos de Triagem e Testagem:**
    - **Foco nos sintomas mais comuns:** Aprimorar os protocolos de triagem para priorizar a triagem de pacientes com tosse e febre.
    - **Incentivo à testagem:** Fortalecer a comunicação sobre a importância da testagem, especialmente com o método Swab.
    """)

    st.markdown("""
    **2. Expansão da Acessibilidade ao Atendimento:**
    - **Canais alternativos:** Desenvolver e promover canais de telemedicina para pacientes com sintomas leves a moderados, a fim de aumentar a busca por auxílio e aliviar a pressão sobre as emergências.
    """)

    st.markdown("""
    **3. Comunicação Direcionada e Educação em Saúde:**
    - **Campanhas focadas:** Criar campanhas de comunicação direcionadas às faixas etárias de 21 a 50 anos, à população Parda e a indivíduos com menor nível de escolaridade.
    - **Linguagem clara:** As campanhas devem usar uma linguagem simples e acessível para explicar a importância do isolamento social, da testagem e da busca por atendimento médico.
    """)