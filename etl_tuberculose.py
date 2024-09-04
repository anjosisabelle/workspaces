import pandas as pd
from datetime import datetime

# Leitura dos arquivos CSV
origem = pd.read_csv('origem.csv')
municipio = pd.read_csv('d_municipio.csv')
tempo = pd.read_csv('d_tempo.csv')

# Verificação das colunas dos arquivos CSV
print("Colunas do arquivo origem:", origem.columns)
print("Colunas do arquivo municipio:", municipio.columns)
print("Colunas do arquivo tempo:", tempo.columns)

# Verificação dos valores únicos nas colunas de interesse
print("Valores únicos em tp_entrada:", origem['tp_entrada'].unique())
print("Valores únicos em tp_forma:", origem['tp_forma'].unique())
print("Valores únicos em tp_situacao_encerramento:", origem['tp_situacao_encerramento'].unique())

# Filtragem dos dados conforme os critérios especificados
origem_filtrada = origem[
    ((origem['tp_entrada'] == 1) |  # Caso novo
     (origem['tp_entrada'] == 3) |  # Pós-óbito
     (origem['tp_entrada'].isna())) &
    ((origem['tp_forma'] == 1) |  # Pulmonar
     (origem['tp_forma'] == 2)) &  # Pulmonar + extrapulmonar
    (origem['tp_situacao_encerramento'] != 10) &  # Mudança de Diagnóstico
    (origem['dt_diagnostico_sintoma'] >= '2021-01-01')
]

# Verificação dos dados filtrados
print(f"Dados filtrados: {origem_filtrada.shape[0]} linhas")

# Merge com a tabela de municípios
dados_completos = origem_filtrada.merge(municipio, left_on='co_municipio_residencia_atual', right_on='dmun_codibge')

# Verificação do merge
print(f"Dados após merge: {dados_completos.shape[0]} linhas")

# Conversão da data para o formato desejado
dados_completos['dt_diagnostico_sintoma'] = pd.to_datetime(dados_completos['dt_diagnostico_sintoma'])
dados_completos['mês'] = dados_completos['dt_diagnostico_sintoma'].dt.strftime('%B de %Y')

# Agrupamento dos dados
resultado = dados_completos.groupby(['dmun_municipio', 'mês']).size().reset_index(name='Quantidade')

# Verificação do agrupamento
print(f"Dados agrupados: {resultado.shape[0]} linhas")

# Adição de todos os municípios e meses possíveis
todos_municipios = municipio['dmun_municipio'].unique()
todos_meses = pd.date_range(start='2021-01-01', end=datetime.now(), freq='MS').strftime('%B de %Y')

# Criação de um DataFrame com todos os municípios e meses possíveis
todos_periodos = pd.MultiIndex.from_product([todos_municipios, todos_meses], names=['dmun_municipio', 'mês']).to_frame(index=False)

# Verificação dos nomes das colunas
print("Colunas do DataFrame resultado:", resultado.columns)
print("Colunas do DataFrame todos_periodos:", todos_periodos.columns)

# Merge com o resultado para garantir que todos os períodos estejam presentes
resultado_completo = todos_periodos.merge(resultado, on=['dmun_municipio', 'mês'], how='left').fillna(0)

# Verificação do resultado final
print(f"Resultado final: {resultado_completo.shape[0]} linhas")

# Renomeando as colunas
resultado_completo.columns = ['Município', 'Mês', 'Quantidade']

# Salvando o resultado em um novo arquivo CSV
resultado_completo.to_csv('saida.csv', index=False)
