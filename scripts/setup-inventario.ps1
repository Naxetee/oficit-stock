# Script de PowerShell para Sistema de Inventario
# Este script levanta Docker Compose y conecta a la base de datos oficit-stock

param(
    [switch]$Setup,      # Instalar y configurar por primera vez
    [switch]$Start,      # Solo iniciar servicios
    [switch]$Stop,       # Detener servicios
    [switch]$Restart,    # Reiniciar servicios
    [switch]$Status,     # Ver estado de servicios
    [switch]$Connect,    # Conectar a base de datos
    [switch]$Clean,      # Limpiar contenedores y volumenes
    [switch]$Help        # Mostrar ayuda
)

# Configuracion
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
    Write-ColorOutput "=================================================================" "Header"
    Write-ColorOutput "                    SISTEMA DE INVENTARIO                        " "Header"
    Write-ColorOutput "                     PostgreSQL + Docker                         " "Header"
    Write-ColorOutput "                        oficit-stock                             " "Header"
    Write-ColorOutput "=================================================================" "Header"
    Write-Host ""
}

# Verificar que Docker esta instalado y corriendo
function Test-DockerInstallation {
    Write-ColorOutput "[INFO] Verificando Docker..." "Info"

    try {
        $dockerVersion = docker --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker no esta instalado"
        }
        Write-ColorOutput "[OK] Docker encontrado: $dockerVersion" "Success"

        # Verificar que Docker Desktop esta corriendo
        $dockerInfo = docker info 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker Desktop no esta corriendo"
        }
        Write-ColorOutput "[OK] Docker Desktop esta corriendo" "Success"
        return $true
    }
    catch {
        Write-ColorOutput "[ERROR] Error: $_" "Error"
        Write-ColorOutput "[WARN] Asegurate de que Docker Desktop este instalado y corriendo" "Warning"
        return $false
    }
}

# Verificar archivos necesarios
function Test-ProjectFiles {
    Write-ColorOutput "[INFO] Verificando archivos del proyecto..." "Info"

    if (-not (Test-Path $DockerComposeFile)) {
        Write-ColorOutput "[ERROR] No se encuentra $DockerComposeFile" "Error"
        return $false
    }
    Write-ColorOutput "[OK] $DockerComposeFile encontrado" "Success"

    if (-not (Test-Path $EnvFile)) {
        Write-ColorOutput "[ERROR] No se encuentra $EnvFile" "Error"
        return $false
    }
    Write-ColorOutput "[OK] $EnvFile encontrado" "Success"

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
    Write-ColorOutput "[INFO] Iniciando servicios Docker..." "Info"

    try {
        $output = docker-compose up -d 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "[OK] Servicios iniciados exitosamente" "Success"
            Write-Host ""
            Show-ServiceStatus
            return $true
        } else {
            Write-ColorOutput "[ERROR] Error iniciando servicios:" "Error"
            Write-Host $output
            return $false
        }
    }
    catch {
        Write-ColorOutput "[ERROR] Error: $_" "Error"
        return $false
    }
}

# Detener servicios Docker
function Stop-DockerServices {
    Write-ColorOutput "[INFO] Deteniendo servicios Docker..." "Info"

    try {
        docker-compose down
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "[OK] Servicios detenidos exitosamente" "Success"
        } else {
            Write-ColorOutput "[ERROR] Error deteniendo servicios" "Error"
        }
    }
    catch {
        Write-ColorOutput "[ERROR] Error: $_" "Error"
    }
}

# Mostrar estado de servicios
function Show-ServiceStatus {
    Write-ColorOutput "[INFO] Estado de servicios:" "Info"
    Write-Host ""

    try {
        docker-compose ps
        Write-Host ""

        # Informacion adicional de la base de datos
        $envVars = Get-EnvVariables
        Write-ColorOutput "[INFO] Informacion de PostgreSQL:" "Info"
        Write-ColorOutput "   - Base de datos: $($envVars.POSTGRES_DB)" "Info"
        Write-ColorOutput "   - Usuario: $($envVars.POSTGRES_USER)" "Info"
        Write-ColorOutput "   - Puerto: $($envVars.POSTGRES_PORT)" "Info"
        Write-ColorOutput "   - Host: $($envVars.POSTGRES_HOST)" "Info"
        Write-Host ""
    }
    catch {
        Write-ColorOutput "[ERROR] Error obteniendo estado: $_" "Error"
    }
}

# Conectar a la base de datos
function Connect-Database {
    $envVars = Get-EnvVariables

    Write-ColorOutput "[INFO] Conectando a la base de datos..." "Info"
    Write-Host ""

    # Verificar que el servicio esta corriendo
    $dbRunning = docker-compose ps db | Select-String "Up"
    if (-not $dbRunning) {
        Write-ColorOutput "[ERROR] El servicio de PostgreSQL no esta corriendo" "Error"
        Write-ColorOutput "[WARN] Ejecuta primero: .\setup-inventario.ps1 -Start" "Warning"
        return
    }

    # Informacion de conexion
    Write-ColorOutput "[INFO] Informacion de conexion:" "Info"
    Write-ColorOutput " - Host: $($envVars.POSTGRES_HOST)" "Info"
    Write-ColorOutput " - Puerto: $($envVars.POSTGRES_PORT)" "Info"
    Write-ColorOutput " - Base de datos: $($envVars.POSTGRES_DB)" "Info"
    Write-ColorOutput " - Usuario: $($envVars.POSTGRES_USER)" "Info"
    Write-Host ""

    # Crear string de conexion para diferentes herramientas
    $connectionString = "postgresql://$($envVars.POSTGRES_USER):$($envVars.POSTGRES_PASSWORD)@$($envVars.POSTGRES_HOST):$($envVars.POSTGRES_PORT)/$($envVars.POSTGRES_DB)"

    # Opciones de conexion
    Write-ColorOutput "[INFO] Opciones para conectar:" "Info"
    Write-ColorOutput "   1. psql (linea de comandos):" "Info"
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
        Write-ColorOutput "[INFO] Conectando con psql..." "Info"
        docker-compose exec db psql -U $($envVars.POSTGRES_USER) -d $($envVars.POSTGRES_DB)
    }
}

# Limpiar contenedores y volumenes
function Clear-DockerEnvironment {
    Write-ColorOutput "[WARN] Limpiando entorno Docker..." "Warning"
    Write-Host ""

    $confirm = Read-Host "ATENCION: Esto eliminara todos los datos. ¿Estas seguro? (s/N)"
    if ($confirm -eq "s" -or $confirm -eq "S" -or $confirm -eq "si" -or $confirm -eq "SI") {
        Write-ColorOutput "[INFO] Eliminando contenedores y volumenes..." "Info"
        docker-compose down -v
        docker-compose rm -f
        Write-ColorOutput "[OK] Limpieza completada" "Success"
    } else {
        Write-ColorOutput "[INFO] Operacion cancelada" "Info"
    }
}

# Configuracion inicial completa
function Initialize-Project {
    Write-ColorOutput "[INFO] Configuracion inicial del proyecto..." "Info"
    Write-Host ""

    if (-not (Test-DockerInstallation)) { return }
    if (-not (Test-ProjectFiles)) { return }

    Write-ColorOutput "[INFO] Descargando imagen de PostgreSQL..." "Info"
    docker-compose pull

    if (Start-DockerServices) {
        Write-ColorOutput "[INFO] Esperando que PostgreSQL este listo..." "Info"
        Start-Sleep -Seconds 10

        Write-ColorOutput "[OK] Configuracion completada!" "Success"
        Write-Host ""
        Write-ColorOutput "[INFO] Proximos pasos:" "Info"
        Write-ColorOutput "   1. Ejecutar: python ejecutar_ejemplos.py" "Success"
        Write-ColorOutput "   2. O usar: .\setup-inventario.ps1 -Connect" "Success"
        Write-Host ""
    }
}

# Mostrar ayuda
function Show-Help {
    Write-Host ""
    Write-ColorOutput "Script de Gestion del Sistema de Inventario" "Header"
    Write-Host ""
    Write-ColorOutput "USO:" "Info"
    Write-ColorOutput "   .\setup-inventario.ps1 [OPCION]" "Success"
    Write-Host ""
    Write-ColorOutput "OPCIONES:" "Info"
    Write-ColorOutput "   -Setup      Configuracion inicial completa" "Success"
    Write-ColorOutput "   -Start      Iniciar servicios Docker" "Success"
    Write-ColorOutput "   -Stop       Detener servicios Docker" "Success"
    Write-ColorOutput "   -Restart    Reiniciar servicios Docker" "Success"
    Write-ColorOutput "   -Status     Ver estado de servicios" "Success"
    Write-ColorOutput "   -Connect    Conectar a base de datos" "Success"
    Write-ColorOutput "   -Clean      Limpiar contenedores y datos" "Success"
    Write-ColorOutput "   -Help       Mostrar esta ayuda" "Success"
    Write-Host ""
    Write-ColorOutput "EJEMPLOS:" "Info"
    Write-ColorOutput "   .\setup-inventario.ps1 -Setup     # Primera instalacion" "Success"
    Write-ColorOutput "   .\setup-inventario.ps1 -Start     # Solo iniciar" "Success"
    Write-ColorOutput "   .\setup-inventario.ps1 -Connect   # Conectar a BD" "Success"
    Write-Host ""
}

# FUNCION PRINCIPAL
function Main {
    Show-Banner

    # Si no hay parametros, mostrar ayuda
    if (-not ($Setup -or $Start -or $Stop -or $Restart -or $Status -or $Connect -or $Clean -or $Help)) {
        Show-Help
        return
    }

    # Ejecutar segun parametros
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

# Ejecutar funcion principal
Main
