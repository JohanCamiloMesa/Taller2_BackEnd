#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cuotas_pendientes.py

Genera un reporte de todos los préstamos que tienen cuotas pendientes.
Guarda el resultado en un archivo CSV llamado cuotas_pendientes.csv.

Contiene la función cuotas_pendientes() que agrupa por préstamo y cliente,
calculando el total de cuotas pendientes y el monto total a pagar.
"""
from typing import List, Dict
import csv
import os
import mysql.connector


def cuotas_pendientes(host: str = None, port: int = None,
                     user: str = None, password: str = None,
                     database: str = None) -> List[Dict[str, str]]:
    """Genera reporte de préstamos con cuotas pendientes.

    La función consulta todos los préstamos que tienen al menos una cuota en estado
    'pendiente', agrupando los resultados por préstamo y cliente. Calcula la cantidad
    de cuotas pendientes y la suma total de montos a pagar para cada préstamo.

    Args:
        host: Servidor MySQL (default: 127.0.0.1 o MYSQL_HOST env)
        port: Puerto MySQL (default: 3306 o MYSQL_PORT env)
        user: Usuario MySQL (default: root o MYSQL_USER env)
        password: Contraseña MySQL (default: E57Nfcl5~3* o MYSQL_PASSWORD env)
        database: Base de datos (default: bancos o MYSQL_DB env)

    Returns:
        Lista de diccionarios con las claves:
        - 'Préstamo': ID del préstamo
        - 'DNI Cliente': DNI del cliente
        - 'Cuotas Pendientes': Cantidad de cuotas pendientes
        - 'Monto Total a Pagar': Suma total formateada con separadores de miles y 2 decimales

    Ejemplo:
        >>> reporte = cuotas_pendientes()
        >>> for item in reporte:
        ...     print(f"Préstamo {item['Préstamo']}: {item['Cuotas Pendientes']} cuotas - {item['Monto Total a Pagar']}")
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
        
        # Query que obtiene préstamos con cuotas pendientes
        # Usa JOINs explícitos: cuota -> prestamo -> usuario
        # Filtra por estado 'pendiente'
        # Agrupa por préstamo y cliente
        # Calcula cantidad de cuotas y suma total de montos
        query = """
            SELECT 
                p.id_prestamo,
                u.dni,
                COUNT(c.id_cuota) AS cuotas_pendientes,
                ROUND(SUM(c.monto), 2) AS monto_total
            FROM cuota c
            JOIN prestamo p ON c.id_prestamo = p.id_prestamo
            JOIN usuario u ON p.id_usuario = u.id_usuario
            WHERE c.estado = 'pendiente'
            GROUP BY p.id_prestamo, u.dni
            ORDER BY p.id_prestamo
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for row in rows:
            id_prestamo, dni, cuotas_pendientes, monto_total = row
            
            # Formatear el monto con separadores de miles y 2 decimales
            monto_formateado = f"$ {monto_total:,.2f}"
            
            result.append({
                'Préstamo': str(id_prestamo),
                'DNI Cliente': dni,
                'Cuotas Pendientes': str(cuotas_pendientes),
                'Monto Total a Pagar': monto_formateado
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
        data: Lista de diccionarios con el reporte de cuotas pendientes
        output_path: Ruta completa del archivo CSV a crear
    """
    fieldnames = ['Préstamo', 'DNI Cliente', 'Cuotas Pendientes', 'Monto Total a Pagar']
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    """Función principal que ejecuta el cálculo y guarda el resultado en CSV."""
    here = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(here, 'cuotas_pendientes.csv')

    print("="*70)
    print("  REPORTE DE CUOTAS PENDIENTES POR PRÉSTAMO")
    print("="*70)
    print("\n🔎 Generando reporte de préstamos con cuotas pendientes...")
    
    data = cuotas_pendientes()
    
    if not data:
        print("\n⚠️  No se encontraron préstamos con cuotas pendientes.")
        return

    _write_csv(data, out_file)
    print(f"\n✅ Archivo generado: {out_file}")
    print(f"   Total de préstamos con cuotas pendientes: {len(data)}")
    
    print(f"\n📊 RESUMEN DE CUOTAS PENDIENTES:")
    print("-"*70)
    print(f"{'Préstamo':<10} {'DNI Cliente':<15} {'Cuotas':<10} {'Monto Total':>20}")
    print("-"*70)
    
    # Mostrar primeras 10 filas
    for item in data[:10]:
        print(f"{item['Préstamo']:<10} {item['DNI Cliente']:<15} "
              f"{item['Cuotas Pendientes']:<10} {item['Monto Total a Pagar']:>20}")
    
    if len(data) > 10:
        print(f"{'...':<10} {'...':<15} {'...':<10} {'...':>20}")
        print(f"\n   (Mostrando 10 de {len(data)} préstamos. Ver archivo CSV para listado completo)")
    
    print("-"*70)
    
    # Estadísticas adicionales
    total_cuotas = sum(int(item['Cuotas Pendientes']) for item in data)
    total_monto = sum(float(item['Monto Total a Pagar'].replace('$', '').replace(',', '').strip()) for item in data)
    
    print(f"\n📈 ESTADÍSTICAS GENERALES:")
    print(f"   • Total de préstamos con cuotas pendientes: {len(data)}")
    print(f"   • Total de cuotas pendientes: {total_cuotas}")
    print(f"   • Monto total a pagar: $ {total_monto:,.2f}")
    print("="*70)


if __name__ == '__main__':
    main()
