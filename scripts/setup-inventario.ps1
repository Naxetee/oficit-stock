# 🚀 Script de PowerShell para Sistema de Inventario
# Este script levanta Docker Compose y conecta a la base de datos oficit-stock

param(
    [switch]$Setup,      # Instalar y configurar por primera vez
    [switch]$Start,      # Solo iniciar servicios
    [switch]$Stop,       # Detener servicios
    [switch]$Restart,    # Reiniciar servicios
    [switch]$Status,     # Ver estado de servicios
    [switch]$Connect,    # Conectar a base de datos
    [switch]$Clean,      # Limpiar contenedores y volúmenes
    [switch]$Help        # Mostrar ayuda
)

# Configuración
$ProjectName = "oficit-stock"
$DockerComposeFile = "docker-compose.yml"
$EnvFile = ".env"

# Colores para output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    switch ($Color) {
        "Success" { Write-Host $Message -ForegroundColor Green }
        "Error"   { Write-Host $Message -ForegroundColor Red }
        "Warning" { Write-Host $Message -ForegroundColor Yellow }
        "Info"    { Write-Host $Message -ForegroundColor Cyan }
        "Header"  { Write-Host $Message -ForegroundColor Magenta }
        default   { Write-Host $Message -ForegroundColor White }
    }
}

# Banner del proyecto
function Show-Banner {
    Write-ColorOutput "╔══════════════════════════════════════════════════════════════════╗" "Header"
    Write-ColorOutput "║                    🎯 SISTEMA DE INVENTARIO                      ║" "Header"
    Write-ColorOutput "║                     PostgreSQL + Docker                          ║" "Header"
    Write-ColorOutput "║                        oficit-stock                              ║" "Header"
    Write-ColorOutput "╚══════════════════════════════════════════════════════════════════╝" "Header"
    Write-Host ""
}

# Verificar que Docker está instalado y corriendo
function Test-DockerInstallation {
    Write-ColorOutput "🔍 Verificando Docker..." "Info"
    
    try {
        $dockerVersion = docker --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker no está instalado"
        }
        Write-ColorOutput "✅ Docker encontrado: $dockerVersion" "Success"
        
        # Verificar que Docker Desktop está corriendo
        $dockerInfo = docker info 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker Desktop no está corriendo"
        }
        Write-ColorOutput "✅ Docker Desktop está corriendo" "Success"
        return $true
    }
    catch {
        Write-ColorOutput "❌ Error: $_" "Error"
        Write-ColorOutput "💡 Asegúrate de que Docker Desktop esté instalado y corriendo" "Warning"
        return $false
    }
}

# Verificar archivos necesarios
function Test-ProjectFiles {
    Write-ColorOutput "📁 Verificando archivos del proyecto..." "Info"
    
    if (-not (Test-Path $DockerComposeFile)) {
        Write-ColorOutput "❌ No se encuentra $DockerComposeFile" "Error"
        return $false
    }
    Write-ColorOutput "✅ $DockerComposeFile encontrado" "Success"
    
    if (-not (Test-Path $EnvFile)) {
        Write-ColorOutput "❌ No se encuentra $EnvFile" "Error"
        return $false
    }
    Write-ColorOutput "✅ $EnvFile encontrado" "Success"
    
    return $true
}

# Cargar variables de entorno
function Get-EnvVariables {
    if (Test-Path $EnvFile) {
        $envVars = @{}
        Get-Content $EnvFile | ForEach-Object {
            if ($_ -match '^([^#][^=]*)=(.*)$') {
                $envVars[$matches[1]] = $matches[2]
            }
        }
        return $envVars
    }
    return @{}
}

# Iniciar servicios Docker
function Start-DockerServices {
    Write-ColorOutput "🚀 Iniciando servicios Docker..." "Info"
    
    try {
        $output = docker-compose up -d 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Servicios iniciados exitosamente" "Success"
            Write-Host ""
            Show-ServiceStatus
            return $true
        } else {
            Write-ColorOutput "❌ Error iniciando servicios:" "Error"
            Write-Host $output
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error: $_" "Error"
        return $false
    }
}

# Detener servicios Docker
function Stop-DockerServices {
    Write-ColorOutput "🛑 Deteniendo servicios Docker..." "Info"
    
    try {
        docker-compose down
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Servicios detenidos exitosamente" "Success"
        } else {
            Write-ColorOutput "❌ Error deteniendo servicios" "Error"
        }
    }
    catch {
        Write-ColorOutput "❌ Error: $_" "Error"
    }
}

# Mostrar estado de servicios
function Show-ServiceStatus {
    Write-ColorOutput "📊 Estado de servicios:" "Info"
    Write-Host ""
    
    try {
        docker-compose ps
        Write-Host ""
        
        # Información adicional de la base de datos
        $envVars = Get-EnvVariables
        Write-ColorOutput "🐘 Información de PostgreSQL:" "Info"
        Write-ColorOutput "   • Base de datos: $($envVars.POSTGRES_DB)" "Info"
        Write-ColorOutput "   • Usuario: $($envVars.POSTGRES_USER)" "Info"
        Write-ColorOutput "   • Puerto: $($envVars.POSTGRES_PORT)" "Info"
        Write-ColorOutput "   • Host: $($envVars.POSTGRES_HOST)" "Info"
        Write-Host ""
    }
    catch {
        Write-ColorOutput "❌ Error obteniendo estado: $_" "Error"
    }
}

# Conectar a la base de datos
function Connect-Database {
    $envVars = Get-EnvVariables
    
    Write-ColorOutput "🔌 Conectando a la base de datos..." "Info"
    Write-Host ""
    
    # Verificar que el servicio está corriendo
    $dbRunning = docker-compose ps db | Select-String "Up"
    if (-not $dbRunning) {
        Write-ColorOutput "❌ El servicio de PostgreSQL no está corriendo" "Error"
        Write-ColorOutput "💡 Ejecuta primero: .\setup-inventario.ps1 -Start" "Warning"
        return
    }
    
    # Información de conexión
    Write-ColorOutput "📋 Información de conexión:" "Info"
    Write-ColorOutput "   Host: $($envVars.POSTGRES_HOST)" "Info"
    Write-ColorOutput "   Puerto: $($envVars.POSTGRES_PORT)" "Info"
    Write-ColorOutput "   Base de datos: $($envVars.POSTGRES_DB)" "Info"
    Write-ColorOutput "   Usuario: $($envVars.POSTGRES_USER)" "Info"
    Write-Host ""
    
    # Crear string de conexión para diferentes herramientas
    $connectionString = "postgresql://$($envVars.POSTGRES_USER):$($envVars.POSTGRES_PASSWORD)@$($envVars.POSTGRES_HOST):$($envVars.POSTGRES_PORT)/$($envVars.POSTGRES_DB)"
    
    Write-ColorOutput "🔗 String de conexión:" "Info"
    Write-ColorOutput "   $connectionString" "Success"
    Write-Host ""
    
    # Opciones de conexión
    Write-ColorOutput "🛠️ Opciones para conectar:" "Info"
    Write-ColorOutput "   1. psql (línea de comandos):" "Info"
    Write-ColorOutput "      psql -h $($envVars.POSTGRES_HOST) -p $($envVars.POSTGRES_PORT) -U $($envVars.POSTGRES_USER) -d $($envVars.POSTGRES_DB)" "Success"
    Write-Host ""
    Write-ColorOutput "   2. Docker exec (acceso directo):" "Info"
    Write-ColorOutput "      docker-compose exec db psql -U $($envVars.POSTGRES_USER) -d $($envVars.POSTGRES_DB)" "Success"
    Write-Host ""
    Write-ColorOutput "   3. DBeaver/pgAdmin:" "Info"
    Write-ColorOutput "      Host: $($envVars.POSTGRES_HOST), Puerto: $($envVars.POSTGRES_PORT)" "Success"
    Write-ColorOutput "      Usuario: $($envVars.POSTGRES_USER), Base de datos: $($envVars.POSTGRES_DB)" "Success"
    Write-Host ""
    
    # Preguntar si quiere conectar directamente
    $connect = Read-Host "¿Quieres conectar directamente con psql? (s/N)"
    if ($connect -eq "s" -or $connect -eq "S" -or $connect -eq "si" -or $connect -eq "SI") {
        Write-ColorOutput "🔌 Conectando con psql..." "Info"
        docker-compose exec db psql -U $($envVars.POSTGRES_USER) -d $($envVars.POSTGRES_DB)
    }
}

# Limpiar contenedores y volúmenes
function Clear-DockerEnvironment {
    Write-ColorOutput "🧹 Limpiando entorno Docker..." "Warning"
    Write-Host ""
    
    $confirm = Read-Host "⚠️  Esto eliminará todos los datos. ¿Estás seguro? (s/N)"
    if ($confirm -eq "s" -or $confirm -eq "S" -or $confirm -eq "si" -or $confirm -eq "SI") {
        Write-ColorOutput "🗑️ Eliminando contenedores y volúmenes..." "Info"
        docker-compose down -v
        docker-compose rm -f
        Write-ColorOutput "✅ Limpieza completada" "Success"
    } else {
        Write-ColorOutput "❌ Operación cancelada" "Info"
    }
}

# Configuración inicial completa
function Initialize-Project {
    Write-ColorOutput "🔧 Configuración inicial del proyecto..." "Info"
    Write-Host ""
    
    if (-not (Test-DockerInstallation)) { return }
    if (-not (Test-ProjectFiles)) { return }
    
    Write-ColorOutput "📦 Descargando imagen de PostgreSQL..." "Info"
    docker-compose pull
    
    if (Start-DockerServices) {
        Write-ColorOutput "⏳ Esperando que PostgreSQL esté listo..." "Info"
        Start-Sleep -Seconds 10
        
        Write-ColorOutput "🎉 ¡Configuración completada!" "Success"
        Write-Host ""
        Write-ColorOutput "📋 Próximos pasos:" "Info"
        Write-ColorOutput "   1. Ejecutar: python ejecutar_ejemplos.py" "Success"
        Write-ColorOutput "   2. O usar: .\setup-inventario.ps1 -Connect" "Success"
        Write-Host ""
    }
}

# Mostrar ayuda
function Show-Help {
    Write-Host ""
    Write-ColorOutput "🚀 Script de Gestión del Sistema de Inventario" "Header"
    Write-Host ""
    Write-ColorOutput "USO:" "Info"
    Write-ColorOutput "   .\setup-inventario.ps1 [OPCIÓN]" "Success"
    Write-Host ""
    Write-ColorOutput "OPCIONES:" "Info"
    Write-ColorOutput "   -Setup      Configuración inicial completa" "Success"
    Write-ColorOutput "   -Start      Iniciar servicios Docker" "Success"
    Write-ColorOutput "   -Stop       Detener servicios Docker" "Success"
    Write-ColorOutput "   -Restart    Reiniciar servicios Docker" "Success"
    Write-ColorOutput "   -Status     Ver estado de servicios" "Success"
    Write-ColorOutput "   -Connect    Conectar a base de datos" "Success"
    Write-ColorOutput "   -Clean      Limpiar contenedores y datos" "Success"
    Write-ColorOutput "   -Help       Mostrar esta ayuda" "Success"
    Write-Host ""
    Write-ColorOutput "EJEMPLOS:" "Info"
    Write-ColorOutput "   .\setup-inventario.ps1 -Setup     # Primera instalación" "Success"
    Write-ColorOutput "   .\setup-inventario.ps1 -Start     # Solo iniciar" "Success"
    Write-ColorOutput "   .\setup-inventario.ps1 -Connect   # Conectar a BD" "Success"
    Write-Host ""
}

# FUNCIÓN PRINCIPAL
function Main {
    Show-Banner
    
    # Si no hay parámetros, mostrar ayuda
    if (-not ($Setup -or $Start -or $Stop -or $Restart -or $Status -or $Connect -or $Clean -or $Help)) {
        Show-Help
        return
    }
    
    # Ejecutar según parámetros
    switch ($true) {
        $Help    { Show-Help }
        $Setup   { Initialize-Project }
        $Start   { 
            if (Test-DockerInstallation -and Test-ProjectFiles) {
                Start-DockerServices 
            }
        }
        $Stop    { Stop-DockerServices }
        $Restart { 
            Stop-DockerServices
            Start-Sleep -Seconds 3
            if (Test-DockerInstallation -and Test-ProjectFiles) {
                Start-DockerServices 
            }
        }
        $Status  { Show-ServiceStatus }
        $Connect { Connect-Database }
        $Clean   { Clear-DockerEnvironment }
    }
}

# Ejecutar función principal
Main
