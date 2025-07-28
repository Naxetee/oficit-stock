# 🛑 Script para Detener Sistema de Inventario

Write-Host "🛑 Deteniendo Sistema de Inventario..." -ForegroundColor Yellow
Write-Host ""

# Detener servicios
Write-Host "⏹️ Deteniendo contenedor PostgreSQL..." -ForegroundColor Red
docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Servicios detenidos exitosamente" -ForegroundColor Green
    Write-Host ""
    
    # Mostrar estado final
    Write-Host "📊 Estado final:" -ForegroundColor Cyan
    docker-compose ps
    Write-Host ""
    
    Write-Host "💡 Para volver a iniciar:" -ForegroundColor Yellow
    Write-Host "   .\iniciar.ps1" -ForegroundColor Green
    Write-Host "   o" -ForegroundColor White
    Write-Host "   .\setup-inventario.ps1 -Start" -ForegroundColor Green
    
} else {
    Write-Host "❌ Error deteniendo servicios" -ForegroundColor Red
}
