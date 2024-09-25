from pyspark.sql import SparkSession
import json

def process_data():
    spark = SparkSession.builder.appName("Processamento Meteomatics").getOrCreate()
    
    # Carregar dados brutos
    raw_data = spark.read.json('/data/raw/processed/data.json')
    
    # Processar os dados para cada zona
    processed_data = raw_data.groupBy("zone").agg(...)
    
    # Salvar os dados processados em formato JSON
    processed_data.write.json('/data/processed/data.json')
    
    print("Dados processados com sucesso!")
