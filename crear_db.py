#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_bancos.py
Genera scripts SQL completos para la BD Bancos:
- catálogos
- 100 usuarios
- 100 cuentas + 100 tarjetas
- 30 préstamos + 360 cuotas
- 4 000 transacciones coherentes
Coherencia: monedas, saldos, fechas, límites.
Salida: archivos .sql en la misma carpeta Y ejecución directa en MySQL.
"""
import random
import datetime as dt
from pathlib import Path
import os
import mysql.connector

# ---------- CONFIG ----------
OUTPUT_DIR = Path(__file__).parent
random.seed(42)          # reproducible
N_USUARIOS = 300
N_PRESTAMOS = 90
N_TRANS    = 8000
# ----------------------------

# ---------- UTILS ----------
def fecha_aleatoria(inicio: dt.date, dias: int) -> dt.date:
    return inicio + dt.timedelta(days=random.randint(0, dias))

def hora_aleatoria(d: dt.date) -> str:
    h, m, s = random.randint(8, 20), random.randint(0, 59), random.randint(0, 59)
    return dt.datetime.combine(d, dt.time(h, m, s)).strftime('%Y-%m-%d %H:%M:%S')

# ---------- CATÁLOGOS ----------
def sql_catalogos():
    pais = """INSERT INTO Pais (nombre,codigo_iso) VALUES
('Argentina','AR'),('Colombia','CO'),('México','MX'),('Perú','PE'),('España','ES');"""
    ciudad = """INSERT INTO Ciudad (nombre,id_pais) VALUES
('Buenos Aires',1),('Córdoba',1),('Rosario',1),('Bogotá',2),('Medellín',2),
('Ciudad de México',3),('Guadalajara',3),('Lima',4),('Arequipa',4),('Madrid',5),('Barcelona',5);"""
    sede = """INSERT INTO Sede (nombre,direccion,id_ciudad) VALUES
('Sede Central BA','Av. Corrientes 123',1),
('Sede Córdoba','Bv. San Juan 456',2),
('Sede Bogotá','Calle 100 7-21',4),
('Sede CDMX','Paseo de la Reforma 222',6),
('Sede Guadalajara','Av. Chapultepec 234',7),
('Sede Lima','Av. Larco 345',8),
('Sede Madrid','Calle de Alcalá 101',10);"""
    moneda = """INSERT INTO Tipo_Moneda (nombre,codigo,simbolo) VALUES
('Peso Argentino','ARS','$'),('Peso Colombiano','COP','$'),
('Peso Mexicano','MXN','$'),('Sol Peruano','PEN','S/'),('Euro','EUR','€');"""
    # Productos por moneda: ARS (id=1), COP (id=2), MXN (id=3), PEN (id=4), EUR (id=5)
    producto = """INSERT INTO Producto (nombre,tipo,descripcion,id_moneda) VALUES
('Cuenta Corriente ARS','cuenta corriente','Cuenta Argentina',1),
('Caja de Ahorro ARS','cuenta ahorro','Ahorro Argentina',1),
('Cuenta Corriente COP','cuenta corriente','Cuenta Colombia',2),
('Caja de Ahorro COP','cuenta ahorro','Ahorro Colombia',2),
('Cuenta Corriente MXN','cuenta corriente','Cuenta México',3),
('Caja de Ahorro MXN','cuenta ahorro','Ahorro México',3),
('Cuenta Corriente PEN','cuenta corriente','Cuenta Perú',4),
('Caja de Ahorro PEN','cuenta ahorro','Ahorro Perú',4),
('Cuenta Corriente EUR','cuenta corriente','Cuenta España',5),
('Caja de Ahorro EUR','cuenta ahorro','Ahorro España',5);"""
    return "\n".join([pais, ciudad, sede, moneda, producto])

# ---------- USUARIOS ----------
def sql_usuarios():
    nombres = ['Luis','Carla','Juan','Ana','Diego','María','Pedro','Lucía','Andrés','Sofía',
            'Martín','Valentina','Matías','Camila','Nicolás','Florencia','Facundo','Agustina',
            'Santiago','Julieta','Tomás','Micaela','Franco','Rocío','Ezequiel','Belén',
            'Ignacio','Daiana','Luciano','Pilar','Alan','Morena','Brian','Melina','Leandro',
            'Celeste','Gonzalo','Jazmín','Maximiliano','Noelia','Sebastián','Aldana',
            'Federico','Ludmila','Ariel','Carolina','Hernán','Estefanía','Ramiro','Olivia']
    apellidos = ['Molina','Gómez','Pérez','Fernández','López','Rodríguez','Hernández','Silva',
            'Cárdenas','Blanco','Sosa','Torres','Ramírez','Herrera','Gutiérrez','Méndez',
            'Ortiz','Rojas','Castro','Vargas','Suárez','Delgado','Ponce','Navarro',
            'Paz','Romero','Arias','Luna','Cabrera','Ríos','Morales','Bravo','Ojeda',
            'Ferreyra','Ponce','Navarro','Medina','Acosta','Figueroa','Herrera','Cordero',
            'Aguirre','Bravo','Pereyra','Ludueña','Quiroga','Benítez','Salazar','Campos','Aguilar']
    emails = []
    lines = []
    for i in range(1, N_USUARIOS+1):
        nom = random.choice(nombres)
        ape = random.choice(apellidos)
        dni = f"{20000000 + i}"
        email = f"{nom.lower()}{ape.lower()}{i}@mail.com"
        emails.append(email)
        tel = f"+57 9 {random.randint(11,15)} {random.randint(4000,9999)}-{random.randint(1000,9999)}"
        fn = fecha_aleatoria(dt.date(1975,1,1), 7300)
        id_ciu = random.randint(1, 11)
        lines.append(f"({i},'{nom}','{ape}','{dni}','{email}','{tel}','{fn}',{id_ciu})")
    return "INSERT INTO Usuario (id_usuario,nombre,apellido,dni,email,telefono,fecha_nacimiento,id_ciudad) VALUES\n" + \
        ",\n".join(lines) + ";"

# ---------- CUENTAS + TARJETAS ----------
def sql_cuentas_tarjetas():
    # Mapeo: ciudad_id -> producto_ids según país/moneda
    # Ciudades 1-3: Argentina (ARS) -> productos 1,2
    # Ciudades 4-5: Colombia (COP) -> productos 3,4
    # Ciudades 6-7: México (MXN) -> productos 5,6
    # Ciudades 8-9: Perú (PEN) -> productos 7,8
    # Ciudades 10-11: España (EUR) -> productos 9,10
    ciudad_a_productos = {
        1: [1, 2], 2: [1, 2], 3: [1, 2],  # Argentina
        4: [3, 4], 5: [3, 4],              # Colombia
        6: [5, 6], 7: [5, 6],              # México
        8: [7, 8], 9: [7, 8],              # Perú
        10: [9, 10], 11: [9, 10]           # España
    }
    
    cuentas, tarjetas = [], []
    for i in range(1, N_USUARIOS+1):
        # Obtener ciudad del usuario (debe coincidir con el generado en sql_usuarios)
        # Usamos la misma lógica: id_ciu = random.randint(1, 11) pero con la misma semilla
        random.seed(42)  # Reset para coincidir con sql_usuarios
        for j in range(1, i+1):
            if j == i:
                # Esta es la iteración del usuario actual
                nom = random.choice(['Luis','Carla','Juan','Ana','Diego','María','Pedro','Lucía','Andrés','Sofía',
                    'Martín','Valentina','Matías','Camila','Nicolás','Florencia','Facundo','Agustina',
                    'Santiago','Julieta','Tomás','Micaela','Franco','Rocío','Ezequiel','Belén',
                    'Ignacio','Daiana','Luciano','Pilar','Alan','Morena','Brian','Melina','Leandro',
                    'Celeste','Gonzalo','Jazmín','Maximiliano','Noelia','Sebastián','Aldana',
                    'Federico','Ludmila','Ariel','Carolina','Hernán','Estefanía','Ramiro','Olivia'])
                ape = random.choice(['Molina','Gómez','Pérez','Fernández','López','Rodríguez','Hernández','Silva',
                    'Cárdenas','Blanco','Sosa','Torres','Ramírez','Herrera','Gutiérrez','Méndez',
                    'Ortiz','Rojas','Castro','Vargas','Suárez','Delgado','Ponce','Navarro',
                    'Paz','Romero','Arias','Luna','Cabrera','Ríos','Morales','Bravo','Ojeda',
                    'Ferreyra','Ponce','Navarro','Medina','Acosta','Figueroa','Herrera','Cordero',
                    'Aguirre','Bravo','Pereyra','Ludueña','Quiroga','Benítez','Salazar','Campos','Aguilar'])
                tel = f"+57 9 {random.randint(11,15)} {random.randint(4000,9999)}-{random.randint(1000,9999)}"
                fn = fecha_aleatoria(dt.date(1975,1,1), 7300)
                id_ciu = random.randint(1, 11)
            else:
                # Avanzar el generador random para las iteraciones previas
                nom = random.choice(['Luis','Carla','Juan','Ana','Diego','María','Pedro','Lucía','Andrés','Sofía',
                    'Martín','Valentina','Matías','Camila','Nicolás','Florencia','Facundo','Agustina',
                    'Santiago','Julieta','Tomás','Micaela','Franco','Rocío','Ezequiel','Belén',
                    'Ignacio','Daiana','Luciano','Pilar','Alan','Morena','Brian','Melina','Leandro',
                    'Celeste','Gonzalo','Jazmín','Maximiliano','Noelia','Sebastián','Aldana',
                    'Federico','Ludmila','Ariel','Carolina','Hernán','Estefanía','Ramiro','Olivia'])
                ape = random.choice(['Molina','Gómez','Pérez','Fernández','López','Rodríguez','Hernández','Silva',
                    'Cárdenas','Blanco','Sosa','Torres','Ramírez','Herrera','Gutiérrez','Méndez',
                    'Ortiz','Rojas','Castro','Vargas','Suárez','Delgado','Ponce','Navarro',
                    'Paz','Romero','Arias','Luna','Cabrera','Ríos','Morales','Bravo','Ojeda',
                    'Ferreyra','Ponce','Navarro','Medina','Acosta','Figueroa','Herrera','Cordero',
                    'Aguirre','Bravo','Pereyra','Ludueña','Quiroga','Benítez','Salazar','Campos','Aguilar'])
                tel = f"+57 9 {random.randint(11,15)} {random.randint(4000,9999)}-{random.randint(1000,9999)}"
                fn = fecha_aleatoria(dt.date(1975,1,1), 7300)
                id_ciu = random.randint(1, 11)
        
        # Ahora tenemos id_ciu correcto para el usuario i
        productos_disponibles = ciudad_a_productos[id_ciu]
        
        # cuenta
        num_cuenta = f"CBU{str(i).zfill(10)}"
        saldo = round(random.uniform(1500, 95000), 2)
        f_ap = fecha_aleatoria(dt.date(2018,1,1), 1800)
        id_prod = random.choice(productos_disponibles)  # Producto según país
        id_sede = random.randint(1, 7)
        cuentas.append(f"(DEFAULT,'{num_cuenta}',{saldo},'{f_ap}',{i},{id_prod},{id_sede})")
        # tarjeta
        num_tar = f"4{str(random.randint(10**14, 10**15-1)).zfill(15)}"
        tipo = random.choice(['débito','crédito'])
        limite = 'NULL' if tipo == 'débito' else round(random.uniform(50000, 200000), 2)
        f_emi = fecha_aleatoria(dt.date(2020,1,1), 900)
        f_ven = f_emi + dt.timedelta(days=365*4)
        tarjetas.append(f"(DEFAULT,'{num_tar}','{tipo}',{limite},'{f_emi}','{f_ven}',{i},(SELECT id_cuenta FROM Cuenta WHERE id_usuario={i} LIMIT 1))")
    
    random.seed(42)  # Reset seed para mantener coherencia en funciones posteriores
    sql_cuenta = "INSERT INTO Cuenta (id_cuenta,numero_cuenta,saldo,fecha_apertura,id_usuario,id_producto,id_sede) VALUES\n" + ",\n".join(cuentas) + ";"
    sql_tarjeta = "INSERT INTO Tarjeta (id_tarjeta,numero_tarjeta,tipo,limite_credito,fecha_emision,fecha_vencimiento,id_usuario,id_cuenta) VALUES\n" + ",\n".join(tarjetas) + ";"
    return sql_cuenta + "\n" + sql_tarjeta

# ---------- PRESTAMOS + CUOTAS ----------
def sql_prestamos_cuotas():
    prestamos, cuotas = [], []
    for p in range(1, N_PRESTAMOS+1):
        id_usu = random.randint(1, N_USUARIOS)
        monto = round(random.uniform(50000, 450000), 2)
        tasa  = round(random.uniform(15, 25), 2)
        f_ini = fecha_aleatoria(dt.date(2022,1,1), 600)
        f_fin = f_ini + dt.timedelta(days=365)
        estado = random.choice(['activo','pagado']) if random.random() < 0.8 else 'en mora'
        prestamos.append(f"(DEFAULT,{id_usu},{monto},{tasa},'{f_ini}','{f_fin}','{estado}',1)")
        # 12 cuotas
        c_couta = random.randint(5, 41)
        cuota_monto = round(monto / c_couta, 2)
        for c in range(1, c_couta+1):
            f_venc = f_ini + dt.timedelta(days=30*c)
            f_pago = None
            if estado == 'pagado' or (estado == 'activo' and random.random() < 0.65):
                f_pago = f_venc + dt.timedelta(days=random.randint(-5, 5))
            est_cuota = 'pagada' if f_pago else ('vencida' if f_venc < dt.date.today() else 'pendiente')
            cuotas.append(f"(DEFAULT,{p},{c},{cuota_monto},'{f_venc}',{f_pago and chr(39)+str(f_pago)+chr(39) or 'NULL'},'{est_cuota}')")
    sql_prest = "INSERT INTO Prestamo (id_prestamo,id_usuario,monto_total,tasa_interes,fecha_inicio,fecha_fin,estado,id_moneda) VALUES\n" + ",\n".join(prestamos) + ";"
    sql_cuo   = "INSERT INTO Cuota (id_cuota,id_prestamo,numero_cuota,monto,fecha_vencimiento,fecha_pago,estado) VALUES\n" + ",\n".join(cuotas) + ";"
    return sql_prest + "\n" + sql_cuo

# ---------- TRANSACCIONES ----------
def sql_transacciones():
    # saldos en memoria para no dejar negativos
    saldos = {i: round(random.uniform(1500, 95000), 2) for i in range(1, N_USUARIOS+1)}
    trans = []
    for t in range(1, N_TRANS+1):
        ori = random.randint(1, N_USUARIOS)
        mon = 1  # todos en ARS para simplificar
        tipo = random.choice(['depósito','retiro','transferencia','pago cuota','compra tarjeta'])
        des = 'NULL'
        if tipo == 'transferencia':
            dest = random.choice([i for i in range(1, N_USUARIOS+1) if i != ori])
            des = str(dest)
        monto = round({
            'depósito': random.uniform(10, 20000),
            'retiro': random.uniform(10, 5000),
            'transferencia': random.uniform(100, 50000),
            'pago cuota': random.uniform(100, 5000),
            'compra tarjeta': random.uniform(10, 3000)
        }[tipo], 2)
        # saldo suficiente
        if tipo in ('retiro','pago cuota','compra tarjeta'):
            if saldos[ori] < monto:
                continue  # saltar para evitar negativos
            saldos[ori] -= monto
        else:
            saldos[ori] += monto
        if tipo == 'transferencia':
            saldos[int(des)] += monto
        fecha = hora_aleatoria(fecha_aleatoria(dt.date(2021,1,1), 900))
        desc = f"{tipo} automática"
        trans.append(f"(DEFAULT,{ori},{des and des or 'NULL'},{monto},'{fecha}','{tipo}','{desc}')")
        if len(trans) == N_TRANS:
            break
    return "INSERT INTO Transaccion (id_transaccion,id_cuenta_origen,id_cuenta_destino,monto,fecha,tipo,descripcion) VALUES\n" + ",\n".join(trans) + ";"

# ---------- MAIN ----------
def ejecutar_sql_en_db(sql_statements: list, host: str = "127.0.0.1", port: int = 3306,
                       user: str = "root", password: str = None, database: str = "bancos"):
    """Ejecuta una lista de statements SQL en la base de datos MySQL."""
    password = password or os.getenv('MYSQL_PASSWORD', 'E57Nfcl5~3*')
    
    try:
        print(f"🔌 Conectando a MySQL en {host}:{port} - base de datos '{database}'...")
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        
        # Limpiar tablas en orden inverso (para respetar FKs)
        print("🗑️  Limpiando tablas existentes...")
        tables_to_truncate = ['transaccion', 'cuota', 'prestamo', 'tarjeta', 'cuenta', 
                             'usuario', 'producto', 'sede', 'ciudad', 'tipo_moneda', 'pais']
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for table in tables_to_truncate:
            try:
                cursor.execute(f"TRUNCATE TABLE {table};")
                print(f"   ✓ {table}")
            except mysql.connector.Error as e:
                print(f"   ⚠️  No se pudo limpiar {table}: {e}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        
        # Ejecutar los statements SQL
        print("\n📝 Insertando datos...")
        for i, sql in enumerate(sql_statements, 1):
            try:
                # Dividir en statements individuales si hay múltiples
                for statement in sql.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                conn.commit()
                print(f"   ✓ Bloque {i} ejecutado")
            except mysql.connector.Error as e:
                print(f"   ❌ Error en bloque {i}: {e}")
                conn.rollback()
                raise
        
        cursor.close()
        conn.close()
        print("\n✅ Todos los datos fueron insertados correctamente en la base de datos!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error de conexión/ejecución: {e}")
        return False

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Generar el SQL
    print("🔧 Generando SQL...")
    files = {
        "01_catalogos.sql": sql_catalogos(),
        "02_usuarios.sql":  sql_usuarios(),
        "03_cuentas_tarjetas.sql": sql_cuentas_tarjetas(),
        "04_prestamos_cuotas.sql": sql_prestamos_cuotas(),
        "05_transacciones.sql":    sql_transacciones()
    }
    
    # Guardar archivos SQL (opcional, por si los necesitas)
    print("\n💾 Guardando archivos SQL...")
    for name, content in files.items():
        (OUTPUT_DIR / name).write_text(content, encoding='utf8')
        print(f"   ✓ {name}")
    
    # Ejecutar en la base de datos
    print("\n" + "="*60)
    sql_statements = list(files.values())
    success = ejecutar_sql_en_db(sql_statements)
    
    if success:
        print("\n🎉 Proceso completado exitosamente!")
        print(f"   - {N_USUARIOS} usuarios")
        print(f"   - {N_USUARIOS} cuentas y {N_USUARIOS} tarjetas")
        print(f"   - {N_PRESTAMOS} préstamos con sus cuotas")
        print(f"   - {N_TRANS} transacciones")
    else:
        print("\n⚠️  Hubo errores durante la ejecución. Los archivos SQL fueron generados.")

if __name__ == "__main__":
    main()