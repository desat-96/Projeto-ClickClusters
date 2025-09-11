import streamlit as st

# A configuração da página é a primeira coisa a ser executada
st.set_page_config(
    page_title="ClickClusters",
    layout="wide",
    initial_sidebar_state="expanded"
)

# O restante do seu código, com todos os elementos visuais preservados
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8F8F8; /* Fundo cinza claro */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center; color: #6C3483; margin-top: 50px; font-size: 52px;'>Bem-vindo ao <span style='color: #9B59B6;'>ClickClusters</span></h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; color: #7F8C8D; font-size: 28px;'>Insights Inteligentes para a Jornada do Viajante</h3>", 
    unsafe_allow_html=True
)
st.write("---")

col_text, col_image = st.columns([0.6, 0.4]) 

with col_text:
    st.markdown(
        """
        <div style='font-size: 17px;'>
        Uma iniciativa de Data Science desenvolvida para revolucionar como a ClickBus compreende e se conecta com seus viajantes. Nossa plataforma integra análises preditivas e segmentação de clientes para transformar dados brutos em insghts que direcionam decisões estratégicas e personalizadas.
        """,
        unsafe_allow_html=True
    )

    st.write(" ")
    st.write(" ")
    st.write(" ") 

    st.markdown(
        """
        <div style='font-size: 17px;'>
        Aqui, você terá acesso a ferramentas para:
        
        * <p style='background-color: #F1C40F; display: inline-block; padding: 2px 5px; border-radius: 3px; color: #2C3E50;'><strong>Decodificar o Comportamento de Compra:</strong></p> Entenda quem são seus clientes e o que os motiva.
        * <p style='background-color: #F1C40F; display: inline-block; padding: 2px 5px; border-radius: 3px; color: #2C3E50;'><strong>Prever Próximas Compras:</strong></p> Antecipe a demanda e otimize suas campanhas de marketing.
        * <p style='background-color: #F1C40F; display: inline-block; padding: 2px 5px; border-radius: 3px; color: #2C3E50;'><strong>Recomendar Trechos Inteligentes:</strong></p> Personalize a experiência de viagem com sugestões precisas.
        </div>
        """,
        unsafe_allow_html=True
    )
with col_image:
    try:
        st.image("Clickclusters_logo.png", use_container_width=True)
    except FileNotFoundError:
        st.warning("Imagem 'Clickclusters_logo.png' não encontrada.")
        st.write("*(Placeholder para Imagem Ilustrativa de Mapa/Conexões)*")

st.write("---")

footer_col1, footer_col2, footer_col3 = st.columns([0.8, 0.1, 0.1])

with footer_col1:
    st.markdown(
        "<p style='text-align: left; color: #7F8C8D;'>Desenvolvido por: [Grupo: Outliers Data Divas - Turma: 1TSCOA] - Enterprise Challenge 2025</p>",
        unsafe_allow_html=True
    )
    
with footer_col2:
    try:
        st.image("fiap_logo.png", width=100)
    except FileNotFoundError:
        st.warning("Logo 'fiap_logo.png' não encontrada.")

with footer_col3:
    try:
        st.image("marca_clickbus.png", width=100)
    except FileNotFoundError:
        st.warning("Logo 'marca_clickbus.png' não encontrada.")
