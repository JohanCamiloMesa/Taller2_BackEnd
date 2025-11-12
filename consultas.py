#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
consultas.py

Contiene las seis funciones principales del taller que generan reportes
en formato CSV desde la base de datos bancaria.

Cada función es independiente, reutilizable y guarda sus resultados en
un archivo CSV específico.
"""
from typing import List, Dict, Optional
import csv
import os
from database import get_connection


def clientes_por_ubicacion(host: str = None, port: int = None,
                           user: str = None, password: str = None,
                           database: str = None) -> List[Dict[str, str]]:
    """Punto 1 - Obtiene un reporte de clientes agrupados por ubicación geográfica.
    
    Genera un listado de todos los clientes con su ciudad y país correspondiente,
    utilizando JOINs explícitos y eliminando duplicados. Los resultados se ordenan
    alfabéticamente por país, ciudad y nombre de cliente.
    
    Args:
        host: Servidor MySQL (opcional)
        port: Puerto MySQL (opcional)
        user: Usuario MySQL (opcional)
        password: Contraseña MySQL (opcional)
        database: Base de datos (opcional)
    
    Returns:
        List[Dict[str, str]]: Lista de diccionarios con las claves:
            - 'Cliente': Nombre completo del cliente
            - 'Ciudad': Ciudad de residencia
            - 'País': País de residencia
    
    CSV generado: clientes_ubicacion.csv
    
    Ejemplo de retorno:
        [
            {'Cliente': 'Juan Pérez', 'Ciudad': 'Buenos Aires', 'País': 'Argentina'},
            {'Cliente': 'María García', 'Ciudad': 'Bogotá', 'País': 'Colombia'}
        ]
    """
    try:
        conn = get_connection(host, port, user, password, database)
        cursor = conn.cursor()
        
        query = """
            SELECT DISTINCT
                CONCAT(u.nombre, ' ', u.apellido) AS Cliente,
                c.nombre AS Ciudad,
                p.nombre AS Pais
            FROM usuario u
            JOIN ciudad c ON u.id_ciudad = c.id_ciudad
            JOIN pais p ON c.id_pais = p.id_pais
            ORDER BY p.nombre, c.nombre, Cliente
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for row in rows:
            cliente, ciudad, pais = row
            result.append({
                'Cliente': cliente,
                'Ciudad': ciudad,
                'País': pais
            })
        
        cursor.close()
        conn.close()
        
        # Guardar en CSV
        _write_csv(result, 'clientes_ubicacion.csv', 
                  ['Cliente', 'Ciudad', 'País'])
        
        return result
        
    except Exception as e:
        print(f"❌ Error en clientes_por_ubicacion: {e}")
        return []


def saldo_por_moneda(host: str = None, port: int = None,
                    user: str = None, password: str = None,
                    database: str = None) -> List[Dict[str, str]]:
    """Punto 2 - Calcula el saldo total agrupado por país y tipo de moneda.
    
    Suma los saldos de todas las cuentas, agrupándolos por país y moneda.
    La moneda se determina a través del producto asociado a cada cuenta.
    Los montos se formatean con separadores de miles y 2 decimales.
    
    Args:
        host: Servidor MySQL (opcional)
        port: Puerto MySQL (opcional)
        user: Usuario MySQL (opcional)
        password: Contraseña MySQL (opcional)
        database: Base de datos (opcional)
    
    Returns:
        List[Dict[str, str]]: Lista de diccionarios con las claves:
            - 'País': Nombre del país
            - 'Moneda': Nombre y código de la moneda
            - 'Saldo Total': Suma total formateada
    
    CSV generado: saldo_por_moneda.csv
    
    Ejemplo de retorno:
        [
            {'País': 'Argentina', 'Moneda': 'Peso Argentino (ARS)', 'Saldo Total': '$ 3,600,000.00'},
            {'País': 'Colombia', 'Moneda': 'Peso Colombiano (COP)', 'Saldo Total': '$ 2,700,000.00'}
        ]
    """
    try:
        conn = get_connection(host, port, user, password, database)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                p.nombre AS pais,
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
            GROUP BY p.id_pais, tm.id_moneda
            ORDER BY p.nombre
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for row in rows:
            pais, moneda_nombre, moneda_codigo, simbolo, saldo_total = row
            
            # Formatear moneda y saldo
            moneda_completa = f"{moneda_nombre} ({moneda_codigo})"
            saldo_formateado = f"{simbolo} {saldo_total:,.2f}"
            
            result.append({
                'País': pais,
                'Moneda': moneda_completa,
                'Saldo Total': saldo_formateado
            })
        
        cursor.close()
        conn.close()
        
        # Guardar en CSV
        _write_csv(result, 'saldo_por_moneda.csv',
                  ['País', 'Moneda', 'Saldo Total'])
        
        return result
        
    except Exception as e:
        print(f"❌ Error en saldo_por_moneda: {e}")
        return []


def prestamos_activos(dni: str, host: str = None, port: int = None,
                     user: str = None, password: str = None,
                     database: str = None) -> Optional[List[Dict[str, str]]]:
    """Punto 3 - Consulta los préstamos activos de un cliente específico por DNI.
    
    Busca todos los préstamos en estado 'activo' para el DNI proporcionado.
    Valida la existencia del DNI antes de realizar la consulta.
    Formatea los montos con símbolo de moneda y la tasa con porcentaje.
    
    Args:
        dni: DNI del cliente a consultar
        host: Servidor MySQL (opcional)
        port: Puerto MySQL (opcional)
        user: Usuario MySQL (opcional)
        password: Contraseña MySQL (opcional)
        database: Base de datos (opcional)
    
    Returns:
        Optional[List[Dict[str, str]]]: Lista de diccionarios con las claves:
            - 'ID Préstamo': ID del préstamo
            - 'Monto Total': Monto formateado con símbolo de moneda
            - 'Tasa Interés': Tasa con símbolo % y 2 decimales
            - 'Fecha Inicio': Fecha de inicio del préstamo
            - 'Fecha Fin': Fecha de finalización del préstamo
            - 'Moneda': Código de la moneda
        
        Retorna None si el DNI no existe.
        Retorna lista vacía si el cliente no tiene préstamos activos.
    
    CSV generado: prestamos_activos_[DNI].csv
    
    Ejemplo de retorno:
        [
            {
                'ID Préstamo': '1',
                'Monto Total': '$ 50,000.00',
                'Tasa Interés': '15.50%',
                'Fecha Inicio': '2024-01-15',
                'Fecha Fin': '2026-01-15',
                'Moneda': 'ARS'
            }
        ]
    """
    try:
        conn = get_connection(host, port, user, password, database)
        cursor = conn.cursor()
        
        # Validar existencia del DNI
        cursor.execute(
            "SELECT id_usuario, nombre, apellido FROM usuario WHERE dni = %s",
            (dni,)
        )
        usuario = cursor.fetchone()
        
        if not usuario:
            cursor.close()
            conn.close()
            return None
        
        # Consultar préstamos activos
        query = """
            SELECT 
                p.id_prestamo,
                p.monto_total,
                p.tasa_interes,
                p.fecha_inicio,
                p.fecha_fin,
                tm.codigo AS moneda_codigo,
                tm.simbolo AS moneda_simbolo
            FROM prestamo p
            JOIN usuario u ON p.id_usuario = u.id_usuario
            JOIN tipo_moneda tm ON p.id_moneda = tm.id_moneda
            WHERE u.dni = %s AND p.estado = 'activo'
            ORDER BY p.fecha_inicio DESC
        """
        
        cursor.execute(query, (dni,))
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for row in rows:
            id_prestamo, monto, tasa, fecha_inicio, fecha_fin, moneda_codigo, simbolo = row
            
            result.append({
                'ID Préstamo': str(id_prestamo),
                'Monto Total': f"{simbolo} {monto:,.2f}",
                'Tasa Interés': f"{tasa:.2f}%",
                'Fecha Inicio': str(fecha_inicio),
                'Fecha Fin': str(fecha_fin),
                'Moneda': moneda_codigo
            })
        
        cursor.close()
        conn.close()
        
        # Guardar en CSV con DNI en el nombre
        _write_csv(result, f'prestamos_activos_{dni}.csv',
                  ['ID Préstamo', 'Monto Total', 'Tasa Interés', 
                   'Fecha Inicio', 'Fecha Fin', 'Moneda'])
        
        return result
        
    except Exception as e:
        print(f"❌ Error en prestamos_activos: {e}")
        return []


def top_clientes_transacciones(host: str = None, port: int = None,
                               user: str = None, password: str = None,
                               database: str = None) -> List[Dict[str, str]]:
    """Punto 4 - Obtiene el top 5 de clientes más activos en transacciones.
    
    Calcula el volumen total movido por cada cliente en los últimos 48 meses,
    considerando únicamente transacciones de tipo 'transferencia' y 'retiro'.
    Los resultados se ordenan de mayor a menor por monto total.
    
    Args:
        host: Servidor MySQL (opcional)
        port: Puerto MySQL (opcional)
        user: Usuario MySQL (opcional)
        password: Contraseña MySQL (opcional)
        database: Base de datos (opcional)
    
    Returns:
        List[Dict[str, str]]: Lista de diccionarios con las claves:
            - 'Puesto': Posición en el ranking (1-5)
            - 'Cliente': Nombre completo del cliente
            - 'Total Movido': Monto total formateado
    
    CSV generado: top_clientes.csv
    
    Ejemplo de retorno:
        [
            {'Puesto': '1', 'Cliente': 'Juan Pérez', 'Total Movido': '$ 288,765.09'},
            {'Puesto': '2', 'Cliente': 'María García', 'Total Movido': '$ 275,546.89'}
        ]
    """
    try:
        conn = get_connection(host, port, user, password, database)
        cursor = conn.cursor()
        
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
            GROUP BY u.id_usuario
            ORDER BY total_movido DESC
            LIMIT 5
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        result: List[Dict[str, str]] = []
        for idx, row in enumerate(rows, 1):
            nombre, apellido, total_movido = row
            
            result.append({
                'Puesto': str(idx),
                'Cliente': f"{nombre} {apellido}",
                'Total Movido': f"$ {total_movido:,.2f}"
            })
        
        cursor.close()
        conn.close()
        
        # Guardar en CSV
        _write_csv(result, 'top_clientes.csv',
                  ['Puesto', 'Cliente', 'Total Movido'])
        
        return result
        
    except Exception as e:
        print(f"❌ Error en top_clientes_transacciones: {e}")
        return []


def cuotas_pendientes(host: str = None, port: int = None,
                     user: str = None, password: str = None,
                     database: str = None) -> List[Dict[str, str]]:
    """Punto 5 - Genera reporte de préstamos con cuotas pendientes.
    
    Obtiene todos los préstamos que tienen al menos una cuota en estado 'pendiente'.
    Agrupa por préstamo y cliente, calculando la cantidad de cuotas pendientes
    y el monto total a pagar para cada préstamo.
    
    Args:
        host: Servidor MySQL (opcional)
        port: Puerto MySQL (opcional)
        user: Usuario MySQL (opcional)
        password: Contraseña MySQL (opcional)
        database: Base de datos (opcional)
    
    Returns:
        List[Dict[str, str]]: Lista de diccionarios con las claves:
            - 'Préstamo': ID del préstamo
            - 'DNI Cliente': DNI del cliente
            - 'Cuotas Pendientes': Cantidad de cuotas pendientes
            - 'Monto Total a Pagar': Suma total formateada
    
    CSV generado: cuotas_pendientes.csv
    
    Ejemplo de retorno:
        [
            {'Préstamo': '7', 'DNI Cliente': '20000190', 
             'Cuotas Pendientes': '8', 'Monto Total a Pagar': '$ 32,798.96'},
            {'Préstamo': '11', 'DNI Cliente': '20000278',
             'Cuotas Pendientes': '3', 'Monto Total a Pagar': '$ 17,295.36'}
        ]
    """
    try:
        conn = get_connection(host, port, user, password, database)
        cursor = conn.cursor()
        
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
            
            result.append({
                'Préstamo': str(id_prestamo),
                'DNI Cliente': dni,
                'Cuotas Pendientes': str(cuotas_pendientes),
                'Monto Total a Pagar': f"$ {monto_total:,.2f}"
            })
        
        cursor.close()
        conn.close()
        
        # Guardar en CSV
        _write_csv(result, 'cuotas_pendientes.csv',
                  ['Préstamo', 'DNI Cliente', 'Cuotas Pendientes', 'Monto Total a Pagar'])
        
        return result
        
    except Exception as e:
        print(f"❌ Error en cuotas_pendientes: {e}")
        return []


def crear_vista(host: str = None, port: int = None,
               user: str = None, password: str = None,
               database: str = None) -> bool:
    """Punto 6a - Crea o reemplaza la vista v_resumen_cliente.
    
    Crea una vista persistente en la base de datos que agrupa información
    por cliente mostrando: nombre completo, cantidad de cuentas, cantidad
    de préstamos y saldo total. Los clientes sin cuentas o préstamos
    aparecen con valores 0.
    
    Args:
        host: Servidor MySQL (opcional)
        port: Puerto MySQL (opcional)
        user: Usuario MySQL (opcional)
        password: Contraseña MySQL (opcional)
        database: Base de datos (opcional)
    
    Returns:
        bool: True si la vista se creó exitosamente, False en caso de error
    
    Vista creada: v_resumen_cliente
    
    Ejemplo de uso:
        >>> if crear_vista():
        ...     print("Vista creada exitosamente")
    """
    try:
        conn = get_connection(host, port, user, password, database)
        cursor = conn.cursor()
        
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
        print(f"❌ Error en crear_vista: {e}")
        return False


def ver_resumen(host: str = None, port: int = None,
               user: str = None, password: str = None,
               database: str = None) -> List[Dict[str, str]]:
    """Punto 6b - Consulta la vista v_resumen_cliente.
    
    Lee todos los registros de la vista v_resumen_cliente y los retorna
    como lista de diccionarios. Los clientes sin cuentas o préstamos
    aparecen con valores 0.
    
    Args:
        host: Servidor MySQL (opcional)
        port: Puerto MySQL (opcional)
        user: Usuario MySQL (opcional)
        password: Contraseña MySQL (opcional)
        database: Base de datos (opcional)
    
    Returns:
        List[Dict[str, str]]: Lista de diccionarios con las claves:
            - 'Nombre Completo': Nombre y apellido del cliente
            - 'Cantidad Cuentas': Número de cuentas
            - 'Cantidad Préstamos': Número de préstamos
            - 'Saldo Total': Saldo total formateado
    
    CSV generado: resumen_cliente.csv
    
    Ejemplo de retorno:
        [
            {'Nombre Completo': 'Juan Pérez', 'Cantidad Cuentas': '1',
             'Cantidad Préstamos': '2', 'Saldo Total': '$ 121,704.74'},
            {'Nombre Completo': 'María García', 'Cantidad Cuentas': '1',
             'Cantidad Préstamos': '0', 'Saldo Total': '$ 29,199.04'}
        ]
    """
    try:
        conn = get_connection(host, port, user, password, database)
        cursor = conn.cursor()
        
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
            
            result.append({
                'Nombre Completo': nombre_completo,
                'Cantidad Cuentas': str(cantidad_cuentas),
                'Cantidad Préstamos': str(cantidad_prestamos),
                'Saldo Total': f"$ {saldo_total:,.2f}"
            })
        
        cursor.close()
        conn.close()
        
        # Guardar en CSV
        _write_csv(result, 'resumen_cliente.csv',
                  ['Nombre Completo', 'Cantidad Cuentas', 'Cantidad Préstamos', 'Saldo Total'])
        
        return result
        
    except Exception as e:
        print(f"❌ Error en ver_resumen: {e}")
        return []


def _write_csv(data: List[Dict[str, str]], filename: str, fieldnames: List[str]) -> None:
    """Función auxiliar para escribir datos en formato CSV.
    
    Args:
        data: Lista de diccionarios con los datos
        filename: Nombre del archivo CSV
        fieldnames: Lista de nombres de columnas
    """
    here = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(here, filename)
    
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
