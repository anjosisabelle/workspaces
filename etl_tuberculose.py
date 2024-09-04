
import pandas as pd

def carregar_dados(origem_path):
    return pd.read_csv(origem_path)

def filtrar_dados(origem_df):
    # Filtrar os dados conforme os critérios especificados
    filtered_df = origem_df[
        (origem_df['tp_entrada'].isin(['Caso novo', 'Pós-óbito', 'Desconhecido'])) &
        (origem_df['tp_forma'].isin(['Pulmonar', 'Pulmonar + extrapulmonar'])) &
        (origem_df['tp_situacao_encerramento'] != 'Mudança de Diagnóstico') &
        (origem_df['dt_diagnostico_sintoma'] >= '2021-01-01')
    ]
    # Converter a coluna 'dt_diagnostico_sintoma' para datetime
    filtered_df.loc[:, 'dt_diagnostico_sintoma'] = pd.to_datetime(filtered_df['dt_diagnostico_sintoma'])
    # Criar a coluna 'mês' no formato "<Mês> de <Ano>"
    filtered_df.loc[:, 'mês'] = filtered_df['dt_diagnostico_sintoma'].dt.strftime('%B de %Y')
    return filtered_df

def agregar_dados(filtered_df, d_municipio_df):
    # Mesclar os dados para obter o nome do município
    merged_df = filtered_df.merge(d_municipio_df, left_on='co_municipio_residencia_atual', right_on='dmun_codibge')
    # Agrupar os dados por município e mês e contar a quantidade de casos
    result_df = merged_df.groupby(['dmun_municipio', 'mês']).size().reset_index(name='Quantidade')
    return result_df

def preencher_dados_faltantes(result_df, municipios_goias, meses):
    # Criar um DataFrame com todos os municípios e meses possíveis
    full_index = pd.MultiIndex.from_product([municipios_goias, meses], names=['dmun_municipio', 'mês'])
    full_df = pd.DataFrame(index=full_index).reset_index()
    # Mesclar com o DataFrame resultante para preencher os dados faltantes com zero
    final_df = full_df.merge(result_df, on=['dmun_municipio', 'mês'], how='left').fillna(0)
    return final_df

def salvar_dados(final_df, saida_path):
    final_df.to_csv(saida_path, index=False)

if __name__ == '__main__':
    origem_path = 'origem.csv'
    saida_path = 'saida.csv'
    d_municipio_data = {
        'dmun_codibge': [5200100, 5200200, 5200300, 5200400, 5200500],
        'dmun_municipio': ['Município A', 'Município B', 'Município C', 'Município D', 'Município E']
    }
    municipios_goias = ['Município A', 'Município B', 'Município C', 'Município D', 'Município E']
    
    origem_df = carregar_dados(origem_path)
    filtered_df = filtrar_dados(origem_df)
    d_municipio_df = pd.DataFrame(d_municipio_data)
    result_df = agregar_dados(filtered_df, d_municipio_df)
    meses = result_df['mês'].unique()
    final_df = preencher_dados_faltantes(result_df, municipios_goias, meses)
    salvar_dados(final_df, saida_path)
