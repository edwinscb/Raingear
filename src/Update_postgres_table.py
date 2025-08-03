import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

usuario = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
puerto = os.getenv("DB_PORT")
bd = os.getenv("DB_NAME")

csv_path = './output/sales_predictions.csv' 
tabla_destino = 'sales_predictions'

df = pd.read_csv(csv_path)

conexion = create_engine(f'postgresql+psycopg2://{usuario}:{password}@{host}:{puerto}/{bd}')

df.to_sql(tabla_destino, conexion, if_exists='replace', index=False)

print("✅ CSV cargado exitosamente a la base de datos.")
