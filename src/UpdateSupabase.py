import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
table = os.getenv("SUPABASE_TABLE") 

if not url or not key:
    raise ValueError("❌ Faltan variables SUPABASE_URL o SUPABASE_SERVICE_KEY en el .env")
if not table:
    raise ValueError("❌ Falta la variable SUPABASE_TABLE en el .env")

print("🔗 URL:", url)
print("🔐 Clave cargada:", "Sí" if key else "No")
print("📋 Tabla destino:", table)

supabase: Client = create_client(url, key)

csv_file = './output/sales_predictions.csv' 
df = pd.read_csv(csv_file)

for row in df.to_dict(orient="records"):
    try:
        response = supabase.table(table).insert(row).execute()
        print(f"✅ Insertado: {response.data}")
    except Exception as e:
        print(f"❌ Error al insertar: {e}")




print("🎉 Proceso finalizado.")