<#
instalar_revitcortex.ps1 — Instala RevitCortex v1.0.50 desde el ZIP de la carpeta compartida.

Entrada : MCP Revit\instalador\RevitCortex-v1.0.50.zip (release oficial
          github.com/LuDattilo/revitcortex-releases, SHA256 abajo)
Salida  : add-in en C:\ProgramData\Autodesk\Revit\Addins\<año>\RevitCortex\
          servidor MCP en %USERPROFILE%\.revitcortex\server\RevitCortex.Server.exe
          registro MCP en Claude Code (si existe `claude`) y Codex (si existe ~/.codex)
Requiere: Revit CERRADO. Se ejecuta con clic derecho > "Ejecutar con PowerShell"
          o:  powershell -ExecutionPolicy Bypass -File ".\MCP Revit\instalar_revitcortex.ps1"
          Pide permisos de administrador (UAC). No agrega exclusiones de Defender.
Fecha   : 23-11-2026 · Dueño: CL-1
Idempotente: reinstalar sobrescribe la misma versión.
#>
$ErrorActionPreference = "Stop"
$Here    = Split-Path -Parent $MyInvocation.MyCommand.Path
$Zip     = Join-Path $Here "instalador\RevitCortex-v1.0.50.zip"
$Dir     = Join-Path $Here "instalador\RevitCortex-v1.0.50"
$Sha256  = "D8B9AA9CC6319AB9939CD81423011A4CEF4CF8BBDFE5499BEE7125099F13AB6E"

if (-not (Test-Path $Zip)) { throw "No existe $Zip. Revisa que OneDrive haya sincronizado la carpeta MCP Revit\instalador." }
$h = (Get-FileHash $Zip -Algorithm SHA256).Hash
if ($h -ne $Sha256) { throw "SHA256 no coincide ($h). No instalar: el ZIP está incompleto o alterado." }
Write-Host "ZIP verificado (SHA256 OK)" -ForegroundColor Green

if (Get-Process -Name Revit -ErrorAction SilentlyContinue) {
    throw "Revit está abierto. Ciérralo y vuelve a correr este script."
}

if (-not (Test-Path (Join-Path $Dir "install.ps1"))) {
    Write-Host "Extrayendo ZIP..."
    Expand-Archive -Path $Zip -DestinationPath $Dir -Force
}
Get-ChildItem $Dir -Recurse -File | Unblock-File -ErrorAction SilentlyContinue

# Instalador oficial en modo silencioso (sin Defender, configura Claude Desktop)
$inst = Join-Path $Dir "install.ps1"
Write-Host "Ejecutando instalador oficial (acepta la ventana de administrador)..." -ForegroundColor Yellow
$p = Start-Process powershell -Verb RunAs -Wait -PassThru -ArgumentList "-ExecutionPolicy Bypass -NoProfile -File `"$inst`" -Silent"
if ($p.ExitCode -ne 0) { throw "El instalador terminó con código $($p.ExitCode)" }

$exe = Join-Path $env:USERPROFILE ".revitcortex\server\RevitCortex.Server.exe"
if (-not (Test-Path $exe)) { throw "No se encontró $exe tras la instalación." }
Write-Host "Servidor: $exe" -ForegroundColor Green

# Registro en Claude Code (scope usuario) y Codex
if (Get-Command claude -ErrorAction SilentlyContinue) {
    & claude mcp remove revitcortex --scope user 2>$null | Out-Null
    & claude mcp add revitcortex --scope user -- "$exe"
    Write-Host "Claude Code: revitcortex registrado (scope user)" -ForegroundColor Green
} else {
    Write-Host "Claude Code CLI no encontrado. Si lo usas: claude mcp add revitcortex --scope user -- `"$exe`"" -ForegroundColor Yellow
}
$codexCfg = Join-Path $env:USERPROFILE ".codex\config.toml"
if (Test-Path (Split-Path $codexCfg)) {
    $txt = if (Test-Path $codexCfg) { Get-Content $codexCfg -Raw } else { "" }
    if ($txt -notmatch "\[mcp_servers\.revitcortex\]") {
        $esc = $exe -replace '\\', '\\'
        Add-Content -Path $codexCfg -Encoding utf8 -Value "`n[mcp_servers.revitcortex]`ncommand = `"$esc`"`n"
        Write-Host "Codex: revitcortex agregado a $codexCfg" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Listo. Abre Revit 2027: pestaña RevitCortex > 'Cortex Switch' para encender el servidor MCP." -ForegroundColor Cyan
Write-Host "Luego reinicia Claude / Codex / Antigravity para que carguen el MCP." -ForegroundColor Cyan
