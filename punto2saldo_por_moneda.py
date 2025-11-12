#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
saldo_por_moneda.py

Calcula el saldo total de dinero en custodia agrupado por tipo de moneda
y guarda el resultado en saldo_por_moneda.csv.

Contiene la función saldo_por_moneda() que devuelve una lista de diccionarios
con el total de saldos agrupados por moneda. La función está diseñada para
ser importada fácilmente por otros módulos.
"""
from typing import List, Dict
import csv
import os
import mysql.connector


def saldo_por_moneda(host: str = None, port: int = None,
                     user: str = None, password: str = None,
                     database: str = None) -> List[Dict[str, str]]:
    """Consulta la base de datos y calcula el saldo total agrupado por país y moneda.

    La función suma todos los saldos de las cuentas, agrupándolos por país del cliente
    y por el tipo de moneda asociado a través del producto de cada cuenta. Los montos
    se mantienen con precisión de dos decimales y se formatean para legibilidad.

    Args:
        host: Servidor MySQL (default: 127.0.0.1 o MYSQL_HOST env)
        port: Puerto MySQL (default: 3306 o MYSQL_PORT env)
        user: Usuario MySQL (default: root o MYSQL_USER env)
        password: Contraseña MySQL (default: E57Nfcl5~3* o MYSQL_PASSWORD env)
        database: Base de datos (default: bancos o MYSQL_DB env)

    Returns:
        Lista de diccionarios con las claves:
        - 'País': Nombre del país
        - 'Moneda': Nombre completo de la moneda (ej: "Peso Argentino (ARS)")
        - 'Saldo Total': Monto formateado con separadores de miles y 2 decimales

    Ejemplo:
        >>> resultados = saldo_por_moneda()
        >>> for row in resultados:
        ...     print(f"{row['País']} - {row['Moneda']}: {row['Saldo Total']}")
    """
    # Configuración de conexión con valores por defecto desde env vars
    host = host or os.getenv('MYSQL_HOST', '127.0.0.1')
    port = int(port or os.getenv('MYSQL_PORT', '3306'))
    user = user or os.getenv('MYSQL_USER', 'root')
    password = password or os.getenv('MYSQL_PASSWORD', 'E57Nfcl5~3*')
    database = database or os.getenv('MYSQL_DB', 'bancos')

    # Query que suma saldos agrupados por país y moneda
    # Utiliza JOINs para relacionar: Cuenta -> Usuario -> Ciudad -> País
    # Y también: Cuenta -> Producto -> Tipo_Moneda
    query = """
        SELECT 
            p.nombre AS pais_nombre,
            tm.nombre AS moneda_nombre,
            tm.codigo AS moneda_codigo,
            tm.simbolo AS moneda_simbolo,
            ROUND(SUM(c.saldo), 2) AS saldo_total
        FROM cuenta c
        JOIN usuario u ON c.id_usuario = u.id_usuario
        JOIN ciudad ci ON u.id_ciudad = ci.id_ciudad
        JOIN pais p ON ci.id_pais = p.id_pais
        JOIN producto pr ON c.id_producto = pr.id_producto
        JOIN tipo_moneda tm ON pr.id_moneda = tm.id_moneda
        GROUP BY p.id_pais, p.nombre, tm.id_moneda, tm.nombre, tm.codigo, tm.simbolo
        ORDER BY p.nombre, tm.nombre
    """

    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
    except Exception as e:
        print(f"❌ Error al conectar a la DB: {e}")
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for row in rows:
            pais_nombre, moneda_nombre, moneda_codigo, moneda_simbolo, saldo_total = row
            
            # Formatear el nombre completo de la moneda
            moneda_completa = f"{moneda_nombre} ({moneda_codigo})"
            
            # Formatear el saldo con separadores de miles y 2 decimales
            # Formato: 1,234,567.89
            saldo_formateado = f"{moneda_simbolo} {saldo_total:,.2f}"
            
            result.append({
                'País': pais_nombre,
                'Moneda': moneda_completa,
                'Saldo Total': saldo_formateado
            })
        
        cursor.close()
        conn.close()
        return result
        
    except Exception as e:
        print(f"❌ Error ejecutando la consulta: {e}")
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        return []


def _write_csv(data: List[Dict[str, str]], output_path: str) -> None:
    """Escribe la lista de diccionarios en un CSV.
    
    Args:
        data: Lista de diccionarios con las claves 'País', 'Moneda' y 'Saldo Total'
        output_path: Ruta completa del archivo CSV a crear
    """
    fieldnames = ['País', 'Moneda', 'Saldo Total']
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    """Función principal que ejecuta el cálculo y guarda el resultado en CSV."""
    here = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(here, 'saldo_por_moneda.csv')

    print("🔎 Calculando saldo total por país y moneda...")
    data = saldo_por_moneda()
    
    if not data:
        print("⚠️  No se generaron datos (posible error de conexión o consulta).")
        return

    _write_csv(data, out_file)
    print(f"✅ Archivo generado: {out_file}")
    print(f"\n📊 Resumen de saldos por país y moneda:")
    print("-" * 80)
    for row in data:
        print(f"  {row['País']:<20} {row['Moneda']:<30} {row['Saldo Total']:>25}")
    print("-" * 80)


if __name__ == '__main__':
    main()
