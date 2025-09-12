import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib 
import gdown  # <-- MUDANÇA AQUI
import os
import glob

# st.set_page_config(page_title="Home", page_icon="🏠")

# st.title("🏠 Página Inicial")

# st.write("Bem-vindo!")

# if st.button("Ir para Página 1"):
#     st.switch_page ("pages/1_Perfis_de_Clientes.py")
    


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
        st.image("dashboard/Clickclusters_logo.png", use_container_width=True)
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
        st.image("dashboard/fiap_logo.png", width=100)
    except FileNotFoundError:
        st.warning("Logo 'dashboard/fiap_logo.png' não encontrada.")

with footer_col3:
    try:
        st.image("dashboard/marca_clickbus.png", width=100)
    except FileNotFoundError:
        st.warning("Logo 'dashboard/marca_clickbus.png' não encontrada.")




#===========================================
# Pagina 1 

# st.set_page_config(page_title="Página 1", page_icon="📄")

# st.title("📄 Página 1")
# st.write("Você chegou na Página 1!")


# st.set_page_config(
#     page_title="ClickClusters - Perfil de Clientes",
#     layout="wide"
# )

# --- PALETA DE CORES DOS SEGMENTOS ---
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
        arquivos= glob.glob('data/*.parquet')
        
        df = pd.concat([pd.read_parquet(arquivo) for arquivo in arquivos], ignore_index=True)
        
        df['date_purchase'] = pd.to_datetime(df['date_purchase'])
        if 'Ano' not in df.columns:
            df['Ano'] = df['date_purchase'].dt.year
            
        return df
        
    except Exception as e:
        st.error(f"Erro fatal ao carregar os dados. Verifique o ID do arquivo ou a conexão. Detalhe: {e}")
        return None

# Carrega o DataFrame mestre e único
df_final_app = carregar_dados()

# --- TÍTULO E INTRODUÇÃO ---
if df_final_app is not None:
    st.title("Módulo 1: Perfil de Clientes")
    st.markdown("Visão 360° do comportamento e características dos seus viajantes.")
    st.write("---")

    # --- BARRA LATERAL (SIDEBAR) COM FILTROS ---
    st.sidebar.header("Filtros de Análise")
    
    lista_segmentos = sorted(df_final_app['Tipo de Seguimento'].unique().tolist())
    segmentos_selecionados = st.sidebar.multiselect(
        'Selecione um ou mais Segmentos:',
        lista_segmentos,
        default=None
    )

    lista_anos = sorted(df_final_app['Ano'].unique().tolist(), reverse=True)
    anos_selecionados = st.sidebar.multiselect(
        'Selecione um ou mais Anos:',
        lista_anos,
        default=None
    )
    limiar_probabilidade = st.sidebar.slider('Limiar de Probabilidade de Compra:', min_value=0, max_value=100, value=70, format='%d%%')

    # --- LÓGICA DE FILTRAGEM ---
    df_filtrado = df_final_app.copy()
    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['Ano'].isin(anos_selecionados)]
    if segmentos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['Tipo de Seguimento'].isin(segmentos_selecionados)]

    
    # --- SEÇÃO DE MÉTRICAS GERAIS ---
    st.subheader("Métricas Gerais")
    total_gmv = df_filtrado['gmv_success'].sum()
    total_clientes = df_filtrado['fk_contact'].nunique()
    total_transacoes = len(df_filtrado)
    gmv_formatado = f"R$ {total_gmv:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    display_segmento = "Todos"
    if len(segmentos_selecionados) == 1:
        display_segmento = segmentos_selecionados[0]
    elif len(segmentos_selecionados) > 1:
        display_segmento = "Múltiplos"

    display_ano = "Todos"
    if len(anos_selecionados) == 1:
        display_ano = str(anos_selecionados[0])
    elif len(anos_selecionados) > 1:
        display_ano = "Múltiplos"

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Segmentos em Análise", value=display_segmento)
    with col2:
        st.metric(label="Anos em Análise", value=display_ano)
    with col3:
        st.metric(label="Faturamento Total", value=gmv_formatado)
    with col4:
        st.metric(label="Total de Clientes", value=f"{total_clientes:,}".replace(",", "."))
    with col5:
        st.metric(label="Total de Transações", value=f"{total_transacoes:,}".replace(",", "."))
    st.write("---")


    with st.expander("Clique aqui para ver a descrição detalhada de cada segmento"):
        st.markdown("""
        * **<span style='color:#E86800; font-weight:bold;'>Super Compradores:</span>** A elite dos clientes. Representam o menor grupo (0.53%), mas com o maior poder de compra e a maior frequência. São os clientes mais valiosos e leais da plataforma. 
        
        * **<span style='color:#9400F7; font-weight:bold;'>Viajantes Inativos:</span>** Representam 30.11% da base, mas são clientes que não realizam uma compra há quase 6 anos em média. Para fins práticos, são considerados clientes perdidos, e o foco para eles seria em campanhas de "win-back" de alto impacto.
        
        * **<span style='color:#EBBC00; font-weight:bold;'>Viajantes Ocasionais:</span>** O maior segmento da base de clientes. São usuários que compram de forma esporádica (frequência de 1.77) e não interagem com a plataforma há um tempo considerável (recência de 572 dias). O principal objetivo para este grupo é reengajamento.
        
        * **<span style='color:#D4A3FF; font-weight:bold;'>Viajantes Promissores:</span>** Um grupo valioso (11.38%) com forte potencial de crescimento. Compram com boa frequência e possuem um gasto significativo. São a base para futuras campanhas de fidelização com o objetivo de elevá-los ao status de Viajantes Frequentes.
        
        * **<span style='color:#00005C; font-weight:bold;'>Viajantes Frequentes:</span>** O núcleo de clientes mais engajados após os Super Compradores. Compram com alta frequência (21 vezes em média) e são recentes, representando uma base fiel e de alto valor que interage constantemente com a plataforma.
        """, unsafe_allow_html=True)

    st.subheader("Tabela Comparativa de Segmentos")

    df_tabela_ano = df_final_app.copy()
    if anos_selecionados:
        df_tabela_ano = df_final_app[df_final_app['Ano'].isin(anos_selecionados)]

    if not df_tabela_ano.empty:
        df_clientes_unicos = df_tabela_ano.drop_duplicates(subset=['fk_contact'])

        tabela_agg_cliente = df_clientes_unicos.groupby('Tipo de Seguimento').agg(
            Gasto_Medio_Cliente=('Valor Monetário (R$)', 'mean'),
            Gasto_Mediano_Cliente=('Valor Monetário (R$)', 'median'),
            Desvio_Padrao_Gasto=('Valor Monetário (R$)', 'std'),
            Recencia_Media=('Recência', 'mean'),
            Frequencia_Media=('Frequência', 'mean'),

        )
        tabela_agg_transacao = df_tabela_ano.groupby('Tipo de Seguimento').agg(
            Ticket_Medio_Compra=('Ticket_Medio_Compra_por_Transacao', 'mean'),
            Ida_e_Volta_Media=('is_ida_e_volta', 'mean'),
            Trecho_Mais_Comum=('Trecho_Anonimo', lambda x: x.mode()[0] if not x.empty else "N/A"),
            Soma_GMV=('gmv_success', 'sum'),
            N_Clientes=('fk_contact', 'nunique')
        )

        tabela_final = pd.concat([tabela_agg_cliente, tabela_agg_transacao], axis=1)
        total_clientes_ano = df_tabela_ano['fk_contact'].nunique()
        if total_clientes_ano > 0:
            tabela_final['Representatividade (%)'] = (tabela_final['N_Clientes'] / total_clientes_ano) * 100
        else:
            tabela_final['Representatividade (%)'] = 0

        tabela_final = tabela_final.reset_index().rename(columns={
            'Tipo de Seguimento': 'Segmento', 'Gasto_Medio_Cliente': 'Gasto Médio (R$)',
            'Gasto_Mediano_Cliente': 'Gasto Mediano (R$)', 'Desvio_Padrao_Gasto': 'Desvio Padrão Gasto (R$)',
            'Ticket_Medio_Compra': 'Ticket Médio (R$)', 'Recencia_Media': 'Recência Média (dias)',
            'Frequencia_Media': 'Frequência Média', 'Ida_e_Volta_Media': '% Ida e Volta',
            'Trecho_Mais_Comum': 'Trecho Mais Comum',

        })
        ordem_colunas = [
            'Segmento', 'Representatividade (%)', 'Gasto Médio (R$)', 'Gasto Mediano (R$)',
            'Desvio Padrão Gasto (R$)', 'Ticket Médio (R$)', 'Recência Média (dias)',
            'Frequência Média', '% Ida e Volta', 'Trecho Mais Comum' # <--- VÍRGULA ADICIONADA AQUI
        ]
        tabela_final = tabela_final[ordem_colunas]
        tabela_para_estilizar = tabela_final.reset_index(drop=True)

        def colorir_primeira_coluna(row):
            cor = PALETA_CORES.get(row['Segmento'], 'black')
            estilo_segmento = f'color: {cor}; font-weight: bold;'
            return [estilo_segmento] + [''] * (len(row) - 1)
        tabela_estilizada = tabela_para_estilizar.style.format({
            'Representatividade (%)': '{:,.2f}%', 'Gasto Médio (R$)': 'R$ {:,.2f}',
            'Gasto Mediano (R$)': 'R$ {:,.2f}', 'Desvio Padrão Gasto (R$)': 'R$ {:,.2f}',
            'Ticket Médio (R$)': 'R$ {:,.2f}', '% Ida e Volta': '{:,.2%}',
            'Recência Média (dias)': '{:,.0f}', 'Frequência Média': '{:,.2f}',
        
        }).apply(colorir_primeira_coluna, axis=1)
        st.dataframe(tabela_estilizada.hide(axis="index"), use_container_width=True)

    else:
        st.warning("Nenhum dado disponível para a seleção de filtros atual.")
    
    st.write("---")
    st.subheader("Sazonalidade Mensal: Vendas (GMV) vs. Número de Transações")
    if not df_filtrado.empty:
        df_timeseries = df_filtrado.set_index('date_purchase')
        monthly_data = df_timeseries.resample('MS').agg(GMV_Mensal=('gmv_success', 'sum'), Total_Transacoes=('nk_ota_localizer_id', 'count'))

        # Datas mínimas e máximas dos dados filtrados
        min_date, max_date = monthly_data.index.min(), monthly_data.index.max()
        
        anos_no_grafico = range(min_date.year, max_date.year + 1)
        # Gerar e filtrar as datas de feriado para estarem dentro do intervalo do gráfico
        natal_dates = pd.to_datetime([f'{year}-12-25' for year in anos_no_grafico])
        carnaval_dates_full = pd.to_datetime(['2014-03-04', '2015-02-17', '2016-02-09', '2017-02-28', '2018-02-13', '2019-03-05', '2020-02-25', '2021-02-16', '2022-03-01', '2023-02-21', '2024-02-13', '2025-03-04'])
        carnaval_dates = [date for date in carnaval_dates_full if min_date <= date <= max_date]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['GMV_Mensal'], name='GMV Mensal (R$)', mode='lines', line=dict(color='#517CED', width=2.5)), secondary_y=False)
        fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data['Total_Transacoes'], name='Total de Transações', mode='lines', line=dict(color="#78A0F8", width=2, dash='dot')), secondary_y=True)
        
        for date in natal_dates:
            fig.add_vline(x=date, line_width=1, line_dash="dash", line_color="red", opacity=0.6)
        for date in carnaval_dates:
            fig.add_vline(x=date, line_width=1, line_dash="dash", line_color="green", opacity=0.6)
            
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='red', dash='dash'), name='Natal'))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='green', dash='dash'), name='Carnaval'))
        fig.update_layout(title_text=None, template='plotly_white', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), hovermode="x unified")
        fig.update_yaxes(title_text="<b>GMV Mensal (R$)</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Total de Transações</b>", secondary_y=True)
        fig.update_xaxes(title_text="<b>Linha do Tempo</b>")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para a seleção de filtros atual.")
    
    st.write("---")
    col_destinos, col_empresas = st.columns(2)
    with col_destinos:
        st.subheader("Top 10 Destinos Populares")
        if not df_filtrado.empty:
            cor_grafico_destinos = COR_NEUTRA
            if len(segmentos_selecionados) == 1:
                cor_grafico_destinos = PALETA_CORES[segmentos_selecionados[0]]
            
            top_destinos = df_filtrado['Destino_Anonima'].value_counts().nlargest(10).reset_index()
            top_destinos.columns = ['Destino', 'Contagem']
            fig_destinos = px.bar(top_destinos.sort_values('Contagem'), x='Contagem', y='Destino', orientation='h', text='Contagem', template='plotly_white')
            fig_destinos.update_traces(marker_color=cor_grafico_destinos, textposition='outside')
            fig_destinos.update_layout(yaxis={'title_text': ''}, xaxis={'title_text': 'Nº de Viagens'}, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_destinos, use_container_width=True)
        else:
            st.warning("Nenhum dado disponível para a seleção de filtros atual.")

    with col_empresas:
        st.subheader("Top 10 Empresas Parceiras")
        if not df_filtrado.empty:
            cor_grafico_empresas = COR_NEUTRA
            if len(segmentos_selecionados) == 1:
                cor_grafico_empresas = PALETA_CORES[segmentos_selecionados[0]]
            
            top_empresas = df_filtrado['fk_departure_ota_bus_company'].value_counts().nlargest(10).reset_index()
            top_empresas.columns = ['Empresa', 'Contagem']
            fig_empresas = px.bar(top_empresas.sort_values('Contagem'), x='Contagem', y='Empresa', orientation='h', text='Contagem', template='plotly_white')
            fig_empresas.update_traces(marker_color=cor_grafico_empresas, textposition='outside')
            fig_empresas.update_layout(yaxis={'title_text': ''}, xaxis={'title_text': 'Nº de Viagens'}, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_empresas, use_container_width=True)
        else:
            st.warning("Nenhum dado disponível para a seleção de filtros atual.")

#====================================================================

# Pagina 2 


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
        arquivos= glob.glob('data/*.parquet')
        
        df = pd.concat([pd.read_parquet(arquivo) for arquivo in arquivos], ignore_index=True)
        
        df['date_purchase'] = pd.to_datetime(df['date_purchase'])
        if 'Ano' not in df.columns:
            df['Ano'] = df['date_purchase'].dt.year
            
        return df
        
    except Exception as e:
        st.error(f"Erro fatal ao carregar os dados. Verifique o ID do arquivo ou a conexão. Detalhe: {e}")
        return None


# --- TÍTULO E INTRODUÇÃO ---
if df_final_app is not None:
    st.title("Módulo 2: Análise Preditiva Unificada")
    st.markdown("Insights acionáveis sobre a probabilidade de compra e o próximo destino dos clientes nos próximos 30 dias.")
    st.write("---")

    # --- BARRA LATERAL (SIDEBAR) COM FILTROS ---
    # st.sidebar.header("Filtros de Análise")
    
    # lista_anos = sorted(df_final_app['Ano'].unique().tolist(), reverse=True)
    # anos_selecionados = st.sidebar.multiselect('Selecione um ou mais Anos:', lista_anos, default=None)
    # lista_segmentos = df_final_app['Tipo de Seguimento'].unique().tolist()
    # segmentos_selecionados = st.sidebar.multiselect('Selecione um ou mais Segmentos:', lista_segmentos, default=None)


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




