# Genera modelos SQLAlchemy usando sqlacodegen y las variables de .env

$envFile = "$PSScriptRoot\..\.env"
$modelsFile = "$PSScriptRoot\models.py"

# Leer variables de .e nv
$envVars = @{}
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^#][^=]*)=(.*)$') {
        $envVars[$matches[1].Trim()] = $matches[2].Trim()
    }
}

# Construir la cadena de conexión
$db = $envVars.POSTGRES_DB
$user = $envVars.POSTGRES_USER
$pass = $envVars.POSTGRES_PASSWORD
$dbHost = $envVars.POSTGRES_HOST
$port = $envVars.POSTGRES_PORT

$connectionString = "postgresql+psycopg://$user`:$pass@$dbHost`:$port/$db"

# Ejecutar sqlacodegen
Write-Host "Ejecutando: sqlacodegen $connectionString > $modelsFile"
sqlacodegen $connectionString | Out-File -Encoding UTF8 $modelsFile
