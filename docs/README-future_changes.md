# 🗄️ Gestión de Base de Datos - Sistema de Inventario

## 📋 Resumen

Este proyecto usa **Alembic** para gestionar el esquema de la base de datos, NO las funciones `create_all()` de SQLAlchemy. Esto es una práctica más profesional y segura.

## 🔄 Flujo Correcto de Gestión de Tablas

### 1. **Primera Configuración (Solo una vez)**

```bash
# 1. Levantar PostgreSQL
.\scripts\setup-inventario.ps1 -Start

# 2. Aplicar migraciones (crear tablas)
alembic upgrade head

# 3. Verificar estado
alembic current
```

### 2. **Cambios en Modelos (Desarrollo)**

```bash
# 1. Modificar modelos en app/models/
# 2. Generar migración automática
alembic revision --autogenerate -m "Descripción del cambio"

# 3. Revisar la migración generada (IMPORTANTE)
# 4. Aplicar la migración
alembic upgrade head
```

### 3. **Verificar Estado de la Base de Datos**

```bash
# Ver migración actual
alembic current

# Ver historial completo
alembic history --verbose

# Ver diferencias pendientes
alembic check
```

## ✅ **Lo que DEBES hacer:**

1. **Usar Alembic** para crear/modificar tablas
2. **Revisar siempre** las migraciones antes de aplicarlas
3. **Hacer backup** antes de cambios importantes
4. **Probar en desarrollo** antes de producción

## ❌ **Lo que NO debes hacer:**

1. ~~`Base.metadata.create_all()`~~ ← **NUNCA** en producción
2. ~~Modificar tablas manualmente~~ ← Usar migraciones
3. ~~Aplicar migraciones sin revisar~~ ← Revisar siempre
4. ~~Mezclar Alembic con create_all()~~ ← Solo Alembic

## 🎯 **Estado Actual del Proyecto:**

- ✅ **Alembic configurado** (`alembic/` folder)
- ✅ **Migración inicial aplicada** 
- ✅ **Tablas creadas** por migración
- ✅ **Script actualizado** para verificar tablas (no crearlas)

## 🚀 **Para Ejecutar Ejemplos:**

```bash
# Asegurar que PostgreSQL está corriendo
.\scripts\setup-inventario.ps1 -Start

# Verificar que migraciones están aplicadas
alembic current

# Si no hay migración aplicada:
alembic upgrade head

# Ejecutar ejemplos
python scripts\ejecutar_ejemplos.py
```

## 📚 **Comandos Útiles de Alembic:**

```bash
# Ver ayuda
alembic --help

# Estado actual
alembic current

# Historial de migraciones
alembic history

# Aplicar todas las migraciones
alembic upgrade head

# Aplicar migración específica
alembic upgrade <revision_id>

# Deshacer última migración (CUIDADO)
alembic downgrade -1

# Crear migración vacía (manual)
alembic revision -m "Descripción"

# Crear migración automática
alembic revision --autogenerate -m "Descripción"
```

## 🛡️ **Seguridad y Buenas Prácticas:**

### ✅ **Cambios Seguros:**
- Agregar columnas opcionales
- Agregar nuevas tablas
- Agregar índices
- Modificar constraints no destructivos

### ⚠️ **Cambios que Requieren Cuidado:**
- Agregar columnas NOT NULL
- Cambiar tipos de datos
- Renombrar columnas/tablas

### 🔥 **Cambios Peligrosos:**
- Eliminar columnas
- Eliminar tablas
- Cambios que modifiquen datos existentes

## 🎉 **Resumen:**

**El proyecto está configurado correctamente:**
- ✅ Usa Alembic para gestión profesional del esquema
- ✅ Scripts actualizados para verificar (no crear) tablas
- ✅ Flujo de trabajo estándar de la industria
- ✅ Preparado para desarrollo y producción
