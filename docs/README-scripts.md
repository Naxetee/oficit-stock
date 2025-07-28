# 🚀 Scripts de PowerShell - Sistema de Inventario

Esta carpeta contiene varios scripts de PowerShell para gestionar fácilmente el entorno Docker del sistema de inventario.

## 📁 Scripts Disponibles

### 1. `setup-inventario.ps1` - Script Principal Completo

**Script principal con todas las funcionalidades:**

```powershell
# Configuración inicial completa (primera vez)
.\setup-inventario.ps1 -Setup

# Solo iniciar servicios
.\setup-inventario.ps1 -Start

# Detener servicios
.\setup-inventario.ps1 -Stop

# Reiniciar servicios
.\setup-inventario.ps1 -Restart

# Ver estado de servicios
.\setup-inventario.ps1 -Status

# Conectar a base de datos
.\setup-inventario.ps1 -Connect

# Limpiar contenedores y datos
.\setup-inventario.ps1 -Clean

# Ayuda
.\setup-inventario.ps1 -Help
```

## 🎯 Uso Recomendado

### Primera Vez (Configuración Inicial):

```powershell
# 1. Configuración completa
.\setup-inventario.ps1 -Setup

# 2. Verificar que todo está corriendo
.\setup-inventario.ps1 -Status

# 3. Probar conexión
.\setup-inventario.ps1 -Connect
```

### Solución de Problemas:

```powershell
# Ver estado actual
.\setup-inventario.ps1 -Status

# Reiniciar si hay problemas
.\setup-inventario.ps1 -Restart

# Limpiar todo y empezar de nuevo
.\setup-inventario.ps1 -Clean
.\setup-inventario.ps1 -Setup
```

## 🔧 Requisitos Previos

1. **Docker Desktop** instalado y corriendo
2. **PowerShell** (incluido en Windows)
3. **Archivos del proyecto:**
   - `docker-compose.yml`
   - `.env`

## 🐘 Información de la Base de Datos

Los scripts se conectan a PostgreSQL con esta configuración:

- **Host:** localhost
- **Puerto:** 5432
- **Base de datos:** oficit_stock
- **Usuario:** oficit
- **Contraseña:** \*\*\*\* (se oculta por seguridad)

## 🎨 Características de los Scripts

### ✨ Funcionalidades Incluidas:

- 🎯 **Detección automática** de Docker
- 🔍 **Verificación de archivos** necesarios
- 📊 **Estado en tiempo real** de servicios
- 🔗 **Información de conexión** completa
- 🧹 **Limpieza segura** con confirmación
- 🎨 **Salida coloreada** para mejor UX

### 🛡️ Seguridad:

- ✅ Verificaciones antes de ejecutar
- ⚠️ Confirmación para operaciones destructivas
- 📋 Información clara sobre lo que hace cada comando
- 🔍 Detección de errores con mensajes útiles

## 📖 Ejemplos de Salida

### Iniciando servicios:
```
🎯 SISTEMA DE INVENTARIO
PostgreSQL + Docker
oficit-stock

🔍 Verificando Docker...
✅ Docker encontrado: Docker version 20.10.x
✅ Docker Desktop está corriendo

🚀 Iniciando servicios Docker...
✅ Servicios iniciados exitosamente

📊 Estado de servicios:
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                    NAMES
a1b2c3d4e5f6   postgres:16   "docker-entrypoint.s…"   2 minutes ago    Up 2 minutes    0.0.0.0:5432->5432/tcp   prinventario_db_1

🐘 Información de PostgreSQL:
   • Base de datos: oficit_stock
   • Usuario: oficit
   • Puerto: 5432
   • Host: localhost
```

## 🚨 Troubleshooting

### Si Docker no inicia:
1. Verificar que Docker Desktop esté corriendo
2. Reiniciar Docker Desktop
3. Verificar espacio en disco

### Si la base de datos no conecta:
1. Verificar que el contenedor esté corriendo: `.\setup-inventario.ps1 -Status`
2. Reiniciar servicios: `.\setup-inventario.ps1 -Restart`
3. Verificar puertos no estén ocupados

### Si hay problemas de permisos:
1. Ejecutar PowerShell como Administrador
2. Verificar política de ejecución: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

**🎯 ¡Con estos scripts tendrás el sistema de inventario corriendo en segundos!**
