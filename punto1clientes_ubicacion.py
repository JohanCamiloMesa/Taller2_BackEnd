#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clientes_ubicacion.py

Genera un reporte CSV `clientes_ubicacion.csv` con las columnas:
Cliente, Ciudad, País

Contiene la función clientes_por_ubicacion() que devuelve una lista de
diccionarios y usa JOINs explícitos en la consulta. El script es
completamente ejecutable por sí mismo.
"""
from typing import List, Dict
import csv
import os
import argparse
import traceback
import mysql.connector


def clientes_por_ubicacion(host: str = None, port: int = None,
                           user: str = None, password: str = None,
                           database: str = None, verbose: bool = False) -> List[Dict[str, str]]:
    """Consulta la base de datos y devuelve la lista de clientes con su ciudad y país.

    Requisitos cumplidos:
    - El nombre completo (nombre + apellido) se devuelve en un solo campo 'Cliente'.
    - Se usan JOINs explícitos en la consulta.
    - Se aplica DISTINCT para evitar duplicados.

    Retorna:
        Lista de diccionarios con las claves: 'Cliente', 'Ciudad', 'País'
    """
    # Use lowercase table names to match the actual DB tables (some MySQL setups are case-sensitive).
    query = (
        "SELECT DISTINCT CONCAT(u.nombre, ' ', u.apellido) AS Cliente, "
        "c.nombre AS Ciudad, p.nombre AS Pais "
        "FROM usuario u "
        "JOIN ciudad c ON u.id_ciudad = c.id_ciudad "
        "JOIN pais p ON c.id_pais = p.id_pais "
        "ORDER BY p.nombre, c.nombre, Cliente"
    )

    # Allow overriding from environment variables when None provided
    host = host or os.getenv('MYSQL_HOST', '127.0.0.1')
    port = int(port or os.getenv('MYSQL_PORT', '3306'))
    user = user or os.getenv('MYSQL_USER', 'root')
    password = password or os.getenv('MYSQL_PASSWORD', 'E57Nfcl5~3*')
    database = database or os.getenv('MYSQL_DB', 'bancos')

    try:
        conn = mysql.connector.connect(host=host, port=port, user=user,
                                       password=password, database=database)
    except Exception as e:
        print(f"❌ Error al conectar a la DB: {e}")
        if verbose:
            traceback.print_exc()
        return []

    # If verbose, print some connection diagnostics (server version, tables, counts)
    if verbose:
        try:
            print("--- Diagnóstico de conexión ---")
            try:
                print(f"Server version: {conn.get_server_info()}")
            except Exception:
                # Some connectors may not implement get_server_info
                pass
            diag_cur = conn.cursor()
            diag_cur.execute("SHOW TABLES")
            tables = [r[0] for r in diag_cur.fetchall()]
            print(f"Tablas en la BD '{database}': {tables}")
            # Try counting rows in Usuario (if the table exists)
            # Check case-insensitively for the usuario table
            tbls_lc = [t.lower() for t in tables]
            if 'usuario' in tbls_lc:
                # Use the actual table name string as returned by SHOW TABLES
                actual_usuario = tables[tbls_lc.index('usuario')]
                diag_cur.execute(f"SELECT COUNT(*) FROM `{actual_usuario}`")
                cnt = diag_cur.fetchone()[0]
                print(f"Filas en Usuario: {cnt}")
            diag_cur.close()
            print("--- Fin diagnóstico ---")
        except Exception as e:
            print(f"⚠️  No se pudo ejecutar diagnóstico adicional: {e}")
            traceback.print_exc()

    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        result: List[Dict[str, str]] = []
        for row in rows:
            # row: (Cliente, Ciudad, Pais)
            cliente, ciudad, pais = row
            result.append({
                'Cliente': cliente,
                'Ciudad': ciudad,
                'País': pais
            })
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"❌ Error ejecutando la consulta: {e}")
        if verbose:
            traceback.print_exc()
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        return []


def _write_csv(data: List[Dict[str, str]], output_path: str) -> None:
    """Escribe la lista de diccionarios en un CSV con encabezado Cliente, Ciudad, País.
    Usa UTF-8-sig para compatibilidad con Excel (BOM).
    """
    fieldnames = ['Cliente', 'Ciudad', 'País']
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description='Generar clientes_ubicacion.csv')
    parser.add_argument('--host')
    parser.add_argument('--port', type=int)
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--database')
    parser.add_argument('--verbose', action='store_true', help='Mostrar trazas completas en caso de error')
    args = parser.parse_args()

    # Ejecuta la función y escribe el CSV en la carpeta del script
    here = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(here, 'clientes_ubicacion.csv')

    print("🔎 Ejecutando consulta de clientes por ubicación...")
    data = clientes_por_ubicacion(host=args.host, port=args.port, user=args.user,
                                  password=args.password, database=args.database,
                                  verbose=args.verbose)
    if not data:
        print("⚠️  No se generaron datos (posible error de conexión o consulta).")
        if args.verbose:
            print("Sugerencias: revisar que el servidor MySQL esté en ejecución, las credenciales, y que la base 'bancos' exista con las tablas cargadas.")
        return

    _write_csv(data, out_file)
    print(f"✅ Archivo generado: {out_file} ({len(data)} filas)")


if __name__ == '__main__':
    main()
