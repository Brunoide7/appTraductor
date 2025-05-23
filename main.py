"""
Traductor de idiomas desplegado en streamlit
"""
import streamlit as st
import streamlit.components.v1 as components
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

#prompt:
system_template = "Traduzca el siguiente texto de entrada a {language}: "
prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text_input}")
    ]
)

#Título e icono de pestaña:
st.set_page_config(
    page_title="Traductor LLM",
    page_icon="https://cdn-icons-png.flaticon.com/128/576/576515.png",
    layout="centered"
)

#streamlit UI:
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background-color: #b03a2e; border-radius: 10px; color: white;'>
        <div style='display: flex; justify-content: center; align-items: center; gap: 15px;'>
            <img src="https://cdn-icons-png.flaticon.com/128/576/576515.png" width="50">
            <h2 style="margin: 0;">Bienvenido al TraductorLLM</h2>
        </div>
        <div style="display: flex; justify-content: center; gap: 40px; margin-top: 20px;">
            <a href="https://github.com/Brunoide7" target="_blank" style="text-decoration:none; color: white; display:flex; align-items:center;">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="24" style="margin-right:8px;">
                Mas aplicaciones en GitHub
            </a>
            <a href="https://www.linkedin.com/in/bruno-ignacio-tolaba/" target="_blank" style="text-decoration:none; color: white; display:flex; align-items:center;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24" style="margin-right:8px;">
                Contacto personal en LinkedIn
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

#función para copiar la traducción al portapapeles
def copiar_al_portapapeles(texto):
    components.html(
        f"""
        <textarea id="to-copy" style="position: absolute; left: -9999px;">{texto}</textarea>
        <button onclick="document.getElementById('to-copy').select(); document.execCommand('copy');"
                style="margin-top:10px; padding:8px 12px; background:#b03a2e; color:white; border:none; border-radius:5px; cursor:pointer;">
            Copiar al portapapeles
        </button>
        """,
        height=80,
    )

#configuración del llm:
def load_llm(openai_api_key):
    return ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

#ingreso de API Key:
openai_api_key = st.text_input("OpenAI API Key", type="password", placeholder="Ex: sk-2twmA8tfCb8un4...")

#seleccionar idioma:
language = st.selectbox(
        'Traducir a:',
        ('English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese'))

#función para insertar el valor del idioma en el diccionario de entrada:
inject_language = RunnableLambda(lambda x: {**x, "language": language})

#ingreso de texto: 
draft_input = st.text_area(label="Text", label_visibility='collapsed',
                            placeholder="Ejemplo: Hello, how are you?", key="draft_input")

if draft_input:
    #verificación de la api_key:
    if not openai_api_key:
        st.warning("Por favor inserte una API Key válida.")
        st.stop()

    #modelo:
    llm = load_llm(openai_api_key)

    #cadena:
    chain =  inject_language | prompt_template | llm | StrOutputParser()

    #Ejecución:
    response = chain.invoke({
        "text_input": draft_input
    })

    #visualización de la respuesta:
    st.markdown("##### Traducción:")
    st.write(response)
    copiar_al_portapapeles(response)

