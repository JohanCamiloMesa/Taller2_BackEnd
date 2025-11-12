#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
top_clientes.py

Identifica a los clientes con mayor volumen de transacciones en los últimos 48 meses.
Genera un archivo CSV llamado top_clientes.csv con los 5 clientes más activos.

Contiene la función top_clientes_transacciones() que calcula el ranking de clientes
según el volumen de dinero movido en transferencias y retiros.
"""
from typing import List, Dict
import csv
import os
import mysql.connector
from datetime import datetime


def top_clientes_transacciones(host: str = None, port: int = None,
                                user: str = None, password: str = None,
                                database: str = None) -> List[Dict[str, str]]:
    """Obtiene el top 5 de clientes con mayor volumen de transacciones en los últimos 48 meses.

    La función calcula el total movido por cada cliente considerando solo transacciones
    de tipo 'transferencia' o 'retiro' desde la cuenta de origen en los últimos 48 meses.
    El periodo de tiempo se calcula dinámicamente usando DATE_SUB.

    Args:
        host: Servidor MySQL (default: 127.0.0.1 o MYSQL_HOST env)
        port: Puerto MySQL (default: 3306 o MYSQL_PORT env)
        user: Usuario MySQL (default: root o MYSQL_USER env)
        password: Contraseña MySQL (default: E57Nfcl5~3* o MYSQL_PASSWORD env)
        database: Base de datos (default: bancos o MYSQL_DB env)

    Returns:
        Lista de 5 diccionarios ordenados por volumen (mayor a menor) con las claves:
        - 'Puesto': Posición en el ranking (1-5)
        - 'Cliente': Nombre completo del cliente
        - 'Total Movido': Monto formateado con separadores de miles y 2 decimales

    Ejemplo:
        >>> clientes = top_clientes_transacciones()
        >>> for cliente in clientes:
        ...     print(f"{cliente['Puesto']}. {cliente['Cliente']}: {cliente['Total Movido']}")
    """
    # Configuración de conexión con valores por defecto desde env vars
    host = host or os.getenv('MYSQL_HOST', '127.0.0.1')
    port = int(port or os.getenv('MYSQL_PORT', '3306'))
    user = user or os.getenv('MYSQL_USER', 'root')
    password = password or os.getenv('MYSQL_PASSWORD', 'E57Nfcl5~3*')
    database = database or os.getenv('MYSQL_DB', 'bancos')

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
        
        # Query que calcula el top 5 de clientes por volumen de transacciones
        # Usa DATE_SUB(NOW(), INTERVAL 48 MONTH) para calcular dinámicamente el periodo
        # Solo considera transacciones tipo 'transferencia' o 'retiro'
        # Suma el monto de la cuenta de origen (id_cuenta_origen)
        query = """
            SELECT 
                u.nombre,
                u.apellido,
                ROUND(SUM(t.monto), 2) AS total_movido
            FROM transaccion t
            JOIN cuenta c ON t.id_cuenta_origen = c.id_cuenta
            JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE t.tipo IN ('transferencia', 'retiro')
              AND t.fecha >= DATE_SUB(NOW(), INTERVAL 48 MONTH)
            GROUP BY u.id_usuario, u.nombre, u.apellido
            ORDER BY total_movido DESC
            LIMIT 5
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for idx, row in enumerate(rows, start=1):
            nombre, apellido, total_movido = row
            
            # Formatear el nombre completo del cliente
            cliente_nombre = f"{nombre} {apellido}"
            
            # Formatear el monto con separadores de miles y 2 decimales
            total_formateado = f"$ {total_movido:,.2f}"
            
            result.append({
                'Puesto': str(idx),
                'Cliente': cliente_nombre,
                'Total Movido': total_formateado
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
        data: Lista de diccionarios con el ranking de clientes
        output_path: Ruta completa del archivo CSV a crear
    """
    fieldnames = ['Puesto', 'Cliente', 'Total Movido']
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    """Función principal que ejecuta el cálculo y guarda el resultado en CSV."""
    here = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(here, 'top_clientes.csv')

    print("="*70)
    print("  TOP 5 CLIENTES MÁS ACTIVOS EN TRANSACCIONES")
    print("="*70)
    print("\n🔎 Calculando top 5 clientes (últimos 48 meses)...")
    print("   • Tipos de transacción: transferencia, retiro")
    print("   • Periodo: Últimos 48 meses desde hoy")
    
    data = top_clientes_transacciones()
    
    if not data:
        print("\n⚠️  No se generaron datos (posible error de conexión o consulta).")
        return

    _write_csv(data, out_file)
    print(f"\n✅ Archivo generado: {out_file}")
    print(f"\n📊 TOP 5 CLIENTES MÁS ACTIVOS:")
    print("-"*70)
    print(f"{'Puesto':<8} {'Cliente':<35} {'Total Movido':>20}")
    print("-"*70)
    
    for cliente in data:
        print(f"{cliente['Puesto']:<8} {cliente['Cliente']:<35} {cliente['Total Movido']:>20}")
    
    print("-"*70)


if __name__ == '__main__':
    main()
