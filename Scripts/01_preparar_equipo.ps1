<#
01_preparar_equipo.ps1 — Verifica y prepara un equipo para correr agentes del proyecto.

Entrada : ninguna (se ubica solo desde la carpeta Scripts\ del proyecto sincronizado)
Salida  : _harness\logs\setup-<EQUIPO>-<DD-MM-AAAA>.md con el resultado de cada chequeo
Acciones: instala paquetes Python de Scripts\requirements.txt (pip --user). Con -Pin,
          pide a OneDrive mantener en el equipo las carpetas que usan los agentes.
          No instala RevitCortex (eso es MCP Revit\instalar_revitcortex.ps1).
Uso     : powershell -ExecutionPolicy Bypass -File .\Scripts\01_preparar_equipo.ps1 [-Pin]
Fecha   : 23-11-2026 · Dueño: CL-1 · Idempotente.
#>
param([switch]$Pin)
$ErrorActionPreference = "Continue"
$Root   = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Equipo = $env:COMPUTERNAME
$Fecha  = Get-Date -Format "dd-MM-yyyy"
$Log    = Join-Path $Root "_harness\logs\setup-$Equipo-$Fecha.md"
$res    = New-Object System.Collections.Generic.List[string]
function Add-Check($ok, $item, $detalle) {
    $m = if ($ok) { "OK " } else { "FALTA" }
    $res.Add("| $m | $item | $detalle |")
    $c = if ($ok) { "Green" } else { "Yellow" }
    Write-Host ("[{0}] {1} - {2}" -f $m, $item, $detalle) -ForegroundColor $c
}

Write-Host "Proyecto: $Root" -ForegroundColor Cyan

# 1. Estructura del proyecto
foreach ($d in @("CLAUDE.md","AGENTS.md","HARNESS.md","_harness\cola.md","_harness\specs","Scripts\schemas","Modelo federado\modelo_federado.rvt")) {
    Add-Check (Test-Path (Join-Path $Root $d)) "Proyecto: $d" "sincronizado"
}

# 2. Vínculos del federado (rutas relativas ..\..\Archivos revit\)
$arch = Join-Path (Split-Path -Parent $Root) "Archivos revit"
$links = @(
 "Estructura_2027\00_ Edificio de educacion\Edificio de educacion.rvt",
 "Acabados_2027\theriam\Proyecto acabado-DAMIAN.rvt",
 "Herrería y Cancelería_2027\TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt",
 "Instalacion IHS_2027\Instalaciones.rvt",
 "Instalacion Electrica_2027\Copias de seguridad\Proyecto electrico_corregido.rvt",
 "TT-ED-EDU-ARQ-MOB.rvt")
foreach ($l in $links) {
    $p = Join-Path $arch $l
    $ok = Test-Path -LiteralPath $p
    $det = "no encontrado en $arch"
    if ($ok) {
        $a = (Get-Item -LiteralPath $p).Attributes.ToString()
        $det = if ($a -match "Offline|RecallOnDataAccess") { "solo en la nube: usar -Pin o 'Mantener siempre en este dispositivo'" } else { "local" }
    }
    Add-Check $ok "Vínculo: $l" $det
}

# 3. Python
$py = Get-Command py -ErrorAction SilentlyContinue
Add-Check ([bool]$py) "Python launcher 'py'" $(if ($py) { (& py --version) } else { "instalar Python 3.12+ desde python.org (no el alias de Store)" })
if ($py) {
    & py -m pip install --user -q -r (Join-Path $Root "Scripts\requirements.txt")
    $mods = & py -c "import pydantic,openpyxl,pdfplumber;print('ok')" 2>$null
    Add-Check ($mods -eq "ok") "Paquetes Python" "pydantic, openpyxl, pdfplumber"
    $v = & py (Join-Path $Root "Scripts\schemas\validar.py") 2>$null
    Add-Check ($LASTEXITCODE -eq 2) "Scripts/schemas/validar.py" "carga los schemas"
}

# 4. Revit y pyRevit
$rv = Test-Path "C:\Program Files\Autodesk\Revit 2027\Revit.exe"
Add-Check $rv "Revit 2027" "C:\Program Files\Autodesk\Revit 2027"
$pr = Get-Command pyrevit -ErrorAction SilentlyContinue
Add-Check ([bool]$pr) "pyRevit CLI" $(if ($pr) { (& pyrevit --version 2>$null | Select-Object -First 1) } else { "instalar pyRevit 7 y adjuntarlo a 2027" })
if ($pr) {
    $st = (& pyrevit agent status 2>&1) -join " "
    Add-Check ($st -notmatch "No running Revit") "Revit abierto con agent host" $st
}

# 5. RevitCortex
$rc = Join-Path $env:USERPROFILE ".revitcortex\server\RevitCortex.Server.exe"
Add-Check (Test-Path $rc) "RevitCortex servidor" $(if (Test-Path $rc) { $rc } else { "correr 'MCP Revit\instalar_revitcortex.ps1' con Revit cerrado" })
$addin = @("C:\ProgramData\Autodesk\Revit\Addins\2027\RevitCortex.addin", (Join-Path $env:APPDATA "Autodesk\Revit\Addins\2027\RevitCortex.addin")) | Where-Object { Test-Path $_ }
Add-Check ([bool]$addin) "RevitCortex add-in 2027" $(if ($addin) { $addin -join ", " } else { "no instalado" })

# 6. Excel (recálculo de la hoja sobrecosto por COM)
$xl = $false
try { $x = New-Object -ComObject Excel.Application; $xl = $true; $x.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($x) } catch {}
Add-Check $xl "Excel COM" "necesario para recalcular D25-00_Sobrecosto (CX-1)"

# 7. Clientes de agentes
foreach ($c in @("claude","codex","antigravity")) {
    $g = Get-Command $c -ErrorAction SilentlyContinue
    Add-Check ([bool]$g) "CLI $c" $(if ($g) { $g.Source } else { "no encontrado (ok si no se usa en este equipo)" })
}

# 8. OneDrive: mantener en el equipo
if ($Pin) {
    foreach ($d in @($Root, $arch)) { attrib +P -U "$d\*" /S /D | Out-Null }
    Add-Check $true "OneDrive pin" "solicitado para proyecto y Archivos revit"
}

# Conflictos de OneDrive
$conf = Get-ChildItem $Root -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "-$Equipo|conflict|conflicto" }
Add-Check (-not $conf) "Copias de conflicto OneDrive" $(if ($conf) { ($conf | Select-Object -First 5 | ForEach-Object Name) -join ", " } else { "ninguna" })

$hdr = @("# Setup $Equipo · $Fecha", "", "Proyecto: $Root", "", "| Estado | Chequeo | Detalle |", "|---|---|---|")
New-Item -ItemType Directory -Force -Path (Split-Path $Log) | Out-Null
($hdr + $res) | Out-File -FilePath $Log -Encoding utf8
Write-Host "`nReporte: $Log" -ForegroundColor Cyan
