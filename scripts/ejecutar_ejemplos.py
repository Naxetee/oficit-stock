#!/usr/bin/env python3
"""
🎯 Ejecutor de Ejemplos del Sistema de Inventario

Este script te permite ejecutar los ejemplos de uso de la arquitectura de servicios
de manera sencilla e interactiva.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import SessionLocal, engine, Base
from app.services.ejemplos import (
    ejemplo_uso_servicios_individuales,
    ejemplo_uso_servicio_coordinador,
    ejemplo_operaciones_avanzadas
)

def crear_tablas():
    """
    Crear todas las tablas en la base de datos
    """
    print("🔧 Creando tablas en la base de datos...")
    try:
        # Importar todos los modelos para que se registren
        from app.models import (
            familia, color, proveedor, precio_venta, precio_compra,
            articulo, producto, producto_simple, producto_compuesto,
            componente, componente_producto, pack, pack_producto, stock
        )
        
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def verificar_conexion():
    """
    Verificar que la conexión a la base de datos funciona
    """
    print("🔍 Verificando conexión a la base de datos...")
    try:
        with SessionLocal() as session:
            # Intentar hacer una consulta simple
            result = session.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 Verifica que:")
        print("   - Docker esté corriendo")
        print("   - PostgreSQL esté iniciado")
        print("   - Las variables de entorno estén configuradas (.env)")
        return False

def menu_principal():
    """
    Mostrar menú principal de opciones
    """
    print("\n" + "="*60)
    print("🎯 EJEMPLOS DEL SISTEMA DE INVENTARIO")
    print("="*60)
    print()
    print("Selecciona qué ejemplo quieres ejecutar:")
    print()
    print("1. 🔧 Servicios Individuales")
    print("   Ejemplos básicos usando cada servicio por separado")
    print()
    print("2. 🎯 Servicio Coordinador")
    print("   Operaciones complejas usando InventarioService")
    print()
    print("3. 🔥 Operaciones Avanzadas")
    print("   Análisis, reportes y operaciones especializadas")
    print()
    print("4. 🚀 Ejecutar Todo")
    print("   Ejecutar todos los ejemplos en secuencia")
    print()
    print("0. ❌ Salir")
    print()

def ejecutar_ejemplo(opcion: str, session: Session):
    """
    Ejecutar el ejemplo seleccionado
    """
    try:
        if opcion == "1":
            print("\n🔧 Ejecutando: Servicios Individuales")
            print("-" * 50)
            ejemplo_uso_servicios_individuales(session)
            
        elif opcion == "2":
            print("\n🎯 Ejecutando: Servicio Coordinador")
            print("-" * 50)
            ejemplo_uso_servicio_coordinador(session)
            
        elif opcion == "3":
            print("\n🔥 Ejecutando: Operaciones Avanzadas")
            print("-" * 50)
            ejemplo_operaciones_avanzadas(session)
            
        elif opcion == "4":
            print("\n🚀 Ejecutando: Todos los Ejemplos")
            print("-" * 50)
            ejemplo_uso_servicios_individuales(session)
            print("\n" + "="*50)
            ejemplo_uso_servicio_coordinador(session)
            print("\n" + "="*50)
            ejemplo_operaciones_avanzadas(session)
            
        print("\n✅ Ejemplo completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplo: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Función principal del ejecutor
    """
    print("🎯 Sistema de Inventario - Ejecutor de Ejemplos")
    print("=" * 60)
    
    # 1. Verificar conexión
    if not verificar_conexion():
        return
    
    # 2. Crear tablas si no existen
    if not crear_tablas():
        return
    
    # 3. Menú interactivo
    while True:
        try:
            menu_principal()
            opcion = input("👉 Selecciona una opción (0-4): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Hasta luego!")
                break
                
            if opcion not in ["1", "2", "3", "4"]:
                print("\n❌ Opción inválida. Por favor selecciona 0-4.")
                continue
            
            # Ejecutar ejemplo con sesión de BD
            with SessionLocal() as session:
                ejecutar_ejemplo(opcion, session)
                
            # Preguntar si quiere continuar
            print("\n" + "-" * 50)
            continuar = input("¿Quieres ejecutar otro ejemplo? (s/n): ").strip().lower()
            if continuar not in ["s", "si", "sí", "y", "yes"]:
                print("\n👋 ¡Hasta luego!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Salida por interrupción del usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            break

if __name__ == "__main__":
    main()
