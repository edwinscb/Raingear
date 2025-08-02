import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os

try:
    df_pedidos = pd.read_csv("./data/Pedido.csv")
    df_detalles_pedido = pd.read_csv("./data/DetallesPedido.csv")
    df_productos = pd.read_csv("./data/Producto.csv")
    df_categorias = pd.read_csv("./data/Categoria.csv")
    df_marcas = pd.read_csv("./data/Marca.csv")
    df_clima = pd.read_csv("./data/climapedido.csv")
    df_clientes = pd.read_csv("./data/Cliente.csv")
    
    print("✅ Todos los archivos CSV se cargaron correctamente.")
except FileNotFoundError as e:
    print(f"❌ Error al cargar un archivo: {e}. Asegúrate de que todos los archivos CSV estén en la carpeta 'data/'.")
    exit()

df_ventas = pd.merge(df_detalles_pedido, df_pedidos, on="pedido_id", how="left")
df_ventas = pd.merge(df_ventas, df_productos, on="producto_id", how="left")
df_ventas = pd.merge(df_ventas, df_categorias, on="categoria_id", how="left")
df_ventas = pd.merge(df_ventas, df_marcas, on="marca_id", how="left")
df_ventas = pd.merge(df_ventas, df_clientes, on="cliente_id", how="left")

df_ventas["fecha_pedido"] = pd.to_datetime(df_ventas["fecha_pedido"]).dt.date

df_ventas = pd.merge(df_ventas, df_clima, on="pedido_id", how="left")

df_ventas.rename(columns={
    "fecha_pedido": "date",
    "producto_id": "product_id",
    "cantidad": "sales",
    "precio": "price",
    "Nombre_categoria": "category",
    "nombre_marca": "brand",
    "temp_max": "temperature",
    "cliente_id": "customer_id",
    "nombre": "customer_name",
    "apellido": "customer_lastname",
    "email": "customer_email",
    "telefono": "customer_phone",
    "direccion": "customer_address",
    "pais": "customer_country",
    "fecha_registro": "customer_registration_date"
}, inplace=True)

df_ventas['temperature'] = df_ventas.groupby('category')['temperature'].transform(lambda x: x.fillna(x.mean()))

df_ventas.dropna(subset=["temperature", "brand"], inplace=True)

df_ventas["year"] = pd.to_datetime(df_ventas["date"]).dt.year
df_ventas["month"] = pd.to_datetime(df_ventas["date"]).dt.month

features = ["price", "temperature", "year", "month"]
target = "sales"

df_model = df_ventas.copy()
df_model = pd.get_dummies(df_model, columns=['brand'], prefix='brand', drop_first=True)

brand_features = [col for col in df_model.columns if col.startswith('brand_')]
features.extend(brand_features)

X = df_model[features]
y = df_model[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

df_ventas["sales_prediction"] = model.predict(df_model[features])

df_ventas["sales_prediction"] = df_ventas["sales_prediction"].apply(lambda x: max(0, x))

print("✅ Modelo de predicción de ventas entrenado y predicciones generadas.")

final_columns = [
    "date", "product_id", "sales", "price", "category", "temperature", "sales_prediction"
]
df_final = df_ventas[final_columns].copy()

output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
df_final.to_csv(f"{output_dir}/sales_predictions.csv", index=False)
print("✅ Datos transformados con predicciones guardados en './output/sales_predictions.csv'.")
