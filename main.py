#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py

Script principal con menú textual para ejecutar las consultas del taller.
Permite al usuario seleccionar qué reporte desea generar.
"""
import os
import sys
from consultas import (
    clientes_por_ubicacion,
    saldo_por_moneda,
    prestamos_activos,
    top_clientes_transacciones,
    cuotas_pendientes,
    crear_vista,
    ver_resumen
)


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("="*70)
    print("  SISTEMA DE REPORTES BANCARIOS")
    print("="*70)
    print("\n📊 MENÚ PRINCIPAL\n")
    print("  1. Clientes por Ubicación Geográfica")
    print("  2. Saldo Total por Moneda y País")
    print("  3. Préstamos Activos de un Cliente (por DNI)")
    print("  4. Top 5 Clientes Más Activos en Transacciones")
    print("  5. Cuotas Pendientes por Préstamo")
    print("  6. Vista Resumen de Cliente")
    print("  0. Salir")
    print("\n" + "="*70)


def ejecutar_punto1():
    """Ejecuta el Punto 1: Clientes por Ubicación."""
    limpiar_pantalla()
    print("="*70)
    print("  PUNTO 1 - CLIENTES POR UBICACIÓN GEOGRÁFICA")
    print("="*70)
    print("\n🔎 Generando reporte de clientes por ubicación...")
    
    data = clientes_por_ubicacion()
    
    if data:
        print(f"\n✅ Archivo generado: clientes_ubicacion.csv")
        print(f"   Total de clientes: {len(data)}")
        print(f"\n📊 PRIMEROS 10 REGISTROS:")
        print("-"*70)
        print(f"{'Cliente':<30} {'Ciudad':<20} {'País':<15}")
        print("-"*70)
        for item in data[:10]:
            print(f"{item['Cliente']:<30} {item['Ciudad']:<20} {item['País']:<15}")
        if len(data) > 10:
            print(f"{'...':<30} {'...':<20} {'...':<15}")
            print(f"\n   (Mostrando 10 de {len(data)} clientes)")
    else:
        print("\n⚠️  No se pudieron obtener los datos.")
    
    pausar()


def ejecutar_punto2():
    """Ejecuta el Punto 2: Saldo por Moneda."""
    limpiar_pantalla()
    print("="*70)
    print("  PUNTO 2 - SALDO TOTAL POR MONEDA Y PAÍS")
    print("="*70)
    print("\n🔎 Calculando saldos agrupados por moneda...")
    
    data = saldo_por_moneda()
    
    if data:
        print(f"\n✅ Archivo generado: saldo_por_moneda.csv")
        print(f"   Total de grupos: {len(data)}")
        print(f"\n📊 SALDOS POR PAÍS Y MONEDA:")
        print("-"*70)
        print(f"{'País':<20} {'Moneda':<30} {'Saldo Total':>18}")
        print("-"*70)
        for item in data:
            print(f"{item['País']:<20} {item['Moneda']:<30} {item['Saldo Total']:>18}")
    else:
        print("\n⚠️  No se pudieron obtener los datos.")
    
    pausar()


def ejecutar_punto3():
    """Ejecuta el Punto 3: Préstamos Activos por DNI."""
    limpiar_pantalla()
    print("="*70)
    print("  PUNTO 3 - PRÉSTAMOS ACTIVOS DE UN CLIENTE")
    print("="*70)
    
    dni = input("\n📋 Ingrese el DNI del cliente: ").strip()
    
    if not dni:
        print("\n⚠️  DNI no válido.")
        pausar()
        return
    
    print(f"\n🔎 Buscando préstamos activos para DNI {dni}...")
    
    data = prestamos_activos(dni)
    
    if data is None:
        print(f"\n❌ Error: No se encontró ningún cliente con DNI {dni}")
    elif len(data) == 0:
        print(f"\n⚠️  El cliente con DNI {dni} no tiene préstamos activos.")
    else:
        print(f"\n✅ Archivo generado: prestamos_activos_{dni}.csv")
        print(f"   Total de préstamos activos: {len(data)}")
        print(f"\n📊 PRÉSTAMOS ACTIVOS:")
        print("-"*70)
        print(f"{'ID':<8} {'Monto':<18} {'Tasa':<12} {'Fecha Inicio':<15} {'Moneda':<8}")
        print("-"*70)
        for item in data:
            print(f"{item['ID Préstamo']:<8} {item['Monto Total']:<18} "
                  f"{item['Tasa Interés']:<12} {item['Fecha Inicio']:<15} {item['Moneda']:<8}")
    
    pausar()


def ejecutar_punto4():
    """Ejecuta el Punto 4: Top 5 Clientes Más Activos."""
    limpiar_pantalla()
    print("="*70)
    print("  PUNTO 4 - TOP 5 CLIENTES MÁS ACTIVOS EN TRANSACCIONES")
    print("="*70)
    print("\n🔎 Calculando top 5 clientes (últimos 48 meses)...")
    
    data = top_clientes_transacciones()
    
    if data:
        print(f"\n✅ Archivo generado: top_clientes.csv")
        print(f"\n📊 TOP 5 CLIENTES:")
        print("-"*70)
        print(f"{'Puesto':<10} {'Cliente':<35} {'Total Movido':>20}")
        print("-"*70)
        for item in data:
            print(f"{item['Puesto']:<10} {item['Cliente']:<35} {item['Total Movido']:>20}")
    else:
        print("\n⚠️  No se pudieron obtener los datos.")
    
    pausar()


def ejecutar_punto5():
    """Ejecuta el Punto 5: Cuotas Pendientes."""
    limpiar_pantalla()
    print("="*70)
    print("  PUNTO 5 - CUOTAS PENDIENTES POR PRÉSTAMO")
    print("="*70)
    print("\n🔎 Generando reporte de cuotas pendientes...")
    
    data = cuotas_pendientes()
    
    if data:
        print(f"\n✅ Archivo generado: cuotas_pendientes.csv")
        print(f"   Total de préstamos con cuotas pendientes: {len(data)}")
        print(f"\n📊 PRIMEROS 10 PRÉSTAMOS:")
        print("-"*70)
        print(f"{'Préstamo':<12} {'DNI Cliente':<15} {'Cuotas':<10} {'Monto Total':>20}")
        print("-"*70)
        for item in data[:10]:
            print(f"{item['Préstamo']:<12} {item['DNI Cliente']:<15} "
                  f"{item['Cuotas Pendientes']:<10} {item['Monto Total a Pagar']:>20}")
        if len(data) > 10:
            print(f"{'...':<12} {'...':<15} {'...':<10} {'...':>20}")
            print(f"\n   (Mostrando 10 de {len(data)} préstamos)")
        
        # Estadísticas
        total_cuotas = sum(int(item['Cuotas Pendientes']) for item in data)
        print(f"\n📈 Total de cuotas pendientes: {total_cuotas}")
    else:
        print("\n⚠️  No se encontraron préstamos con cuotas pendientes.")
    
    pausar()


def ejecutar_punto6():
    """Ejecuta el Punto 6: Vista Resumen de Cliente."""
    limpiar_pantalla()
    print("="*70)
    print("  PUNTO 6 - VISTA RESUMEN DE CLIENTE")
    print("="*70)
    
    print("\n🔧 Creando vista v_resumen_cliente...")
    if not crear_vista():
        print("\n❌ Error: No se pudo crear la vista.")
        pausar()
        return
    
    print("✅ Vista creada exitosamente.")
    
    print("\n🔎 Consultando vista y generando reporte...")
    data = ver_resumen()
    
    if data:
        print(f"\n✅ Archivo generado: resumen_cliente.csv")
        print(f"   Total de clientes: {len(data)}")
        print(f"\n📊 PRIMEROS 10 CLIENTES:")
        print("-"*70)
        print(f"{'Nombre Completo':<30} {'Cuentas':<10} {'Préstamos':<12} {'Saldo Total':>15}")
        print("-"*70)
        for item in data[:10]:
            print(f"{item['Nombre Completo']:<30} {item['Cantidad Cuentas']:<10} "
                  f"{item['Cantidad Préstamos']:<12} {item['Saldo Total']:>15}")
        if len(data) > 10:
            print(f"{'...':<30} {'...':<10} {'...':<12} {'...':>15}")
            print(f"\n   (Mostrando 10 de {len(data)} clientes)")
        
        # Estadísticas
        total_cuentas = sum(int(item['Cantidad Cuentas']) for item in data)
        total_prestamos = sum(int(item['Cantidad Préstamos']) for item in data)
        clientes_sin_prestamos = sum(1 for item in data if item['Cantidad Préstamos'] == '0')
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   • Total de cuentas: {total_cuentas}")
        print(f"   • Total de préstamos: {total_prestamos}")
        print(f"   • Clientes sin préstamos: {clientes_sin_prestamos}")
    else:
        print("\n⚠️  No se pudieron obtener los datos.")
    
    pausar()


def main():
    """Función principal que ejecuta el menú interactivo."""
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("\n➤ Seleccione una opción: ").strip()
        
        if opcion == '1':
            ejecutar_punto1()
        elif opcion == '2':
            ejecutar_punto2()
        elif opcion == '3':
            ejecutar_punto3()
        elif opcion == '4':
            ejecutar_punto4()
        elif opcion == '5':
            ejecutar_punto5()
        elif opcion == '6':
            ejecutar_punto6()
        elif opcion == '0':
            limpiar_pantalla()
            print("\n¡Hasta luego! 👋\n")
            sys.exit(0)
        else:
            print("\n⚠️  Opción no válida. Por favor, seleccione una opción del menú.")
            pausar()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        limpiar_pantalla()
        print("\n\n⚠️  Programa interrumpido por el usuario.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}\n")
        sys.exit(1)
