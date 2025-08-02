import pandas as pd
import os
archivo_excel = "./data/data.xlsx"

hojas = pd.read_excel(archivo_excel, sheet_name=None)
os.makedirs("./data", exist_ok=True)
for nombre_hoja, dataframe in hojas.items():
    nombre_csv = f"./data/{nombre_hoja}.csv"
    dataframe.to_csv(nombre_csv, index=False)
    print(f"✅ Hoja '{nombre_hoja}' guardada como {nombre_csv}")
