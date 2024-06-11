# Gaming Recommendation

https://gamingrecommendation.streamlit.app/

Projeto voltado a recomendação de jogos utilizando K-Prototype e o índice de Jaccard.

## Setup
A versão do Python utilizado nesse projeto foi a `3.12.3` (https://www.python.org/downloads/release/python-3123/). Todas as bibliotecas necessárias para instalação estão no arquivo de texto `requirements.txt` e para a instalação basta executar `pip install -r requirements.txt` pelo terminal. Também é necessário a instalação do ambiente de desenvolvimento Jupyter Notebook (https://jupyter.org/installs) para a visualização e execução do código da pasta `2 - Clustering Gaming Database`.

## 1 - Base de dados
A base de dados utilizada foi a do IGDB (https://www.igdb.com), disponibilizada através de uma API própria do site. O código utilizado para extrair os dados está na pasta `1 - Scraping Gaming Database`, sendo necessário a inclusão de credenciais para a extração da base de dados (id do cliente e o token de acesso), o IGDB disponibiliza um tutorial de como conseguir através do site da API (https://api-docs.igdb.com/#getting-started). Após conseguir as credenciais, é necessário preencher o arquivo JSON chamado `keys` dentro da pasta `cred` para o código de extração dos dados funcionar. Por fim, após a execução do código, os dados da API vão ficar disponibilizados na pasta `Databases`.

## 2 - Clusterização e Similaridade
A pasta `2 - Clustering Gaming Database` contém o código para criação do banco de dados SQLite para gerar recomendações dos jogos. A recomendação utiliza o modelo de Machine Learning K-Prototype para realizar a clusterização dos dados e o índice de Jaccard para obter a similaridade de cada linha do dataset. Após a execução do código, o banco de dados vai ficar disponibilizado na pasta `Databases`.

## 3 - Visualização
A visualização do projeto foi criada através da biblioteca chamada Streamlit que permite criar aplicações web interativas para visualização dos dados. Para executar o código de visualização, é necessário executar o comando `streamlit run streamlit_app.py` pelo terminal na pasta `3 - Deploy with Streamlit`.
