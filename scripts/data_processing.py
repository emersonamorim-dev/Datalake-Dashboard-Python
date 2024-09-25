from pyspark.sql import SparkSession
import json

def process_data():
    spark = SparkSession.builder.appName("Processamento Meteomatics").getOrCreate()
    
    # Carrega dados brutos
    raw_data = spark.read.json('/data/raw/processed/data.json')
    
    # Processa os dados para cada zona
    processed_data = raw_data.groupBy("zone").agg(...)
    
    # Salva os dados processados em formato JSON
    processed_data.write.json('/data/processed/data.json')
    
    print("Dados processados com sucesso!")
