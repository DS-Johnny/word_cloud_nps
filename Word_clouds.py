#--------------------------------------------------IMPORTS
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
import spacy
import spacy.cli

# ----------------------------------------- CONFIG
import subprocess

# Verifique se o modelo Spacy já está instalado
try:
    import spacy
    nlp = spacy.load("pt_core_news_sm")
except ImportError:
    # Se o modelo não estiver instalado, instale-o a partir do arquivo .whl
    subprocess.run(["pip", "install", "pt_core_news_sm-3.6.0-py3-none-any.whl"])

#spacy.cli.download("pt_core_news_sm")

#nlp = spacy.load("pt_core_news_sm")


def gerar_nuvem(df, coluna):
    comentarios = list(df[coluna].dropna())
    coments = ''
    for comentario in comentarios:
        comentario = comentario.replace('!', ' ')
        coments += comentario


    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(coments)
    words = ''
    for token in doc:
        if token.pos_ in options:
            words += ' ' + token.text

    mask = np.array(Image.open('logo-movida.png'))

    with open("stop_words.txt", "r") as arquivo:
        stop = arquivo.read()
        stop = stop.split(', ')

    wc = WordCloud(stopwords = stop,
                   mask= mask, background_color = 'white',
                   max_words = 2000, max_font_size = 500,
                   random_state = 43, width= mask.shape[1],
                   height = mask.shape[0])

    wc.generate(words)
    plt.imshow(wc, interpolation="None")
    plt.axis('off')
    img = plt
    st.pyplot(img)

#-------------------------------------------------SIDEBAR
st.sidebar.title('Movida')
st.sidebar.write('Análise de comentários')

options = st.sidebar.multiselect(
    'Escolha',
    ['VERB', 'NOUN', 'ADJ'],
    default=['VERB', 'NOUN', 'ADJ']
)

#-----------------------------------------------------------BODY
arquivo = st.file_uploader("Choose a file", type=['xlsx', 'csv'])

if arquivo:
    try:
        df = pd.read_csv(arquivo)
    except:
        df = pd.read_excel(arquivo)
    
    colunas = df.columns.to_list()
    coluna = st.selectbox('Escolha a coluna que contém os comentários', colunas)
    coluna_notas = st.selectbox('Excolha a coluna que contém as notas', colunas)
    notas = df[coluna_notas].unique()
    if notas is not None:
        nota = st.sidebar.multiselect(
            'Selecione as notas',
            notas
        )
        lines = df[coluna_notas].isin(nota)
        df = df.loc[lines, :]
        
    gerar_nuvem(df, coluna)
    
    
    
else:
    st.warning('Por favor, carregue um arquivo .csv ou .xlsx')

