import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuração da Página ---
st.set_page_config(
    page_title="Judicialização da Saúde no Brasil",
    layout="wide",
    initial_sidebar_state="expanded"
)

def carregar_dados_simulados():
    """Cria um DataFrame simulado para demonstração."""
    data = {
        'AnoDecisao': [2018, 2019, 2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024, 2023, 2022, 2021, 2020, 2023, 2022],
        'TipoPedido': ['Medicamento', 'Tratamento', 'Medicamento', 'Insumo', 'Medicamento', 'Cirurgia', 'Medicamento', 'Tratamento', 'Medicamento', 'Medicamento', 'Tratamento', 'Medicamento', 'Insumo', 'Tratamento', 'Medicamento', 'Medicamento', 'Cirurgia'],
        'Tribunal': ['TJSP', 'TJRJ', 'TJMG', 'TJSP', 'TJDF', 'TJRJ', 'TJSP', 'TJRS', 'TJMG', 'TJSP', 'TJRJ', 'TJSP', 'TJMG', 'TJRS', 'TJSP', 'TJDF', 'TJRJ'],
        'ValorCausa': [15000.00, 50000.00, 5000.00, 2500.00, 8000.00, 100000.00, 7500.00, 30000.00, 6000.00, 12000.00, 45000.00, 9000.00, 3000.00, 15000.00, 5500.00, 7000.00, 85000.00],
        'ResultadoJulgamento': ['Procedente', 'Improcedente', 'Procedente', 'Procedente', 'Procedente', 'Improcedente', 'Procedente', 'Procedente', 'Procedente', 'Procedente', 'Improcedente', 'Procedente', 'Procedente', 'Improcedente', 'Procedente', 'Procedente', 'Improcedente'],
        'FundamentoLegal': ['Art. 196 CF', 'Tema 106 STJ', 'Art. 196 CF', 'Art. 196 CF', 'Art. 196 CF', 'Súmula X', 'Art. 196 CF', 'Tema 106 STJ', 'Art. 196 CF', 'Art. 196 CF', 'Tema 106 STJ', 'Art. 196 CF', 'Art. 196 CF', 'Tema 106 STJ', 'Art. 196 CF', 'Art. 196 CF', 'Súmula Y']
    }
    df = pd.DataFrame(data)
    
    # Tratamento de dados
    df['Tribunal'] = df['Tribunal'].str.strip().str.capitalize()
    df['ResultadoJulgamento'] = df['ResultadoJulgamento'].str.strip().str.capitalize()
    df['AnoDecisao'] = df['AnoDecisao'].astype(int)
    
    return df

@st.cache_data
def analise_evolucao(df):
    """Gera o gráfico de evolução anual."""
    acoes_por_ano = df.groupby('AnoDecisao').size().reset_index(name='TotalAcoes')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=acoes_por_ano, x='AnoDecisao', y='TotalAcoes', marker='o', color='darkblue', ax=ax)
    ax.set_title('Evolução do Número de Decisões Judiciais por Ano')
    ax.set_xlabel('Ano da Decisão')
    ax.set_ylabel('Número Total de Ações')
    ax.set_xticks(acoes_por_ano['AnoDecisao'])
    plt.close(fig) # Fecha a figura Matplotlib para o Streamlit exibi-la
    return fig

@st.cache_data
def analise_comparativa_tribunal(df):
    """Gera o gráfico de deferimento por tribunal (barras empilhadas)."""
    comparacao_tribunal = df.groupby(['Tribunal', 'ResultadoJulgamento']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    comparacao_tribunal[['Procedente', 'Improcedente']].plot(
        kind='bar',
        stacked=True,
        ax=ax,
        color=['#4CAF50', '#F44336'] # Verde/Vermelho
    )
    ax.set_title('Distribuição dos Resultados por Tribunal')
    ax.set_xlabel('Tribunal')
    ax.set_ylabel('Número de Decisões')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Resultado', labels=['Deferido (Procedente)', 'Indeferido (Improcedente)'])
    plt.tight_layout()
    plt.close(fig)
    return fig

# --- Corpo Principal da Aplicação Streamlit ---

# 1. Carregar dados (simulados ou de um arquivo real)
df = carregar_dados_simulados()

st.title("⚖️ Judicialização da Saúde no Brasil: Análise Baseada em Dados")
st.markdown("""
Esta aplicação analisa dados de processos judiciais de saúde, buscando padrões nas decisões de fornecimento de medicamentos e tratamentos.
""")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🛠️ Filtros de Análise")
ano_min = int(df['AnoDecisao'].min())
ano_max = int(df['AnoDecisao'].max())

anos_selecionados = st.sidebar.slider(
    'Selecione o Intervalo de Anos',
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_max)
)

tribunais_selecionados = st.sidebar.multiselect(
    'Selecione os Tribunais',
    options=df['Tribunal'].unique().tolist(),
    default=df['Tribunal'].unique().tolist()
)

# Aplicar filtros
df_filtrado = df[
    (df['AnoDecisao'] >= anos_selecionados[0]) & 
    (df['AnoDecisao'] <= anos_selecionados[1]) &
    (df['Tribunal'].isin(tribunais_selecionados))
]

st.info(f"Mostrando {len(df_filtrado)} registros filtrados.")

# --- Seções de Análise ---

## 📊 Evolução Temporal
st.header("1. Evolução do Volume de Decisões")
if not df_filtrado.empty:
    st.pyplot(analise_evolucao(df_filtrado))
else:
    st.warning("Nenhum dado encontrado com os filtros aplicados para esta seção.")

st.markdown("---")

## ⚖️ Comparação entre Tribunais
st.header("2. Taxa de Deferimento por Tribunal")
if not df_filtrado.empty:
    st.pyplot(analise_comparativa_tribunal(df_filtrado))
else:
    st.warning("Nenhum dado encontrado com os filtros aplicados para esta seção.")

st.markdown("---")

## 📃 Dados de Entrada
st.header("3. Visualização dos Dados")
st.dataframe(df_filtrado)
