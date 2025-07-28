# 🚀 Script Rápido - Iniciar Sistema de Inventario
# Levanta Docker y muestra información de conexión

Write-Host "🎯 Iniciando Sistema de Inventario..." -ForegroundColor Cyan
Write-Host ""

# Verificar Docker
try {
    docker --version | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Docker no encontrado" }
} catch {
    Write-Host "❌ Docker no está instalado o no está corriendo" -ForegroundColor Red
    Write-Host "💡 Instala Docker Desktop y asegúrate de que esté corriendo" -ForegroundColor Yellow
    exit 1
}

# Iniciar servicios
Write-Host "🚀 Levantando contenedor PostgreSQL..." -ForegroundColor Green
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Contenedor iniciado exitosamente" -ForegroundColor Green
    Write-Host ""
    
    # Mostrar estado
    Write-Host "📊 Estado del contenedor:" -ForegroundColor Cyan
    docker-compose ps
    Write-Host ""
    
    # Información de conexión
    Write-Host "🔗 Información de conexión PostgreSQL:" -ForegroundColor Cyan
    Write-Host "   • Host: localhost" -ForegroundColor White
    Write-Host "   • Puerto: 5432" -ForegroundColor White
    Write-Host "   • Base de datos: oficit_stock" -ForegroundColor White
    Write-Host "   • Usuario: oficit" -ForegroundColor White
    Write-Host "   • Contraseña: root" -ForegroundColor White
    Write-Host ""
    
    Write-Host "🎯 Para usar el sistema:" -ForegroundColor Yellow
    Write-Host "   1. python ejecutar_ejemplos.py" -ForegroundColor Green
    Write-Host "   2. .\setup-inventario.ps1 -Connect" -ForegroundColor Green
    Write-Host ""
    
    # Preguntar si quiere conectar
    $connect = Read-Host "¿Conectar directamente a la base de datos? (s/N)"
    if ($connect -eq "s" -or $connect -eq "S") {
        Write-Host "🔌 Conectando..." -ForegroundColor Green
        docker-compose exec db psql -U oficit -d oficit_stock
    }
    
} else {
    Write-Host "❌ Error iniciando el contenedor" -ForegroundColor Red
    Write-Host "💡 Verifica que Docker Desktop esté corriendo" -ForegroundColor Yellow
}
