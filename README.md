# Taller 2 - Backend - Sistema Bancario

Sistema de gestión y análisis de datos bancarios con generación de reportes en CSV.

## � Descripción General

Este proyecto implementa un sistema de reportes para una base de datos bancaria que incluye:
- Gestión de clientes por ubicación geográfica
- Análisis de saldos por moneda y país
- Consulta de préstamos activos por cliente
- Rankings de clientes más activos
- Seguimiento de cuotas pendientes
- Vista consolidada de resumen por cliente

## � Tabla de Resumen - Archivos por Punto

| Punto | Función en `consultas.py` | Script Individual | CSV Generado |
|-------|---------------------------|-------------------|--------------|
| **1** | `clientes_por_ubicacion()` | `clientes_ubicacion.py` | `clientes_ubicacion.csv` |
| **2** | `saldo_por_moneda()` | `saldo_por_moneda.py` | `saldo_por_moneda.csv` |
| **3** | `prestamos_activos(dni)` | `punto3prestamos_activos.py` | `prestamos_activos_[DNI].csv` |
| **4** | `top_clientes_transacciones()` | `top_clientes.py` | `top_clientes.csv` |
| **5** | `cuotas_pendientes()` | `cuotas_pendientes.py` | `cuotas_pendientes.csv` |
| **6** | `crear_vista()` + `ver_resumen()` | `resumen_cliente.py` | `resumen_cliente.csv` |

> **Nota:** Todos los puntos están implementados tanto en scripts individuales como en funciones dentro de `consultas.py`, permitiéndote elegir la forma de ejecución que prefieras.

## �📁 Estructura del Proyecto - Entregables Finales

### 🎯 Archivos Principales (Entregables)

```
Taller2_BackEnd/
├── consultas.py               # ⭐ ENTREGABLE 1: Seis funciones principales
├── database.py                # ⭐ ENTREGABLE 2: Configuración de conexión
├── main.py                    # ⭐ ENTREGABLE 3: Menú interactivo
├── README.md                  # ⭐ ENTREGABLE 4: Documentación completa
└── requirements.txt           # Dependencias del proyecto
```

### 📂 Archivos por Punto del Taller

**Punto 1 - Clientes por Ubicación:**
- `clientes_ubicacion.py` (script individual)
- `consultas.py` → función `clientes_por_ubicacion()`
- `clientes_ubicacion.csv` (reporte generado)

**Punto 2 - Saldo por Moneda:**
- `saldo_por_moneda.py` (script individual)
- `consultas.py` → función `saldo_por_moneda()`
- `saldo_por_moneda.csv` (reporte generado)

**Punto 3 - Préstamos Activos:**
- `punto3prestamos_activos.py` (script individual)
- `consultas.py` → función `prestamos_activos(dni)`
- `prestamos_activos_[DNI].csv` (reporte dinámico)

**Punto 4 - Top 5 Clientes:**
- `top_clientes.py` (script individual)
- `consultas.py` → función `top_clientes_transacciones()`
- `top_clientes.csv` (reporte generado)

**Punto 5 - Cuotas Pendientes:**
- `cuotas_pendientes.py` (script individual)
- `consultas.py` → función `cuotas_pendientes()`
- `cuotas_pendientes.csv` (reporte generado)

**Punto 6 - Vista Resumen:**
- `resumen_cliente.py` (script individual)
- `consultas.py` → funciones `crear_vista()` y `ver_resumen()`
- `resumen_cliente.csv` (reporte generado)

### 🛠️ Archivos Auxiliares

```
├── crear_db.py                # Generador de datos de prueba
├── prueba_conexion.py         # Utilidad para verificar conexión
├── 01_catalogos.sql          # SQL generado: catálogos
├── 02_usuarios.sql           # SQL generado: usuarios
├── 03_cuentas_tarjetas.sql   # SQL generado: cuentas y tarjetas
├── 04_prestamos_cuotas.sql   # SQL generado: préstamos y cuotas
└── 05_transacciones.sql      # SQL generado: transacciones
```

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- **Python 3.8+**
- **MySQL Server 8.0+** (o compatible)
- **Git** (para clonar el repositorio)

### 2. Clonar el Repositorio

```powershell
git clone https://github.com/JohanCamiloMesa/Taller2_BackEnd.git
cd Taller2_BackEnd
```

### 3. Crear y Activar el Entorno Virtual

**En Windows (PowerShell):**
```powershell
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**En Linux/Mac:**
```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

### 4. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 5. Configurar la Base de Datos

Crear la base de datos en MySQL:

```sql
CREATE DATABASE IF NOT EXISTS bancos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Configurar Variables de Entorno (Opcional)

Puedes configurar las credenciales de MySQL usando variables de entorno:

```powershell
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "tu_password"
$env:MYSQL_DB = "bancos"
```

Si no configuras estas variables, el sistema usará los valores por defecto definidos en `database.py`.

### 7. Generar Datos de Prueba

```powershell
python crear_db.py
```

Este script:
- ✅ Genera archivos SQL (01-05)
- ✅ Carga automáticamente los datos en MySQL
- ✅ Crea 300 usuarios, 300 cuentas, 90 préstamos, 8000 transacciones

## 🎯 Uso del Sistema

### Ejecutar el Menú Principal

```powershell
python main.py
```

El menú interactivo te permitirá:

El menú interactivo te permitirá:
- Generar cada reporte de forma individual
- Ver un resumen de los resultados en consola
- Acceder a todas las funciones de forma intuitiva

**Salida esperada del menú:**

```
======================================================================
  SISTEMA DE REPORTES BANCARIOS
======================================================================

📊 MENÚ PRINCIPAL

  1. Clientes por Ubicación Geográfica
  2. Saldo Total por Moneda y País
  3. Préstamos Activos de un Cliente (por DNI)
  4. Top 5 Clientes Más Activos en Transacciones
  5. Cuotas Pendientes por Préstamo
  6. Vista Resumen de Cliente
  0. Salir

======================================================================
Seleccione una opción [0-6]: 
```

### Formas de Ejecutar Cada Punto

Tienes **3 opciones** para ejecutar cualquier punto del taller:

#### Opción 1: Menú Principal (RECOMENDADO ⭐)
```powershell
python main.py
# Selecciona la opción 1-6 según el punto que quieras ejecutar
```

#### Opción 2: Scripts Individuales
```powershell
python clientes_ubicacion.py        # Punto 1
python saldo_por_moneda.py          # Punto 2
python punto3prestamos_activos.py   # Punto 3 (solicita DNI por consola)
python top_clientes.py              # Punto 4
python cuotas_pendientes.py         # Punto 5
python resumen_cliente.py           # Punto 6
```

#### Opción 3: Importar desde `consultas.py`
```python
from consultas import (
    clientes_por_ubicacion,        # Punto 1
    saldo_por_moneda,              # Punto 2
    prestamos_activos,             # Punto 3
    top_clientes_transacciones,    # Punto 4
    cuotas_pendientes,             # Punto 5
    crear_vista, ver_resumen       # Punto 6
)

# Ejemplo: Ejecutar Punto 1
datos = clientes_por_ubicacion()
print(f"Total de clientes: {len(datos)}")

# Ejemplo: Ejecutar Punto 3
prestamos = prestamos_activos('20000029')
if prestamos:
    print(f"Préstamos encontrados: {len(prestamos)}")
```

## 📊 Descripción de Cada Punto del Taller

### Punto 1 - Clientes por Ubicación Geográfica

**Función:** `clientes_por_ubicacion()`

**Descripción:** Genera un listado de todos los clientes con su ciudad y país correspondiente.

**Archivo CSV generado:** `clientes_ubicacion.csv`

**Columnas:**
- `Cliente`: Nombre completo del cliente (nombre + apellido)
- `Ciudad`: Ciudad de residencia
- `País`: País de residencia

**Ejemplo de salida por consola:**
```
======================================================================
  PUNTO 1 - CLIENTES POR UBICACIÓN GEOGRÁFICA
======================================================================

🔎 Generando reporte de clientes por ubicación...

✅ Archivo generado: clientes_ubicacion.csv
   Total de clientes: 300

📊 PRIMEROS 10 REGISTROS:
----------------------------------------------------------------------
Cliente                        Ciudad               País           
----------------------------------------------------------------------
Agustina Aguilar               Buenos Aires         Argentina      
Agustina Benítez               Madrid               España         
Agustina Cabrera               Bogotá               Colombia       
...
```

**Ejemplo de contenido CSV:**
```csv
Cliente,Ciudad,País
Juan Pérez,Buenos Aires,Argentina
María García,Bogotá,Colombia
Carlos López,Madrid,España
```

**Características técnicas:**
- ✅ Utiliza JOINs explícitos (usuario → ciudad → país)
- ✅ Elimina duplicados con DISTINCT
- ✅ Ordenamiento alfabético por país, ciudad y cliente
- ✅ Manejo de errores de conexión

---

### Punto 2 - Saldo Total por Moneda y País

**Función:** `saldo_por_moneda()`

**Descripción:** Calcula y agrupa la suma de saldos de todas las cuentas por país y tipo de moneda.

**Archivo CSV generado:** `saldo_por_moneda.csv`

**Columnas:**
- `País`: Nombre del país
- `Moneda`: Nombre y código de la moneda (ej: "Peso Argentino (ARS)")
- `Saldo Total`: Suma total formateada con separadores de miles

**Ejemplo de salida por consola:**
```
======================================================================
  PUNTO 2 - SALDO TOTAL POR MONEDA Y PAÍS
======================================================================

🔎 Calculando saldos agrupados por moneda...

✅ Archivo generado: saldo_por_moneda.csv
   Total de grupos: 5

📊 SALDOS POR PAÍS Y MONEDA:
----------------------------------------------------------------------
País                 Moneda                          Saldo Total
----------------------------------------------------------------------
Argentina            Peso Argentino (ARS)           $ 3,636,098.35
Colombia             Peso Colombiano (COP)          $ 2,744,717.56
España               Euro (EUR)                      € 3,371,476.02
México               Peso Mexicano (MXN)            $ 1,897,803.34
Perú                 Sol Peruano (PEN)               S/ 3,265,172.43
```

**Ejemplo de contenido CSV:**
```csv
País,Moneda,Saldo Total
Argentina,Peso Argentino (ARS),"$ 3,636,098.35"
Colombia,Peso Colombiano (COP),"$ 2,744,717.56"
```

**Características técnicas:**
- ✅ Agrupa por país y moneda
- ✅ Precisión de dos decimales
- ✅ Formato legible con separadores de miles
- ✅ Incluye símbolo de moneda correcto para cada país

---

### Punto 3 - Préstamos Activos de un Cliente

**Función:** `prestamos_activos(dni: str)`

**Descripción:** Consulta y muestra todos los préstamos en estado 'activo' de un cliente específico por su DNI.

**Archivo CSV generado:** `prestamos_activos_[DNI].csv` (nombre dinámico según el DNI consultado)

**Columnas:**
- `ID Préstamo`: Identificador único del préstamo
- `Monto Total`: Monto del préstamo con símbolo de moneda
- `Tasa Interés`: Tasa de interés con símbolo % y 2 decimales
- `Fecha Inicio`: Fecha de inicio del préstamo
- `Fecha Fin`: Fecha de finalización del préstamo
- `Moneda`: Nombre de la moneda

**Ejemplo de salida por consola:**
```
======================================================================
  PUNTO 3 - PRÉSTAMOS ACTIVOS DE UN CLIENTE (POR DNI)
======================================================================

Ingrese el DNI del cliente: 20000029

🔎 Buscando préstamos activos para DNI: 20000029...

✅ Cliente encontrado: Juan Pérez
✅ Archivo generado: prestamos_activos_20000029.csv
   Total de préstamos activos: 2

📊 PRÉSTAMOS ACTIVOS:
----------------------------------------------------------------------
ID      Monto Total      Tasa          Fecha Inicio  Fecha Fin
----------------------------------------------------------------------
15      $ 125,000.00     15.50%        2024-01-15    2026-01-15
28      $ 80,000.00      12.75%        2024-06-10    2027-06-10
```

**Ejemplo de contenido CSV:**
```csv
ID Préstamo,Monto Total,Tasa Interés,Fecha Inicio,Fecha Fin,Moneda
15,"$ 125,000.00",15.50%,2024-01-15,2026-01-15,Peso Argentino
28,"$ 80,000.00",12.75%,2024-06-10,2027-06-10,Peso Argentino
```

**Características técnicas:**
- ✅ Validación de existencia del DNI
- ✅ Mensaje de error si DNI no encontrado
- ✅ Filtrado por estado 'activo'
- ✅ Nombre de archivo dinámico según DNI

---

### Punto 4 - Top 5 Clientes Más Activos en Transacciones

**Función:** `top_clientes_transacciones()`

**Descripción:** Identifica y clasifica los 5 clientes que han movido más dinero en los últimos 48 meses, considerando solo transacciones de tipo 'transferencia' y 'retiro'.

**Archivo CSV generado:** `top_clientes.csv`

**Columnas:**
- `Puesto`: Posición en el ranking (1-5)
- `Cliente`: Nombre completo del cliente
- `Total Movido`: Suma total de dinero movido (formateado)

**Ejemplo de salida por consola:**
```
======================================================================
  PUNTO 4 - TOP 5 CLIENTES MÁS ACTIVOS EN TRANSACCIONES
======================================================================

🔎 Calculando top 5 clientes (últimos 48 meses)...

✅ Archivo generado: top_clientes.csv

📊 TOP 5 CLIENTES MÁS ACTIVOS:
----------------------------------------------------------------------
Puesto | Cliente                        | Total Movido
----------------------------------------------------------------------
1      | Ariel Vargas                   | $ 288,765.09
2      | Carolina Rodríguez             | $ 275,546.89
3      | Nicolás Aguilar                | $ 263,626.48
4      | Luciano Sosa                   | $ 233,686.70
5      | Rocío Benítez                  | $ 229,007.34
```

**Ejemplo de contenido CSV:**
```csv
Puesto,Cliente,Total Movido
1,Ariel Vargas,"$ 288,765.09"
2,Carolina Rodríguez,"$ 275,546.89"
3,Nicolás Aguilar,"$ 263,626.48"
4,Luciano Sosa,"$ 233,686.70"
5,Rocío Benítez,"$ 229,007.34"
```

**Características técnicas:**
- ✅ Periodo dinámico: últimos 48 meses desde NOW()
- ✅ Filtrado por tipo de transacción ('transferencia', 'retiro')
- ✅ Solo monto de cuenta de origen
- ✅ Top 5 ordenados de mayor a menor

---

### Punto 5 - Cuotas Pendientes por Préstamo

**Función:** `cuotas_pendientes()`

**Descripción:** Genera un reporte de todos los préstamos que tienen al menos una cuota en estado 'pendiente', mostrando el total de cuotas pendientes y el monto total a pagar por cada préstamo.

**Archivo CSV generado:** `cuotas_pendientes.csv`

**Columnas:**
- `Préstamo`: ID del préstamo
- `DNI Cliente`: DNI del cliente titular del préstamo
- `Cuotas Pendientes`: Cantidad de cuotas en estado pendiente
- `Monto Total a Pagar`: Suma de montos de cuotas pendientes

**Ejemplo de salida por consola:**
```
======================================================================
  REPORTE DE CUOTAS PENDIENTES POR PRÉSTAMO
======================================================================

🔎 Generando reporte de préstamos con cuotas pendientes...

✅ Archivo generado: cuotas_pendientes.csv
   Total de préstamos con cuotas pendientes: 9

📊 RESUMEN DE CUOTAS PENDIENTES:
----------------------------------------------------------------------
Préstamo   DNI Cliente     Cuotas              Monto Total
----------------------------------------------------------------------
7          20000190        8                   $ 32,798.96
11         20000278        3                   $ 17,295.36
15         20000065        3                   $ 13,310.37
...

📈 ESTADÍSTICAS GENERALES:
   • Total de préstamos con cuotas pendientes: 9
   • Total de cuotas pendientes: 30
   • Monto total a pagar: $ 138,792.73
```

**Ejemplo de contenido CSV:**
```csv
Préstamo,DNI Cliente,Cuotas Pendientes,Monto Total a Pagar
7,20000190,8,"$ 32,798.96"
11,20000278,3,"$ 17,295.36"
15,20000065,3,"$ 13,310.37"
```

**Características técnicas:**
- ✅ Agrupación por préstamo y cliente
- ✅ Filtrado exclusivo por estado 'pendiente'
- ✅ Cálculo de suma total de montos pendientes
- ✅ Conteo de cuotas pendientes

---

### Punto 6 - Vista Resumen de Cliente

**Funciones:** `crear_vista()` y `ver_resumen()`

**Descripción:** Crea una vista persistente en la base de datos que consolida información por cliente (cuentas, préstamos y saldo total), y genera un reporte CSV con esta información.

**Archivo CSV generado:** `resumen_cliente.csv`

**Columnas:**
- `Nombre Completo`: Nombre y apellido del cliente
- `Cantidad Cuentas`: Número de cuentas abiertas
- `Cantidad Préstamos`: Número de préstamos contratados
- `Saldo Total`: Saldo total de todas las cuentas

**Ejemplo de salida por consola:**
```
======================================================================
  VISTA RESUMEN DE CLIENTE
======================================================================

🔧 Creando vista v_resumen_cliente...
✅ Vista creada exitosamente.

🔎 Consultando vista y generando reporte...

✅ Archivo generado: resumen_cliente.csv
   Total de clientes: 300

📊 RESUMEN DE CLIENTES (Primeros 10):
----------------------------------------------------------------------
Nombre Completo                Cuentas    Préstamos    Saldo Total
----------------------------------------------------------------------
Agustina Aguilar               1          1            $ 27,945.44
Agustina Benítez               1          0            $ 29,199.04
Alan Ferreyra                  1          2            $ 121,704.74
...

📈 ESTADÍSTICAS GENERALES:
   • Total de clientes: 300
   • Total de cuentas: 300
   • Total de préstamos: 90
   • Saldo total en el sistema: $ 15,357,129.91
   • Clientes sin cuentas: 0
   • Clientes sin préstamos: 223
```

**Ejemplo de contenido CSV:**
```csv
Nombre Completo,Cantidad Cuentas,Cantidad Préstamos,Saldo Total
Agustina Aguilar,1,1,"$ 27,945.44"
Agustina Benítez,1,0,"$ 29,199.04"
Alan Ferreyra,1,2,"$ 121,704.74"
```

**Características técnicas:**
- ✅ Vista dinámica con CREATE OR REPLACE VIEW
- ✅ LEFT JOINs para incluir todos los clientes
- ✅ COALESCE para valores NULL → 0
- ✅ Clientes sin cuentas/préstamos aparecen con 0

## 🔧 Archivos del Proyecto

### 1. `consultas.py` - Funciones Principales

Contiene las **6 funciones** del taller:

1. `clientes_por_ubicacion()` - Punto 1
2. `saldo_por_moneda()` - Punto 2  
3. `prestamos_activos(dni)` - Punto 3
4. `top_clientes_transacciones()` - Punto 4
5. `cuotas_pendientes()` - Punto 5
6. `crear_vista()` y `ver_resumen()` - Punto 6

Cada función:
- ✅ Es independiente y reutilizable
- ✅ Incluye docstring descriptivo
- ✅ Guarda resultados en CSV
- ✅ Maneja errores de conexión
- ✅ Retorna `List[Dict[str, str]]`

### 2. `database.py` - Configuración de Conexión

Contiene:
- `get_db_config()`: Obtiene configuración desde variables de entorno
- `get_connection()`: Crea conexión a MySQL

**Características:**
- ✅ No incluye credenciales hardcodeadas
- ✅ Usa variables de entorno
- ✅ Valores por defecto configurables
- ✅ Manejo de errores de conexión

### 3. `main.py` - Script Principal con Menú

Características:
- ✅ Menú textual interactivo
- ✅ Navegación intuitiva
- ✅ Muestra resumen de resultados en consola
- ✅ Limpieza de pantalla entre opciones
- ✅ Validación de entradas
- ✅ Opción de salida

## 📝 Características Técnicas Generales

### Claridad del Reporte
- ✅ Columnas con nombres descriptivos
- ✅ Orden lógico de información
- ✅ Sin duplicados (uso de DISTINCT)
- ✅ Formato legible con separadores de miles

### Precisión de Consultas SQL
- ✅ JOINs explícitos (no implícitos)
- ✅ Filtrados específicos según requerimientos
- ✅ Agregaciones correctas (SUM, COUNT)
- ✅ Ordenamiento apropiado

### Modularidad
- ✅ Funciones independientes
- ✅ Fácilmente reutilizables
- ✅ Importables desde otros módulos
- ✅ Separación de responsabilidades

### Manejo de Archivos CSV
- ✅ Encoding UTF-8-sig (compatible con Excel)
- ✅ Nombres de archivo específicos
- ✅ Columnas según especificación
- ✅ Formato consistente

### Documentación
- ✅ Docstrings en todas las funciones
- ✅ Descripción de parámetros y retorno
- ✅ Ejemplos de uso
- ✅ Formato de datos documentado

### Manejo de Errores
- ✅ Try-except para conexiones
- ✅ Mensajes informativos
- ✅ Cierre seguro de recursos
- ✅ Validaciones de entrada

## 📊 Datos Generados

El script `crear_db.py` genera:

| Tabla | Cantidad de Registros |
|-------|----------------------|
| Países | 5 |
| Ciudades | 11 |
| Sedes | 7 |
| Tipo_Moneda | 5 |
| Productos | 10 |
| Usuarios | 300 |
| Cuentas | 300 |
| Tarjetas | 300 |
| Préstamos | 90 |
| Cuotas | ~1080-3690 |
| Transacciones | 8000 |

## 🧪 Pruebas

### Verificar Conexión a MySQL
```powershell
python prueba_conexion.py
```

### Ejecutar Funciones Individualmente

También puedes importar y usar las funciones desde Python:

### Generar y Cargar Datos en la Base de Datos

```powershell
python crear_db.py
```

Este script:
- ✅ Genera archivos SQL (01-05)
- ✅ Carga automáticamente los datos en MySQL
- ✅ Crea 300 usuarios, 300 cuentas, 90 préstamos, 8000 transacciones

### Punto 1 - Reporte de Clientes por Ubicación

```powershell
python clientes_ubicacion.py
```

**Resultado:** Genera `clientes_ubicacion.csv` con:
- Cliente (nombre completo)
- Ciudad
- País
- Ordenado alfabéticamente por País → Ciudad → Cliente

**Importar la función en otro módulo:**
```python
from clientes_ubicacion import clientes_por_ubicacion

clientes = clientes_por_ubicacion()
for cliente in clientes:
    print(f"{cliente['Cliente']} - {cliente['Ciudad']}, {cliente['País']}")
```

### Punto 2 - Reporte de Saldos por Moneda

```powershell
python saldo_por_moneda.py
```

**Resultado:** Genera `saldo_por_moneda.csv` con:
- País
- Moneda (nombre y código)
- Saldo Total (formateado con separadores de miles y 2 decimales)

**Importar la función en otro módulo:**
```python
from saldo_por_moneda import saldo_por_moneda

saldos = saldo_por_moneda()
for item in saldos:
    print(f"{item['País']} - {item['Moneda']}: {item['Saldo Total']}")
```

### Punto 3 - Préstamos Activos por DNI

```powershell
python punto3prestamos_activos.py
```

El script solicitará el DNI del cliente por consola.

**Resultado:** Genera `prestamos_activos_[DNI].csv` con:
- ID Préstamo
- Monto Total (con símbolo de moneda)
- Tasa Interés (con símbolo % y 2 decimales)
- Fecha Inicio
- Fecha Fin
- Moneda

**Importar la función en otro módulo:**
```python
from punto3prestamos_activos import prestamos_activos

# Consultar préstamos activos de un cliente
prestamos = prestamos_activos('20000029')

if prestamos is None:
    print("Error: Cliente no encontrado")
elif len(prestamos) == 0:
    print("Cliente sin préstamos activos")
else:
    for p in prestamos:
        print(f"Préstamo {p['ID Préstamo']}: {p['Monto Total']} - Tasa: {p['Tasa Interés']}")
```

### Punto 4 - Top 5 Clientes Más Activos

```powershell
python top_clientes.py
```

**Resultado:** Genera `top_clientes.csv` con:
- Puesto (1-5)
- Cliente (nombre completo)
- Total Movido (formateado con separadores de miles y 2 decimales)

**Importar la función en otro módulo:**
```python
from top_clientes import top_clientes_transacciones

# Obtener top 5 clientes
clientes = top_clientes_transacciones()
for cliente in clientes:
    print(f"{cliente['Puesto']}. {cliente['Cliente']}: {cliente['Total Movido']}")
```

### Punto 5 - Cuotas Pendientes por Préstamo

```powershell
python cuotas_pendientes.py
```

**Resultado:** Genera `cuotas_pendientes.csv` con:
- Préstamo (ID del préstamo)
- DNI Cliente
- Cuotas Pendientes (cantidad)
- Monto Total a Pagar (formateado con separadores de miles y 2 decimales)

**Importar la función en otro módulo:**
```python
from cuotas_pendientes import cuotas_pendientes

# Obtener préstamos con cuotas pendientes
reporte = cuotas_pendientes()
for item in reporte:
    print(f"Préstamo {item['Préstamo']} - DNI {item['DNI Cliente']}: "
          f"{item['Cuotas Pendientes']} cuotas - {item['Monto Total a Pagar']}")
```

### Punto 6 - Vista Resumen de Cliente

```powershell
python resumen_cliente.py
```

**Resultado:** 
1. Crea o reemplaza la vista persistente `v_resumen_cliente` en la base de datos
2. Genera `resumen_cliente.csv` con:
   - Nombre Completo
   - Cantidad Cuentas
   - Cantidad Préstamos
   - Saldo Total (formateado con separadores de miles y 2 decimales)

**Importar las funciones en otro módulo:**
```python
from resumen_cliente import crear_vista, ver_resumen

# Crear o actualizar la vista
if crear_vista():
    print("Vista creada exitosamente")

# Obtener resumen de todos los clientes
resumen = ver_resumen()
for cliente in resumen:
    print(f"{cliente['Nombre Completo']}: {cliente['Cantidad Cuentas']} cuentas, "
          f"{cliente['Cantidad Préstamos']} préstamos - {cliente['Saldo Total']}")
```

## 🔧 Configuración Avanzada

### Variables de Entorno

Puedes configurar la conexión a MySQL usando variables de entorno:

```powershell
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "tu_password"
$env:MYSQL_DB = "bancos"
```

### Opciones de Línea de Comandos

**clientes_ubicacion.py:**
```powershell
python clientes_ubicacion.py --host 127.0.0.1 --port 3306 --user root --password "pass" --database bancos --verbose
```

## 📝 Características Técnicas

### Punto 1 - Clientes por Ubicación

**Requisitos Funcionales:**
- ✅ Nombre completo en un solo campo
- ✅ JOINs explícitos en la consulta
- ✅ Sin duplicados (DISTINCT)
- ✅ Ordenamiento alfabético por país, ciudad y cliente

**Requisitos No Funcionales:**
- ✅ Función `clientes_por_ubicacion()` retorna List[Dict]
- ✅ Script independiente y ejecutable
- ✅ Fácilmente importable por otros módulos

### Punto 2 - Saldo por Moneda

**Requisitos Funcionales:**
- ✅ Suma de saldos de todas las cuentas
- ✅ Agrupado por país y moneda (vía producto)
- ✅ Precisión de dos decimales

**Requisitos No Funcionales:**
- ✅ Montos formateados para legibilidad (separadores de miles)
- ✅ Función `saldo_por_moneda()` retorna List[Dict]
- ✅ Diseñada para importación por otros módulos

### Punto 3 - Préstamos Activos por DNI

**Requisitos Funcionales:**
- ✅ Validación de existencia del DNI
- ✅ Mensaje de error si DNI no encontrado
- ✅ Monto con símbolo de moneda
- ✅ Tasa de interés con 2 decimales y símbolo %
- ✅ Filtrado por estado 'activo'

**Requisitos No Funcionales:**
- ✅ Lógica en función `prestamos_activos(dni: str)`
- ✅ Consulta optimizada con índices
### Ejecutar Funciones Individualmente

También puedes importar y usar las funciones desde Python:

```python
from consultas import (
    clientes_por_ubicacion,
    saldo_por_moneda,
    prestamos_activos,
    top_clientes_transacciones,
    cuotas_pendientes,
    crear_vista,
    ver_resumen
)

# Ejemplo: Obtener clientes por ubicación
clientes = clientes_por_ubicacion()
for cliente in clientes[:5]:
    print(f"{cliente['Cliente']} - {cliente['Ciudad']}, {cliente['País']}")

# Ejemplo: Consultar préstamos activos
prestamos = prestamos_activos('20000029')
if prestamos:
    print(f"Préstamos activos: {len(prestamos)}")

# Ejemplo: Crear vista y ver resumen
if crear_vista():
    resumen = ver_resumen()
    print(f"Total clientes: {len(resumen)}")
```

## ⚠️ Solución de Problemas

### Error de Autenticación MySQL

Si obtienes el error: `Authentication plugin 'caching_sha2_password' is not supported`

**Solución:**
```powershell
# Usar el Python del entorno virtual
.\venv\Scripts\python.exe main.py
```

### Error de Permisos en PowerShell

Si no puedes activar el entorno virtual:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error de Conexión a MySQL

Verifica que:
1. MySQL Server esté corriendo
2. Las credenciales sean correctas
3. La base de datos `bancos` exista
4. El puerto 3306 esté disponible

## 📚 Dependencias

El archivo `requirements.txt` incluye:

```
mysql-connector-python==8.0.33
```

## 🎓 Notas Académicas

Este proyecto fue desarrollado como parte del **Taller 2 - Backend** y cumple con todos los requisitos especificados:

### Entregables Finales ✅

1. **consultas.py** - Seis funciones con docstrings completos
2. **database.py** - Configuración de conexión sin credenciales hardcodeadas
3. **main.py** - Menú textual interactivo para invocar las funciones
4. **README.md** - Documentación completa con ejemplos y instrucciones

### Recomendaciones Implementadas ✅

- ✅ **Claridad del reporte:** Columnas legibles, orden lógico, sin duplicados
- ✅ **Precisión de consultas:** SQL responde exactamente a los requerimientos
- ✅ **Modularidad:** Funciones independientes y reutilizables
- ✅ **Manejo de archivos:** Cada función guarda CSV con nombre y columnas especificadas
- ✅ **Documentación:** Docstrings con propósito y formato de retorno
- ✅ **Manejo de errores:** Captura de excepciones de conexión a BD

## 📄 Licencia

MIT License - Ver archivo `LICENSE` para más detalles.

## 👤 Autor

**Johan Camilo Mesa Rios**

---

*Última actualización: Noviembre 2025*
