# conexion_bancos.py

import mysql.connector
import pandas as pd

def conectar():
    """Establece la conexión con la base de datos."""
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",        # Servidor
            port=3306,               # Puerto
            user="root",             # Usuario MySQL
            password="E57Nfcl5~3*",             # Contraseña MySQL
            database="bancos"        # Base de datos
        )
        if conexion.is_connected():
            print("✅ Conectado a la base de datos")
            return conexion
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar: {e}")
        return None

def consultar(conexion):
    """Ejecuta una consulta de ejemplo y muestra resultados."""
    try:
        query = "SELECT * FROM producto;"
        df = pd.read_sql(query, con=conexion)
        print("\n📊 Primeras transacciones:")
        print(df)
        print(f"El tamaño del DataFrame es: {df.shape}")
    except Exception as e:
        print(f"❌ Error en la consulta: {e}")

def main():
    conexion = conectar()
    if conexion:
        consultar(conexion)
        conexion.close()
        print("\n🔒 Conexión cerrada")

if __name__ == "__main__":
    main()
