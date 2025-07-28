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
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.db import SessionLocal
from app.services.ejemplos import (
    ejemplo_uso_servicios_individuales,
    ejemplo_uso_servicio_coordinador,
    ejemplo_operaciones_avanzadas
)

# Cargar variables de entorno
load_dotenv()

# Crear engine silencioso para los ejemplos (sin logs SQL)
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
silent_engine = create_engine(DATABASE_URL, echo=False)
SilentSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=silent_engine)

def verificar_tablas():
    """
    Verificar que las tablas existen en la base de datos (creadas por Alembic)
    """
    print("🔍 Verificando que las tablas existen...")
    try:
        with SessionLocal() as session:
            # Verificar algunas tablas clave
            result = session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
            tablas = [row[0] for row in result.fetchall()]
            
            tablas_requeridas = ['familia', 'color', 'proveedor', 'articulo', 'producto', 'stock']
            tablas_faltantes = [tabla for tabla in tablas_requeridas if tabla not in tablas]
            
            if tablas_faltantes:
                print(f"❌ Faltan tablas: {', '.join(tablas_faltantes)}")
                print("💡 Ejecuta: alembic upgrade head")
                return False
            
            print(f"✅ Todas las tablas necesarias existen ({len(tablas)} tablas encontradas)")
            return True
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        print("💡 Asegúrate de que:")
        print("   - PostgreSQL esté corriendo")
        print("   - Las migraciones estén aplicadas: alembic upgrade head")
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
    # Temporalmente suprimir logs de SQLAlchemy para una salida más limpia
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
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
    
    finally:
        # Restaurar nivel de logging
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def main():
    """
    Función principal del ejecutor
    
    Nota: Usa dos tipos de sesiones diferentes:
    - SessionLocal: Para verificaciones (mantiene logs para debugging)
    - SilentSessionLocal: Para ejemplos (sin logs SQL para salida limpia)
    """
    print("🎯 Sistema de Inventario - Ejecutor de Ejemplos")
    print("=" * 60)
    
    # 1. Verificar conexión
    if not verificar_conexion():
        return
    
    # 2. Verificar que las tablas existen (creadas por Alembic)
    if not verificar_tablas():
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
            
            # Ejecutar ejemplo con sesión de BD silenciosa (sin logs SQL)
            with SilentSessionLocal() as session:
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
