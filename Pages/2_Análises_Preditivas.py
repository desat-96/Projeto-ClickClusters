import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib 
import gdown  # <-- MUDANÇA AQUI
import os     # <-- MUDANÇA AQUI

st.set_page_config(
    page_title="ClickClusters - Previsão de Compras",
    layout="wide"
)

# --- PALETA DE CORES E COR NEUTRA ---
PALETA_CORES = {
    'Viajantes Inativos': '#9400F7',
    'Viajantes Ocasionais': '#EBBC00',
    'Viajantes Frequentes': '#00005C',
    'Viajantes Promissores': '#D4A3FF',
    'Super Compradores': '#E86800'
}
COR_NEUTRA = '#517CED'

# --- FUNÇÃO PARA CARREGAR OS DADOS (VERSÃO FINAL COM GDOWN) ---
@st.cache_data
def carregar_dados():
    try:
        # ID do arquivo no Google Drive extraído do seu link
        file_id = '1Inn8nyb3YRiqpln1yI0jph7bRUGLOal4'
        output_path = 'df_dashboard_final_producao.csv' # Nome do arquivo a ser salvo

        # Verifica se o arquivo já foi baixado para não baixar de novo
        if not os.path.exists(output_path):
            st.warning(f"Baixando o arquivo de dados ({output_path}) do Google Drive. Isso pode levar um momento...")
            gdown.download(id=file_id, output=output_path, quiet=False)
        
        df = pd.read_csv(output_path)
        
        df['date_purchase'] = pd.to_datetime(df['date_purchase'])
        if 'Ano' not in df.columns:
            df['Ano'] = df['date_purchase'].dt.year
            
        return df
        
    except Exception as e:
        st.error(f"Erro fatal ao carregar os dados. Verifique o ID do arquivo ou a conexão. Detalhe: {e}")
        return None

df_final_app = carregar_dados()

# --- TÍTULO E INTRODUÇÃO ---
if df_final_app is not None:
    st.title("Módulo 2: Análise Preditiva Unificada")
    st.markdown("Insights acionáveis sobre a probabilidade de compra e o próximo destino dos clientes nos próximos 30 dias.")
    st.write("---")

    # --- BARRA LATERAL (SIDEBAR) COM FILTROS ---
    st.sidebar.header("Filtros de Análise")
    
    lista_anos = sorted(df_final_app['Ano'].unique().tolist(), reverse=True)
    anos_selecionados = st.sidebar.multiselect('Selecione um ou mais Anos:', lista_anos, default=None)
    lista_segmentos = df_final_app['Tipo de Seguimento'].unique().tolist()
    segmentos_selecionados = st.sidebar.multiselect('Selecione um ou mais Segmentos:', lista_segmentos, default=None)
    limiar_probabilidade = st.sidebar.slider('Limiar de Probabilidade de Compra:', min_value=0, max_value=100, value=70, format='%d%%')

    # --- LÓGICA DE FILTRAGEM ---
    df_filtrado = df_final_app.copy()
    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['Ano'].isin(anos_selecionados)]
    if segmentos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['Tipo de Seguimento'].isin(segmentos_selecionados)]
    
    limiar_decimal = limiar_probabilidade / 100
    df_clientes_acionaveis = df_filtrado[df_filtrado['Probabilidade_Compra'] >= limiar_decimal]

    # --- SEÇÃO DE KPIs ---
    st.subheader("Indicadores de Performance da Previsão")
    
    clientes_acionaveis_count = df_clientes_acionaveis['fk_contact'].nunique()
    if clientes_acionaveis_count > 0:
        gmv_potencial = clientes_acionaveis_count * df_clientes_acionaveis.drop_duplicates(subset=['fk_contact'])['Ticket_Medio_Compra_por_Transacao'].mean()
    else:
        gmv_potencial = 0
    
    if not df_filtrado.empty:
        trecho_popular = df_filtrado['Trecho_Anonimo'].mode()[0] if not df_filtrado['Trecho_Anonimo'].mode().empty else "N/A"
        trecho_rentavel = df_filtrado.groupby('Trecho_Anonimo')['gmv_success'].sum().idxmax() if not df_filtrado.empty else "N/A"
    else:
        trecho_popular = "N/A"
        trecho_rentavel = "N/A"

    gmv_formatado = f"R$ {gmv_potencial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label=f"Clientes Acionáveis (> {limiar_probabilidade}%)", value=f"{clientes_acionaveis_count:,}".replace(",", "."))
    with col2:
        st.metric(label="GMV Potencial Estimado (R$)", value=gmv_formatado)
    with col3:
        st.metric(label="Trecho Mais Popular", value=trecho_popular)
    with col4:
        st.metric(label="Trecho Mais Rentável", value=trecho_rentavel)
    with col5:
        st.metric(
            label="Cobertura de Oportunidades", 
            value="89%",
            help="Nosso modelo é calibrado para encontrar 89 de cada 100 clientes que realizarão uma compra em 30 dias."
        )
    st.write("---")

    # --- TABELA DE CLIENTES ACIONÁVEIS ---
    st.subheader("Lista de Clientes Acionáveis")
    
    def colorir_segmento(val):
        cor = PALETA_CORES.get(val, 'black')
        return f'color: {cor}; font-weight: bold;'

    colunas_tabela = ['fk_contact', 'Tipo de Seguimento', 'Probabilidade_Compra', 'Frequência', 'Recência', 'Trecho_Sugerido_Anonimo']
    df_tabela_display = df_clientes_acionaveis.drop_duplicates(subset=['fk_contact']).sort_values('Probabilidade_Compra', ascending=False).head(1000)
    tabela_para_exibir = df_tabela_display[colunas_tabela]
    
    tabela_renomeada = tabela_para_exibir.rename(columns={
        'fk_contact': 'ID do Cliente', 'Tipo de Seguimento': 'Segmento',
        'Probabilidade_Compra': 'Probabilidade de Compra em 30 dias', 'Frequência': 'Frequência',
        'Recência': 'Recência (dias)', 'Trecho_Sugerido_Anonimo': 'Trecho Sugerido'
    })

    tabela_para_estilizar = tabela_renomeada.reset_index(drop=True)
    tabela_estilizada = tabela_para_estilizar.style.format({
        'Probabilidade de Compra em 30 dias': '{:.2%}'
    }).apply(lambda row: row.map(lambda val: colorir_segmento(val)), subset=['Segmento'])
        
  
    st.dataframe(tabela_estilizada.hide(axis="index"), use_container_width=True)
    st.write("---")

    # --- GRÁFICO DE DISTRIBUIÇÃO DE RECOMPRA ---
    st.subheader("Distribuição de Recompra dos Clientes")
    cor_grafico_ciclo = COR_NEUTRA
    if len(segmentos_selecionados) == 1:
        cor_grafico_ciclo = PALETA_CORES[segmentos_selecionados[0]]
    
    # Criamos um dataframe de clientes únicos ANTES de plotar o gráfico
    df_clientes_unicos_filtrado = df_filtrado.drop_duplicates(subset=['fk_contact'])
    df_recompras_filtrado = df_clientes_unicos_filtrado.dropna(subset=['dias_entre_compras'])
    
    if not df_recompras_filtrado.empty:
        fig_hist_dias = px.histogram(df_recompras_filtrado, x='dias_entre_compras', nbins=100, template='plotly_white', labels={'dias_entre_compras': 'Dias Até a Próxima Compra'})
        fig_hist_dias.update_traces(marker_color=cor_grafico_ciclo, xbins=dict(start=0, end=df_recompras_filtrado['dias_entre_compras'].max(), size=7))
        
        # AJUSTE 2: Alterar a escala do eixo x
        fig_hist_dias.update_xaxes(range=[0, 500])
        
        fig_hist_dias.update_layout(title_text=None, yaxis_title='Quantidade de Recompras', xaxis_title='Dias até a Próxima Compra', bargap=0.1)
        st.plotly_chart(fig_hist_dias, use_container_width=True)
    else:
        st.info("Não há dados de recompra para a seleção de segmentos atual.")
    st.write("---")

    # --- GRÁFICOS DE ANÁLISE PREDITIVA ---
    col_dist, col_trechos = st.columns(2)

    with col_dist:
        st.subheader("Distribuição das Probabilidades")
        cor_grafico_dist = COR_NEUTRA
        if len(segmentos_selecionados) == 1:
            cor_grafico_dist = PALETA_CORES[segmentos_selecionados[0]]

        df_clientes_unicos_filtrado = df_filtrado.drop_duplicates(subset=['fk_contact'])   
        
        fig_hist_prob = px.histogram(df_clientes_unicos_filtrado, x='Probabilidade_Compra', nbins=50, labels={'Probabilidade_Compra': 'Faixa de Probabilidade de Compra'}, template='plotly_white')
        fig_hist_prob.update_traces(marker_color=cor_grafico_dist)
        fig_hist_prob.update_layout(yaxis_title='Quantidade de Clientes', bargap=0.1, title_text=None)
        fig_hist_prob.update_xaxes(tickformat='.0%')
        st.plotly_chart(fig_hist_prob, use_container_width=True)

    with col_trechos:
        st.subheader("Top 10 Trechos para Clientes Acionáveis")
        cor_grafico_trechos = COR_NEUTRA
        if len(segmentos_selecionados) == 1:
            cor_grafico_trechos = PALETA_CORES[segmentos_selecionados[0]]
        
        if not df_clientes_acionaveis.empty:
            top_trechos = df_clientes_acionaveis['Trecho_Anonimo'].value_counts().nlargest(10).reset_index()
            top_trechos.columns = ['Trecho', 'Contagem']
            
            fig_trechos = px.bar(top_trechos.sort_values('Contagem'), x='Contagem', y='Trecho', orientation='h', text='Contagem', template='plotly_white')
            fig_trechos.update_traces(marker_color=cor_grafico_trechos, textposition='outside')
            fig_trechos.update_layout(title_text=None, yaxis={'title_text': ''}, xaxis={'title_text': 'Nº de Clientes Acionáveis'}, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_trechos, use_container_width=True)
        else:
            st.info("Não há clientes acionáveis para a seleção atual.")