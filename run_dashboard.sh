#!/bin/bash

# Função para checar o status da execução e exibir uma mensagem em caso de erro
check_status() {
    if [ $? -ne 0 ]; then
        echo "Erro ao executar $1. Abortando."
        exit 1
    fi
}

# Executar o script de extração de dados
echo "Executando extração de dados..."
python3 scripts/data_extraction.py
check_status "extração de dados"


# Exibir URLs para acesso aos serviços
echo "Aplicação iniciada! Acesse o dashboard em http://localhost:8501 e o Airflow em http://localhost:8080"
