#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
database.py

Configuración de conexión a la base de datos MySQL.
Utiliza variables de entorno para las credenciales.
"""
import os
import mysql.connector
from typing import Optional


def get_db_config() -> dict:
    """Obtiene la configuración de la base de datos desde variables de entorno.
    
    Returns:
        dict: Diccionario con los parámetros de conexión (host, port, user, password, database)
    
    Ejemplo:
        >>> config = get_db_config()
        >>> print(config['host'])
        127.0.0.1
    """
    return {
        'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'port': int(os.getenv('MYSQL_PORT', '3306')),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', 'E57Nfcl5~3*'),
        'database': os.getenv('MYSQL_DB', 'bancos')
    }


def get_connection(host: str = None, port: int = None,
                  user: str = None, password: str = None,
                  database: str = None):
    """Crea y retorna una conexión a la base de datos MySQL.
    
    Args:
        host: Servidor MySQL (default: desde get_db_config())
        port: Puerto MySQL (default: desde get_db_config())
        user: Usuario MySQL (default: desde get_db_config())
        password: Contraseña MySQL (default: desde get_db_config())
        database: Base de datos (default: desde get_db_config())
    
    Returns:
        mysql.connector.connection: Objeto de conexión MySQL
    
    Raises:
        mysql.connector.Error: Si hay error en la conexión
    
    Ejemplo:
        >>> try:
        ...     conn = get_connection()
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT 1")
        ...     cursor.close()
        ...     conn.close()
        ... except Exception as e:
        ...     print(f"Error: {e}")
    """
    config = get_db_config()
    
    # Sobrescribir con parámetros explícitos si se proporcionan
    if host is not None:
        config['host'] = host
    if port is not None:
        config['port'] = port
    if user is not None:
        config['user'] = user
    if password is not None:
        config['password'] = password
    if database is not None:
        config['database'] = database
    
    return mysql.connector.connect(**config)
