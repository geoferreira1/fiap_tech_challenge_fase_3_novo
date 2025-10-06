import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

# Configuração inicial
st.set_page_config(page_title="Análise COVID", layout="wide")



#Header
with st.container():

    st.title("📊 Tech Challenger Fase 3 - Fiap")
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)

    st.header('O problema')
    st.write(
        """
        Imagine agora que você foi contratado(a) como Expert em Data Analytics
        por um grande hospital para entender como foi o comportamento da população
        na época da pandemia da COVID-19 e quais indicadores seriam importantes
        para o planejamento, caso haja um novo surto da doença.

        Apesar de ser contratado(a) agora, a sua área observou que a utilização
        do estudo do PNAD-COVID 19 do IBGE seria uma ótima base para termos boas
        respostas ao problema proposto, pois são dados confiáveis. Porém, não será
        necessário utilizar todas as perguntas realizadas na pesquisa para enxergar
        todas as oportunidades ali postas.

        ## Condições: 

        É sempre bom ressaltar que há dados triviais que precisam estar no projeto, pois auxiliam muito na análise dos dados:

        - Características clínicas dos sintomas;

        - Características da população;

        - Características econômicas da sociedade.


        E além disso, o Head de Dados pediu para que você entrasse na base de dados do PNAD-COVID-19 do IBGE (https://covid19.ibge.gov.br/pnad-covid/) e organizasse esta base para análise, utilizando Banco de Dados em Nuvem e trazendo as seguintes características:

        - Utilização de no máximo 20 questionamentos realizados na pesquisa;

        - Utilizar 3 meses para construção da solução;

        - Caracterização dos sintomas clínicos da população;

        - Comportamento da população na época da COVID-19;

        - Características econômicas da Sociedade;

        Seu objetivo será trazer uma breve análise dessas informações, como foi
        a organização do banco, as perguntas selecionadas para a resposta do problema
        e quais seriam as principais ações que o hospital deverá tomar em caso de um
        novo surto de COVID-19.
        """
    )

    st.write("""
    **Aluna:**
    
    Geovana dos Santos ferreira Matricula: RM364998
    """)
    
    st.write('[Projeto - Github](https://github.com/geoferreira1/fiap_tech_challenge_fase_3_novo/tree/main)')