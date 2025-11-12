#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resumen_cliente.py

Crea una vista persistente v_resumen_cliente y genera un reporte CSV con el resumen
de información por cliente (cuentas, préstamos y saldo total).

Contiene las funciones:
- crear_vista(): Crea o reemplaza la vista v_resumen_cliente
- ver_resumen(): Consulta la vista y genera resumen_cliente.csv
"""
from typing import List, Dict, Optional
import csv
import os
import mysql.connector


def crear_vista(host: str = None, port: int = None,
               user: str = None, password: str = None,
               database: str = None) -> bool:
    """Crea o reemplaza la vista v_resumen_cliente en la base de datos.

    La vista agrupa información por cliente mostrando:
    - Nombre completo del cliente
    - Cantidad de cuentas abiertas
    - Cantidad de préstamos contratados
    - Saldo total de todas sus cuentas

    Los clientes sin cuentas o préstamos aparecen con valores 0.

    Args:
        host: Servidor MySQL (default: 127.0.0.1 o MYSQL_HOST env)
        port: Puerto MySQL (default: 3306 o MYSQL_PORT env)
        user: Usuario MySQL (default: root o MYSQL_USER env)
        password: Contraseña MySQL (default: E57Nfcl5~3* o MYSQL_PASSWORD env)
        database: Base de datos (default: bancos o MYSQL_DB env)

    Returns:
        True si la vista se creó exitosamente, False en caso de error

    Ejemplo:
        >>> if crear_vista():
        ...     print("Vista creada exitosamente")
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
        return False

    try:
        cursor = conn.cursor()
        
        # Query para crear o reemplazar la vista
        # Usa LEFT JOINs para incluir todos los usuarios, incluso sin cuentas o préstamos
        # COALESCE convierte NULL a 0 para clientes sin cuentas/préstamos
        create_view_query = """
            CREATE OR REPLACE VIEW v_resumen_cliente AS
            SELECT 
                u.id_usuario,
                CONCAT(u.nombre, ' ', u.apellido) AS nombre_completo,
                COALESCE(COUNT(DISTINCT c.id_cuenta), 0) AS cantidad_cuentas,
                COALESCE(COUNT(DISTINCT p.id_prestamo), 0) AS cantidad_prestamos,
                COALESCE(ROUND(SUM(c.saldo), 2), 0.00) AS saldo_total
            FROM usuario u
            LEFT JOIN cuenta c ON u.id_usuario = c.id_usuario
            LEFT JOIN prestamo p ON u.id_usuario = p.id_usuario
            GROUP BY u.id_usuario, u.nombre, u.apellido
            ORDER BY nombre_completo
        """
        
        cursor.execute(create_view_query)
        conn.commit()
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear la vista: {e}")
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        return False


def ver_resumen(host: str = None, port: int = None,
               user: str = None, password: str = None,
               database: str = None) -> List[Dict[str, str]]:
    """Consulta la vista v_resumen_cliente y retorna todos los registros.

    Esta función lee todos los datos de la vista v_resumen_cliente y los retorna
    como una lista de diccionarios. Los clientes sin cuentas o préstamos aparecen
    con valores 0.

    Args:
        host: Servidor MySQL (default: 127.0.0.1 o MYSQL_HOST env)
        port: Puerto MySQL (default: 3306 o MYSQL_PORT env)
        user: Usuario MySQL (default: root o MYSQL_USER env)
        password: Contraseña MySQL (default: E57Nfcl5~3* o MYSQL_PASSWORD env)
        database: Base de datos (default: bancos o MYSQL_DB env)

    Returns:
        Lista de diccionarios con las claves:
        - 'Nombre Completo': Nombre y apellido del cliente
        - 'Cantidad Cuentas': Número de cuentas abiertas
        - 'Cantidad Préstamos': Número de préstamos contratados
        - 'Saldo Total': Saldo total formateado con separadores de miles y 2 decimales

    Ejemplo:
        >>> resumen = ver_resumen()
        >>> for cliente in resumen:
        ...     print(f"{cliente['Nombre Completo']}: {cliente['Cantidad Cuentas']} cuentas")
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
        
        # Query simple para obtener todos los registros de la vista
        query = """
            SELECT 
                nombre_completo,
                cantidad_cuentas,
                cantidad_prestamos,
                saldo_total
            FROM v_resumen_cliente
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for row in rows:
            nombre_completo, cantidad_cuentas, cantidad_prestamos, saldo_total = row
            
            # Formatear el saldo con separadores de miles y 2 decimales
            saldo_formateado = f"$ {saldo_total:,.2f}"
            
            result.append({
                'Nombre Completo': nombre_completo,
                'Cantidad Cuentas': str(cantidad_cuentas),
                'Cantidad Préstamos': str(cantidad_prestamos),
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
        data: Lista de diccionarios con el resumen de clientes
        output_path: Ruta completa del archivo CSV a crear
    """
    fieldnames = ['Nombre Completo', 'Cantidad Cuentas', 'Cantidad Préstamos', 'Saldo Total']
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    """Función principal que crea la vista y genera el archivo CSV."""
    here = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(here, 'resumen_cliente.csv')

    print("="*70)
    print("  VISTA RESUMEN DE CLIENTE")
    print("="*70)
    
    # Paso 1: Crear o reemplazar la vista
    print("\n🔧 Creando vista v_resumen_cliente...")
    if not crear_vista():
        print("\n❌ Error: No se pudo crear la vista.")
        return
    
    print("✅ Vista creada exitosamente.")
    
    # Paso 2: Consultar la vista y generar el CSV
    print("\n🔎 Consultando vista y generando reporte...")
    data = ver_resumen()
    
    if not data:
        print("\n⚠️  No se encontraron registros en la vista.")
        return

    _write_csv(data, out_file)
    print(f"\n✅ Archivo generado: {out_file}")
    print(f"   Total de clientes: {len(data)}")
    
    print(f"\n📊 RESUMEN DE CLIENTES (Primeros 10):")
    print("-"*70)
    print(f"{'Nombre Completo':<30} {'Cuentas':<10} {'Préstamos':<12} {'Saldo Total':>15}")
    print("-"*70)
    
    # Mostrar primeras 10 filas
    for item in data[:10]:
        print(f"{item['Nombre Completo']:<30} {item['Cantidad Cuentas']:<10} "
              f"{item['Cantidad Préstamos']:<12} {item['Saldo Total']:>15}")
    
    if len(data) > 10:
        print(f"{'...':<30} {'...':<10} {'...':<12} {'...':>15}")
        print(f"\n   (Mostrando 10 de {len(data)} clientes. Ver archivo CSV para listado completo)")
    
    print("-"*70)
    
    # Estadísticas adicionales
    total_cuentas = sum(int(item['Cantidad Cuentas']) for item in data)
    total_prestamos = sum(int(item['Cantidad Préstamos']) for item in data)
    total_saldo = sum(float(item['Saldo Total'].replace('$', '').replace(',', '').strip()) for item in data)
    
    clientes_sin_cuentas = sum(1 for item in data if item['Cantidad Cuentas'] == '0')
    clientes_sin_prestamos = sum(1 for item in data if item['Cantidad Préstamos'] == '0')
    
    print(f"\n📈 ESTADÍSTICAS GENERALES:")
    print(f"   • Total de clientes: {len(data)}")
    print(f"   • Total de cuentas: {total_cuentas}")
    print(f"   • Total de préstamos: {total_prestamos}")
    print(f"   • Saldo total en el sistema: $ {total_saldo:,.2f}")
    print(f"   • Clientes sin cuentas: {clientes_sin_cuentas}")
    print(f"   • Clientes sin préstamos: {clientes_sin_prestamos}")
    print("="*70)


if __name__ == '__main__':
    main()
