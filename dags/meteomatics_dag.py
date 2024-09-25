import sys
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


# Adiciona o caminho do diretório "scripts" ao PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))


# Importa as funções da extração, processamento e armazenamento de dados
from data_extraction import extract_meteomatics_data
from data_processing import process_data
from data_storage import store_data

# Define argumentos padrão do DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define o DAG para a coleta de dados da API Meteomatics
dag = DAG(
    'meteomatics_data_pipeline',
    default_args=default_args,
    description='Pipeline para coletar e processar dados da API Meteomatics',
    schedule_interval=timedelta(hours=1),
)

# Define tarefa de extração de dados
extract_task = PythonOperator(
    task_id='extract_meteomatics_data',
    python_callable=extract_meteomatics_data,
    dag=dag,
)

# Define tarefa de processamento de dados
process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag,
)

# Define tarefa de armazenamento de dados
store_task = PythonOperator(
    task_id='store_data',
    python_callable=store_data,
    dag=dag,
)

# Define a ordem de execução das tarefas
extract_task >> process_task >> store_task
