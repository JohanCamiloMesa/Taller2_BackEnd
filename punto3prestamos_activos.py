#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prestamos_activos.py

Consulta y muestra los préstamos activos de un cliente específico a partir de su DNI.
Guarda el resultado en un archivo CSV llamado prestamos_activos_[DNI].csv.

Contiene la función prestamos_activos(dni: str) que valida la existencia del DNI
y retorna la información de los préstamos activos del cliente.
"""
from typing import List, Dict, Optional
import csv
import os
import mysql.connector


def prestamos_activos(dni: str, host: str = None, port: int = None,
                      user: str = None, password: str = None,
                      database: str = None) -> Optional[List[Dict[str, str]]]:
    """Consulta los préstamos activos de un cliente por su DNI.

    La función valida la existencia del DNI y retorna la información de todos
    los préstamos con estado 'activo' del cliente. Los montos incluyen el símbolo
    de la moneda y las tasas de interés se muestran con dos decimales y el símbolo %.

    Args:
        dni: Número de DNI del cliente a consultar
        host: Servidor MySQL (default: 127.0.0.1 o MYSQL_HOST env)
        port: Puerto MySQL (default: 3306 o MYSQL_PORT env)
        user: Usuario MySQL (default: root o MYSQL_USER env)
        password: Contraseña MySQL (default: E57Nfcl5~3* o MYSQL_PASSWORD env)
        database: Base de datos (default: bancos o MYSQL_DB env)

    Returns:
        Lista de diccionarios con los datos de los préstamos activos, o None si:
        - El DNI no existe en la base de datos
        - Hay un error de conexión
        
        Cada diccionario contiene las claves:
        - 'ID Préstamo': Identificador del préstamo
        - 'Monto Total': Monto con símbolo de moneda
        - 'Tasa Interés': Tasa con símbolo %
        - 'Fecha Inicio': Fecha de inicio del préstamo
        - 'Fecha Fin': Fecha de finalización del préstamo
        - 'Moneda': Código de la moneda

    Ejemplo:
        >>> prestamos = prestamos_activos('20000001')
        >>> if prestamos:
        ...     for prestamo in prestamos:
        ...         print(f"Préstamo {prestamo['ID Préstamo']}: {prestamo['Monto Total']}")
        >>> else:
        ...     print("Error: Cliente no encontrado")
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
        return None

    try:
        cursor = conn.cursor()
        
        # Primero validar que el DNI existe
        validacion_query = "SELECT id_usuario, nombre, apellido FROM usuario WHERE dni = %s"
        cursor.execute(validacion_query, (dni,))
        usuario = cursor.fetchone()
        
        if not usuario:
            cursor.close()
            conn.close()
            return None  # DNI no encontrado
        
        id_usuario, nombre, apellido = usuario
        
        # Consulta principal: obtener préstamos activos con información de moneda
        # Usa índices en: usuario.dni, prestamo.id_usuario, prestamo.estado
        prestamos_query = """
            SELECT 
                p.id_prestamo,
                p.monto_total,
                p.tasa_interes,
                p.fecha_inicio,
                p.fecha_fin,
                tm.simbolo,
                tm.codigo
            FROM prestamo p
            JOIN usuario u ON p.id_usuario = u.id_usuario
            JOIN tipo_moneda tm ON p.id_moneda = tm.id_moneda
            WHERE u.dni = %s AND p.estado = 'activo'
            ORDER BY p.fecha_inicio DESC
        """
        
        cursor.execute(prestamos_query, (dni,))
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for row in rows:
            id_prestamo, monto_total, tasa_interes, fecha_inicio, fecha_fin, simbolo, codigo = row
            
            # Formatear monto con símbolo de moneda y separadores de miles
            monto_formateado = f"{simbolo} {monto_total:,.2f}"
            
            # Formatear tasa de interés con 2 decimales y símbolo %
            tasa_formateada = f"{tasa_interes:.2f}%"
            
            result.append({
                'ID Préstamo': str(id_prestamo),
                'Monto Total': monto_formateado,
                'Tasa Interés': tasa_formateada,
                'Fecha Inicio': str(fecha_inicio),
                'Fecha Fin': str(fecha_fin),
                'Moneda': codigo
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
        return None


def _write_csv(data: List[Dict[str, str]], output_path: str, cliente_info: str) -> None:
    """Escribe la lista de diccionarios en un CSV.
    
    Args:
        data: Lista de diccionarios con los préstamos activos
        output_path: Ruta completa del archivo CSV a crear
        cliente_info: Información del cliente para incluir como comentario
    """
    fieldnames = ['ID Préstamo', 'Monto Total', 'Tasa Interés', 'Fecha Inicio', 'Fecha Fin', 'Moneda']
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    """Función principal que solicita el DNI por consola y genera el reporte."""
    print("="*70)
    print("  CONSULTA DE PRÉSTAMOS ACTIVOS POR DNI")
    print("="*70)
    
    # Solicitar DNI por consola
    dni = input("\n📋 Ingrese el DNI del cliente: ").strip()
    
    if not dni:
        print("⚠️  Error: Debe ingresar un DNI")
        return
    
    print(f"\n🔎 Buscando préstamos activos para DNI: {dni}...")
    
    # Consultar préstamos activos
    prestamos = prestamos_activos(dni)
    
    if prestamos is None:
        print(f"\n❌ Error: Cliente no encontrado")
        return
    
    if len(prestamos) == 0:
        print(f"\n✅ Cliente encontrado, pero no tiene préstamos activos")
        return
    
    # Generar archivo CSV
    here = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(here, f'prestamos_activos_{dni}.csv')
    
    _write_csv(prestamos, out_file, f"DNI: {dni}")
    
    # Mostrar resultados
    print(f"\n✅ Se encontraron {len(prestamos)} préstamo(s) activo(s)")
    print(f"📄 Archivo generado: {out_file}")
    print("\n" + "-"*70)
    print(f"{'ID':<8} {'Monto Total':<20} {'Tasa':<10} {'Inicio':<12} {'Fin':<12} {'Moneda':<8}")
    print("-"*70)
    
    for p in prestamos:
        print(f"{p['ID Préstamo']:<8} {p['Monto Total']:<20} {p['Tasa Interés']:<10} "
              f"{p['Fecha Inicio']:<12} {p['Fecha Fin']:<12} {p['Moneda']:<8}")
    
    print("-"*70)


if __name__ == '__main__':
    main()
