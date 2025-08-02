import pandas as pd
import requests
import time

df_pedidos = pd.read_csv("./data/Pedido.csv")
df_pedidos["fecha_pedido"] = pd.to_datetime(df_pedidos["fecha_pedido"]).dt.date
df_ciudades_fechas = df_pedidos[["ciudad_pedido", "fecha_pedido"]].dropna().drop_duplicates()

def obtener_coordenadas(ciudad):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={ciudad}&format=json"
        headers = {"User-Agent": "etl-openmeteo"}
        r = requests.get(url, headers=headers)
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except:
        return None, None
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
                "fecha": fecha,
                "lat": lat,
                "lon": lon,
                "temp_max": data["daily"]["temperature_2m_max"][0],
                "temp_min": data["daily"]["temperature_2m_min"][0],
                "precipitacion": data["daily"]["precipitation_sum"][0],
            }
    except:
        return None
    return None

# Extraer clima por ciudad y fecha
registros = []
for _, fila in df_ciudades_fechas.iterrows():
    ciudad = fila["ciudad_pedido"]
    fecha = fila["fecha_pedido"]

    lat, lon = obtener_coordenadas(ciudad)
    if lat is None:
        print(f"❌ No se encontraron coordenadas para: {ciudad}")
        continue

    print(f"🌍 {ciudad} ({lat}, {lon}) - {fecha}")
    clima = obtener_clima(lat, lon, fecha)
    if clima:
        clima["ciudad"] = ciudad
        registros.append(clima)
    else:
        print(f"⚠️ Clima no disponible para {ciudad} el {fecha}")

    time.sleep(1)  # evitar rate limit de Nominatim y Open-Meteo

# Guardar resultados
df_clima = pd.DataFrame(registros)
df_clima.to_csv("./data/clima.csv", index=False)
print("✅ Clima histórico guardado en ./data/clima.csv")
