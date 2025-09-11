import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gdown  # <-- CORRIGIDO
import os     # <-- CORRIGIDO

st.set_page_config(page_title="Perfil de Clientes", page_icon="📄")

st.title("📄 Perfil de Clientes")
st.write("Você chegou na Perfil de Clientes")


st.set_page_config(
    page_title="ClickClusters - Perfil de Clientes",
    layout="wide"
)

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