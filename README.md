# ETL de Casos Novos de Tuberculose Pulmonar por Município em Goiás

Este repositório contém um script de ETL (Extract, Transform, Load) que processa o arquivo `origem.csv` e gera um arquivo `saida.csv` com a quantidade de casos novos de tuberculose pulmonar por município em Goiás, agrupados por mês.

O script utiliza a biblioteca Pandas para ler o arquivo de origem, filtrar os dados de acordo com os critérios especificados, agrupar os dados por município e mês, e criar o arquivo de saída.

Os requisitos atendidos pelo script são:

* Uma coluna chamada `município` com o nome de cada município por extenso.
* Uma coluna chamada `mês` com o período por extenso no formato `<Mês> de <Ano>`.
* Uma coluna chamada `Quantidade` com a quantidade de casos novos de tuberculose pulmonar por município e mês.
* Apenas dados a partir de 2021.
* Todos os 246 municípios de Goiás são incluídos, mesmo que não tenham valores para serem apresentados.

Para executar o script, basta rodar o arquivo Python e o arquivo `saida.csv` será gerado automaticamente.
