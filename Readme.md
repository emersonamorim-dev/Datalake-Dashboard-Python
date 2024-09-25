### Datalake Dashboard Python - Minsait com Meteomatics - FIAP 🚀 🔄 🌐
Codificação em Python com Streamlit para um projeto onde implementei um Datalake para coleta, processamento e armazenamento de dados meteorológicos utilizando a API da Meteomatics, usado Python com FastAPI e diversas ferramentas para orquestração, automação e visualização.

##### Arquitetura da Aplicação
A imagem fornecida ilustra a estrutura do projeto, que pode ser resumida nos seguintes componentes principais:

![](https://raw.githubusercontent.com/emersonamorim-dev/Datalake-Dashboard-Python/refs/heads/main/diagrama/Arquitetura-Modular.png)


- Configuração: Arquivos YAML centralizam parâmetros e credenciais para acesso à API da Meteomatics e outras configurações gerais.
- Ambiente Virtual (venv): Isola as dependências do projeto, garantindo reprodutibilidade.
- Docker: Contêineriza a aplicação para facilitar implantação e portabilidade.
- Airflow: Orquestra o fluxo de trabalho, agendando e monitorando as tarefas de extração, processamento e armazenamento de dados.
- Scripts de Processamento: Implementam a lógica de coleta de dados da Meteomatics, transformações, limpeza e armazenamento em formato estruturado (JSON).
- Dashboard: Interface web (construída com Dash) para visualização e exploração dos dados processados.

#### Tecnologias Utilizadas
- Python: Linguagem principal para desenvolvimento dos scripts de processamento e do dashboard.
- Meteomatics API: Fonte dos dados meteorológicos.
- Airflow: Orquestração do fluxo de trabalho.
- Docker: Contêinerização da aplicação.
- Dash: Criação do dashboard interativo.
- Pandas: Manipulação e análise de dados.
- WSL 2 com Ubuntu 24.04

#### Como Executar
1. Clone o Repositório:
```
git clone https://github.com/emersonamorim-dev/Datalake-Dashboard-Python.git
```

```
cd Datalake-Dashboard-Python
```

2. Crie o Ambiente Virtual e Instale as Dependências:

```
python -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

3. Executar aplicação

Edite o arquivo com seu Usuário e Senha

```
data_extraction.py
```

#### Usuário e senha da Meteomatics
username = 'SeuUsuario'  
password = 'SuaSenha'  


#### Rode o Comando abaixo para extrair os Dados da Meteomatics

- Comando para permissão
```
chmod +x ./run_dashboard.sh
```

- Comando para instalar o GeoPandas
```
pip install geopandas
```

- Comando para rodar aplicação
```
./run_dashboard.sh
```

Isso vai gerar um Arquivo data.json no diretório: data/raw/processed/data.json com dados na data atual da API da
Meteomatics.
Lembrando o código data_extraction.py está configurado para acessar os dados até a seguinte datas:

##### Período de tempo de interesse 
start_date = "2024-09-24"
end_date = "2024-10-05"

Como a conta é Trial é preciso verificar seu tempo ativo na Meteomatics para uso.

##### Rodar o Dashboard
```
streamlit run dashboard/app.py
```

#### Acesse o Dashboar no seguinte endereço:

- Local URL: 
```
http://localhost:8503
```

#### Caso queira subir o Docker em Container para Acessar o Apache Airflow

```
docker-compose up -d
```

#### Comandos caso queira entrar dentro Container do Apache Airflor
```
docker exec -it airflow-webserver bash
```

- Copiar arquivos dentro Container
```
cp -r /opt/airflow/scripts /opt/airflow/dags/scripts
```

- Vericar se os arquivos estão dentro do Container
```
docker exec -it airflow-webserver ls /opt/airflow/dags
```


- Força restart do Apache Airflow fora do Container
```
docker-compose restart airflow-webserver airflow-scheduler
```

- Acessar o Containar via Root para instalar pacotes:

- Listar Containar Ativos
```
docker ps

```
```
docker exec -it --user root seuIDcontainer bash
```

#### Para derrubar o Container
```
docker-compose down
```

#### Observação para Implementar
Falta corrigir erros no Apache Airflow e aplicação não está integrada com MongoDB.


#### Conclusão
Este projeto de Datalake - Minsait com uso de Meteomatics para trabalho na FIAP, combinando a riqueza dos dados meteorológicos da Meteomatics com a flexibilidade do Python e o poder de ferramentas como Airflow e Docker, oferece uma base sólida para coleta, processamento, armazenamento e visualização de informações meteorológicas. A arquitetura modular e escalável permite a expansão e adaptação a diferentes necessidades, enquanto a interface do dashboard possibilita a exploração e análise interativa dos dados.

Com o desenvolvimento contínuo, incluindo a implementação de testes, monitoramento, segurança aprimorada e otimizações para escalabilidade, este datalake tem o potencial de se tornar uma ferramenta valiosa para diversas aplicações, desde previsões meteorológicas até estudos climáticos e tomada de decisões estratégicas em setores como agricultura, energia e transporte.

Ao fornecer uma estrutura organizada e eficiente para lidar com dados meteorológicos, este projeto contribui para um melhor entendimento dos padrões climáticos e seus impactos, abrindo portas para novas descobertas e inovações em áreas cruciais para a sociedade e o meio ambiente.


### Desenvolvido por:
Emerson Amorim [@emerson-amorim-dev](https://www.linkedin.com/in/emerson-amorim-dev/)
