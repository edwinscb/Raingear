import pandas as pd
import requests
import time
from datetime import date

df_pedidos = pd.read_csv("./data/Pedido.csv")
df_pedidos["fecha_pedido"] = pd.to_datetime(df_pedidos["fecha_pedido"]).dt.date

def obtener_coordenadas(ciudad):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={ciudad}&format=json"
        headers = {"User-Agent": "etl-openmeteo"}
        r = requests.get(url, headers=headers)
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except:
        pass
    return None, None

def obtener_clima(lat, lon, fecha):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={fecha}&end_date={fecha}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&timezone=America/Bogota"
        )
        r = requests.get(url)
        data = r.json()
        if "daily" in data and "temperature_2m_max" in data["daily"]:
            return {
                "temp_max": data["daily"]["temperature_2m_max"][0],
                "temp_min": data["daily"]["temperature_2m_min"][0],
                "precipitacion": data["daily"]["precipitation_sum"][0],
            }
    except:
        return None
    return None

cache_coord = {}
registros = []

for _, fila in df_pedidos.iterrows():
    pedido_id = fila["pedido_id"]
    ciudad = fila["ciudad_pedido"]
    fecha = fila["fecha_pedido"]

    if ciudad not in cache_coord:
        lat, lon = obtener_coordenadas(ciudad)
        if lat is None:
            print(f"❌ No se encontraron coordenadas para: {ciudad}. Usando Bogotá.")
            ciudad = "Bogotá"
            lat, lon = obtener_coordenadas(ciudad)
        cache_coord[ciudad] = (lat, lon)
    else:
        lat, lon = cache_coord[ciudad]

    print(f"📦 Pedido {pedido_id} - {ciudad} ({lat}, {lon}) - {fecha}")
    clima = obtener_clima(lat, lon, fecha)

    if not clima:
        print(f"⚠️ Clima no disponible para {ciudad} el {fecha}. Intentando con clima actual...")
        clima = obtener_clima(lat, lon, date.today())
        if clima:
            clima["nota"] = "clima_actual_usado"
            print(f"✅ Clima encontrado para {ciudad} el {date.today()} (clima actual)")
        else:
            print(f"🚫 Clima actual tampoco disponible para {ciudad}. Usando Medellín.")
            ciudad = "Medellín"
            if ciudad not in cache_coord:
                lat, lon = obtener_coordenadas(ciudad)
                cache_coord[ciudad] = (lat, lon)
            else:
                lat, lon = cache_coord[ciudad]
            clima = obtener_clima(lat, lon, date.today())
            if clima:
                clima["nota"] = "clima_medellin_actual"
                print(f"✅ Clima encontrado para Medellín el {date.today()} (reemplazo final)")
    else:
        print(f"✅ Clima encontrado para {ciudad} el {fecha}")

    if clima:
        registros.append({
            "pedido_id": pedido_id,
            "ciudad": ciudad,
            "fecha": fecha,
            "lat": lat,
            "lon": lon,
            **clima
        })

    time.sleep(1)

df_clima = pd.DataFrame(registros)
df_clima.insert(0, "id", range(1, len(df_clima) + 1))

df_clima.to_csv("./data/climapedido.csv", index=False)
print("✅ Archivo guardado como ./data/climapedido.csv")
