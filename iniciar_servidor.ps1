# Script de inicio para PowerShell
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   CLÍNICA ODONTOLÓGICA 'SONRISA PERFECTA' - INICIANDO SISTEMA" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Comprobar puerto 8000 o alternativo
$port = 8000
$testSocket = New-Object System.Net.Sockets.TcpClient
try {
    $testSocket.Connect("127.0.0.1", $port)
    $testSocket.Close()
    Write-Host "[AVISO] El puerto 8000 está ocupado por otro de sus proyectos. Usando puerto 8088..." -ForegroundColor Yellow
    $port = 8088
} catch {
    # Puerto libre
}

Write-Host "`nIniciando servidor web en: http://127.0.0.1:$port/" -ForegroundColor Green
Write-Host "Credenciales precargadas:" -ForegroundColor White
Write-Host " - Administrador: admin / admin123" -ForegroundColor Gray
Write-Host " - Recepción:     recepcion / recepcion123`n" -ForegroundColor Gray

python manage.py runserver 127.0.0.1:$port
