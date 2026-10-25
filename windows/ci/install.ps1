[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$PgRoot,
      [Parameter(Mandatory=$true)][string]$UpstreamDir)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$config = Get-Content (Join-Path $PSScriptRoot '../../config/extension.json') -Raw | ConvertFrom-Json
$expectedVersion = [string]$config.upstream.version
if ($expectedVersion -cnotmatch '^[0-9]+\.[0-9]+\.[0-9]+
$control = Join-Path $UpstreamDir 'hypopg.control'
$sql = @(Get-ChildItem $UpstreamDir -File -Filter 'hypopg--*.sql')
if (-not (Test-Path $dll -PathType Leaf) -or -not (Test-Path $control -PathType Leaf) -or
    $sql.Count -eq 0 -or $sql.Name -cnotcontains 'hypopg--$expectedVersion.sql') {
    throw 'Required HypoPG DLL/control/install SQL not found'
}
$actualControl = Get-Content $control -Raw
$escaped = [regex]::Escape($expectedVersion)
if ($actualControl -cnotmatch "(?m)^default_version\s*=\s*'$escaped'\s*$") {
    throw 'Install control version disagrees with immutable manifest'
}
$extdir = Join-Path $PgRoot 'share/extension'
if (-not (Test-Path $extdir)) { throw 'PostgreSQL extension directory missing' }
Copy-Item $dll (Join-Path $PgRoot 'lib/hypopg.dll') -Force
Copy-Item $control (Join-Path $extdir 'hypopg.control') -Force
foreach ($f in $sql) { Copy-Item $f.FullName (Join-Path $extdir $f.Name) -Force }
Write-Host "Installed HypoPG DLL and $($sql.Count) SQL scripts"
 -or [string]$config.upstream.ref -cne $expectedVersion) {
    throw 'Invalid pinned HypoPG SQL install version'
}
$dll = Join-Path $UpstreamDir 'hypopg.dll'
$control = Join-Path $UpstreamDir 'hypopg.control'
$sql = @(Get-ChildItem $UpstreamDir -File -Filter 'hypopg--*.sql')
if (-not (Test-Path $dll -PathType Leaf) -or -not (Test-Path $control -PathType Leaf) -or
    $sql.Count -eq 0 -or $sql.Name -cnotcontains 'hypopg--$expectedVersion.sql') {
    throw 'Required HypoPG DLL/control/install SQL not found'
}
$extdir = Join-Path $PgRoot 'share/extension'
if (-not (Test-Path $extdir)) { throw 'PostgreSQL extension directory missing' }
Copy-Item $dll (Join-Path $PgRoot 'lib/hypopg.dll') -Force
Copy-Item $control (Join-Path $extdir 'hypopg.control') -Force
foreach ($f in $sql) { Copy-Item $f.FullName (Join-Path $extdir $f.Name) -Force }
Write-Host "Installed HypoPG DLL and $($sql.Count) SQL scripts"
