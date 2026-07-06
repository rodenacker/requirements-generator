#requires -Version 7.0
<#
.SYNOPSIS
  Environment setup for the requirements-generator workspace. Detects, installs (user
  scope), configures, and tests the external dependencies the pipelines need.

.DESCRIPTION
  Component-addressable and idempotent. Run the whole core set (default) via /setup, or a
  single component from an agent's just-in-time refusal handback (e.g. -Component markitdown).
  Detection-first: a dependency that is already present is verified and left untouched.

  This script is the CANONICAL home for each tool's install command. The setup-instruction
  docs under framework/shared/setup-instructions/ and the RF-01/06/10/11 refusal handbacks
  reference this script by component name instead of restating commands. It installs and tests
  ENVIRONMENT dependencies only; it never reads or writes pipeline artefacts.

.PARAMETER Component
  Which dependency to act on:
    all (default)            python, markitdown, node, mmdc, drawio, playwright  (full core set)
    core                     python, markitdown, node, mmdc, playwright  (items 1-6; `all` minus drawio + on-demand renderers)
    markitdown               Office/PDF converters + markitdown-mcp  (the Office-extras fix)
    drawio                   draw.io Desktop + the `drawio` PATH shim  (the shim fix)
    node | python            language runtimes
    mmdc                     @mermaid-js/mermaid-cli
    playwright               warm the @playwright/mcp npx cache
    inkscape | libreoffice   on-demand vector renderers (NOT part of `all`)

.PARAMETER Probe
  Detect-only. Report status, install nothing. Used for the post-restart confirmation pass
  and by agents that only want a status read.

.OUTPUTS
  Human-readable per-component lines on the host, then a machine-readable JSON array between
  the ===SETUP-ENVIRONMENT-SUMMARY-BEGIN/END=== sentinels for the caller (/setup) to parse.
  Status values: ready | installed-pending-restart | failed | absent | n/a.

.NOTES
  Windows caches PATH and the MCP tool list at session start, so anything this script freshly
  installs or shims reports `installed-pending-restart`: it is on disk, but the running Claude
  Code session cannot use it until you restart. Re-run with -Probe after restarting to confirm.
#>
[CmdletBinding()]
param(
  [ValidateSet('all','core','markitdown','drawio','node','python','mmdc','playwright','inkscape','libreoffice')]
  [string]$Component = 'all',
  [switch]$Probe
)

$ErrorActionPreference = 'Continue'
$script:results = @()

# ---------- helpers ----------

function Add-Result {
  param(
    [string]$Name, [string]$Status, [string]$Detail, [string]$Gates,
    [bool]$RestartNeeded = $false
  )
  $script:results += [pscustomobject]@{
    component = $Name; status = $Status; detail = $Detail
    gates = $Gates; restartNeeded = $RestartNeeded
  }
  $glyph = switch ($Status) {
    'ready'                     { 'OK' }
    'installed-pending-restart' { '**' }
    'failed'                    { 'XX' }
    'absent'                    { '--' }
    default                     { '..' }
  }
  Write-Host ("  [{0}] {1,-11} {2,-26} {3}" -f $glyph, $Name, $Status, $Detail)
}

function Test-Cmd { param([string]$Name) [bool](Get-Command $Name -ErrorAction SilentlyContinue) }

function Get-SemverFrom {
  param([string]$Name, [string[]]$VersionArgs = @('--version'))
  try {
    $text = (& $Name @VersionArgs 2>&1 | Out-String)
    if ($text -match '(\d+)\.(\d+)(?:\.(\d+))?') {
      return [version]("{0}.{1}.{2}" -f $Matches[1], $Matches[2], ($Matches[3] ?? '0'))
    }
  } catch { }
  return $null
}

function Invoke-Winget {
  param([string]$Id)
  & winget install --exact --id $Id --silent --accept-package-agreements --accept-source-agreements --disable-interactivity 2>&1 | Out-Null
  return $LASTEXITCODE
}

# Locate an executable under the common per-user / per-machine install roots.
function Find-Exe {
  param([string]$FileName)
  $roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}, "$env:LOCALAPPDATA\Programs") |
           Where-Object { $_ -and (Test-Path $_) }
  foreach ($r in $roots) {
    $hit = Get-ChildItem $r -Recurse -Filter $FileName -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) { return $hit.FullName }
  }
  return $null
}

# Write a `<name>.cmd` shim that forwards to an .exe, into the conventional winget Links dir,
# and make sure that dir is on the user PATH. Returns whether the dir was already on PATH
# (i.e. whether the shim resolves without a restart).
function Set-Shim {
  param([string]$Name, [string]$ExePath)
  $shimDir = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Links'
  if (-not (Test-Path $shimDir)) { New-Item -ItemType Directory -Path $shimDir -Force | Out-Null }
  $shimPath = Join-Path $shimDir "$Name.cmd"
  "@echo off`r`n`"$ExePath`" %*" | Set-Content -Path $shimPath -Encoding ascii
  $onPath = (($env:PATH -split ';') -contains $shimDir)
  if (-not $onPath) {
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if (($userPath -split ';') -notcontains $shimDir) {
      [Environment]::SetEnvironmentVariable('Path', ($userPath.TrimEnd(';') + ';' + $shimDir), 'User')
    }
    $env:PATH = $env:PATH.TrimEnd(';') + ';' + $shimDir
  }
  return [pscustomobject]@{ shimPath = $shimPath; shimDir = $shimDir; alreadyOnPath = $onPath }
}

function Test-MarkitdownConverters {
  if (-not (Test-Cmd 'python')) { return $false }
  & python -c 'import mammoth, pptx, openpyxl, xlrd, pdfminer' *> $null
  return ($LASTEXITCODE -eq 0)
}

# ---------- components ----------

function Setup-Python {
  $gates = 'markitdown (Office/PDF conversion)'
  if (Test-Cmd 'python') {
    $v = Get-SemverFrom 'python'
    if ($v -and $v -ge [version]'3.10') { Add-Result 'python' 'ready' "Python $v" $gates; return }
    if ($Probe) { Add-Result 'python' 'absent' "Python $v (<3.10)" $gates; return }
  } elseif ($Probe) { Add-Result 'python' 'absent' 'not found' $gates; return }

  Write-Host '  installing Python 3.12 via winget...'
  if ((Invoke-Winget 'Python.Python.3.12') -eq 0) {
    Add-Result 'python' 'installed-pending-restart' 'Python 3.12 installed' $gates $true
  } else {
    Add-Result 'python' 'failed' 'winget failed -- see setup-instructions/markitdown.md' $gates
  }
}

function Setup-Markitdown {
  $gates = '.docx/.pptx/.xlsx/.xls/.pdf inputs'
  $convOk = Test-MarkitdownConverters
  $mcpOk  = Test-Cmd 'markitdown-mcp'
  if ($convOk -and $mcpOk) {
    Add-Result 'markitdown' 'ready' 'all converters import; markitdown-mcp present' $gates; return
  }
  if ($Probe) {
    $miss = @(); if (-not $convOk) { $miss += 'converters' }; if (-not $mcpOk) { $miss += 'markitdown-mcp' }
    Add-Result 'markitdown' 'absent' ("missing: " + ($miss -join ', ')) $gates; return
  }
  if (-not (Test-Cmd 'python')) {
    Add-Result 'markitdown' 'failed' 'Python 3.10+ required first (run -Component python)' $gates; return
  }

  # 1) Office/PDF converters for the markitdown library. Install the SCOPED extras only -- never
  #    markitdown[all] and never --upgrade. markitdown-mcp depends on markitdown[all], whose
  #    youtube-transcript-api / onnxruntime pins have no wheels on newer Python (e.g. 3.14), so
  #    re-resolving [all] fails (ResolutionImpossible). The scoped extras resolve cleanly.
  if (-not $convOk) {
    Write-Host '  installing markitdown Office/PDF converters (scoped extras)...'
    & python -m pip install --disable-pip-version-check 'markitdown[docx,pptx,xlsx,xls,pdf,outlook]'
  }

  # 2) MCP server -- only if missing. Use --no-deps to avoid dragging in markitdown[all], then
  #    add its real runtime dep (mcp). markitdown itself is already present from step 1.
  if (-not $mcpOk) {
    Write-Host '  installing markitdown-mcp server (--no-deps to avoid the [all] conflict)...'
    & python -m pip install --disable-pip-version-check --no-deps 'markitdown-mcp==0.0.1a4'
    & python -m pip install --disable-pip-version-check 'mcp~=1.8.0'
    $mcpOk = Test-Cmd 'markitdown-mcp'
  }

  if ((Test-MarkitdownConverters) -and $mcpOk) {
    Add-Result 'markitdown' 'installed-pending-restart' 'converters OK (docx,pptx,xlsx,xls,pdf); restart so markitdown-mcp reloads' $gates $true
  } elseif (Test-MarkitdownConverters) {
    Add-Result 'markitdown' 'failed' 'converters OK but markitdown-mcp missing -- see setup-instructions/markitdown.md' $gates
  } else {
    Add-Result 'markitdown' 'failed' 'converter import still fails -- see setup-instructions/markitdown.md' $gates
  }
}

function Setup-Node {
  $gates = '/prototype, Playwright MCP (npx)'
  if (Test-Cmd 'node') {
    $v = Get-SemverFrom 'node'
    if ($v -and $v -ge [version]'20.0') { Add-Result 'node' 'ready' "Node $v" $gates; return }
    if ($Probe) { Add-Result 'node' 'absent' "Node $v (<20)" $gates; return }
  } elseif ($Probe) { Add-Result 'node' 'absent' 'not found' $gates; return }

  Write-Host '  installing Node.js LTS via winget...'
  if ((Invoke-Winget 'OpenJS.NodeJS.LTS') -eq 0) {
    Add-Result 'node' 'installed-pending-restart' 'Node LTS installed' $gates $true
  } else {
    Add-Result 'node' 'failed' 'winget failed -- see setup-instructions/node-toolchain.md' $gates
  }
}

function Setup-Mmdc {
  $gates = '/requirements §2.4 domain-model Mermaid validation (drafter step 9, mermaid-validator.md)'
  if (Test-Cmd 'mmdc') { Add-Result 'mmdc' 'ready' ("mmdc " + (Get-SemverFrom 'mmdc')) $gates; return }
  if ($Probe) { Add-Result 'mmdc' 'absent' 'not found' $gates; return }
  if (-not (Test-Cmd 'npm')) { Add-Result 'mmdc' 'failed' 'npm (Node.js) required first' $gates; return }

  Write-Host '  installing @mermaid-js/mermaid-cli globally...'
  & npm install -g '@mermaid-js/mermaid-cli' 2>&1 | Out-Null
  if ($LASTEXITCODE -eq 0) {
    Add-Result 'mmdc' 'installed-pending-restart' 'mermaid-cli installed' $gates $true
  } else {
    Add-Result 'mmdc' 'failed' 'npm failed -- see setup-instructions/mmdc.md' $gates
  }
}

function Setup-Drawio {
  $gates = '.drawio inputs (primary render path)'
  if (Test-Cmd 'drawio') { Add-Result 'drawio' 'ready' "resolves: $((Get-Command drawio).Source)" $gates; return }
  if ($Probe) { Add-Result 'drawio' 'absent' 'drawio not on PATH' $gates; return }

  $exe = Find-Exe 'draw.io.exe'
  if (-not $exe) {
    Write-Host '  installing draw.io Desktop via winget...'
    Invoke-Winget 'JGraph.Draw' | Out-Null
    $exe = Find-Exe 'draw.io.exe'
  }
  if (-not $exe) {
    Add-Result 'drawio' 'failed' 'draw.io.exe not found after install -- see setup-instructions/visual-render.md' $gates; return
  }

  $shim = Set-Shim 'drawio' $exe
  if ($shim.alreadyOnPath -and (Test-Cmd 'drawio')) {
    Add-Result 'drawio' 'ready' "shim -> $($shim.shimPath)" $gates
  } else {
    Add-Result 'drawio' 'installed-pending-restart' "shim written; added $($shim.shimDir) to user PATH" $gates $true
  }
}

function Setup-Playwright {
  $gates = '/design-system URL extraction, /prototype smoke'
  if ($Probe) { Add-Result 'playwright' 'n/a' 'launched via npx; MCP tool verified by /setup' $gates; return }
  if (-not (Test-Cmd 'npx')) { Add-Result 'playwright' 'failed' 'npx (Node.js) required first' $gates; return }

  Write-Host '  warming @playwright/mcp npx cache...'
  & npx -y '@playwright/mcp@0.0.76' --help *> $null
  if ($LASTEXITCODE -eq 0) {
    Add-Result 'playwright' 'ready' 'npx cache warmed; server registered in .mcp.json' $gates
  } else {
    Add-Result 'playwright' 'failed' 'npx failed -- see setup-instructions/playwright.md' $gates
  }
}

function Setup-Inkscape {
  $gates = '.svg inputs (on-demand)'
  if (Test-Cmd 'inkscape')     { Add-Result 'inkscape' 'ready' ("inkscape " + (Get-SemverFrom 'inkscape')) $gates; return }
  if (Test-Cmd 'rsvg-convert') { Add-Result 'inkscape' 'ready' 'rsvg-convert present (SVG renderer)' $gates; return }
  if ($Probe) { Add-Result 'inkscape' 'absent' 'no SVG renderer found' $gates; return }

  Write-Host '  installing Inkscape via winget...'
  if ((Invoke-Winget 'Inkscape.Inkscape') -eq 0) {
    Add-Result 'inkscape' 'installed-pending-restart' 'Inkscape installed' $gates $true
  } else {
    Add-Result 'inkscape' 'failed' 'winget failed -- see setup-instructions/visual-render.md' $gates
  }
}

function Setup-LibreOffice {
  $gates = '.vsdx inputs (best-effort, on-demand)'
  if (Test-Cmd 'soffice') { Add-Result 'libreoffice' 'ready' 'soffice resolves' $gates; return }
  if ($Probe) {
    if (Find-Exe 'soffice.exe') { Add-Result 'libreoffice' 'absent' 'installed but soffice not on PATH (re-run without -Probe to shim)' $gates }
    else { Add-Result 'libreoffice' 'absent' 'soffice not found' $gates }
    return
  }

  $exe = Find-Exe 'soffice.exe'
  if (-not $exe) {
    Write-Host '  installing LibreOffice via winget...'
    Invoke-Winget 'TheDocumentFoundation.LibreOffice' | Out-Null
    $exe = Find-Exe 'soffice.exe'
  }
  if (-not $exe) {
    Add-Result 'libreoffice' 'failed' 'soffice.exe not found after install -- see setup-instructions/visual-render.md' $gates; return
  }
  $shim = Set-Shim 'soffice' $exe
  if ($shim.alreadyOnPath -and (Test-Cmd 'soffice')) {
    Add-Result 'libreoffice' 'ready' "shim -> $($shim.shimPath)" $gates
  } else {
    Add-Result 'libreoffice' 'installed-pending-restart' "shim written; added $($shim.shimDir) to user PATH" $gates $true
  }
}

# ---------- dispatch ----------

$plan = if ($Component -eq 'all') {
  @('python', 'markitdown', 'node', 'mmdc', 'drawio', 'playwright')
} elseif ($Component -eq 'core') {
  @('python', 'markitdown', 'node', 'mmdc', 'playwright')   # items 1-6; excludes drawio + on-demand renderers
} else {
  @($Component)
}

Write-Host ''
Write-Host ("requirements-generator environment setup  (component: {0}{1})" -f $Component, $(if ($Probe) { ' / probe' } else { '' }))
Write-Host ('-' * 72)

foreach ($c in $plan) {
  switch ($c) {
    'python'      { Setup-Python }
    'markitdown'  { Setup-Markitdown }
    'node'        { Setup-Node }
    'mmdc'        { Setup-Mmdc }
    'drawio'      { Setup-Drawio }
    'playwright'  { Setup-Playwright }
    'inkscape'    { Setup-Inkscape }
    'libreoffice' { Setup-LibreOffice }
  }
}

Write-Host ('-' * 72)
if ($script:results | Where-Object { $_.restartNeeded }) {
  Write-Host 'NOTE: restart Claude Code so freshly installed/shimmed tools become visible (PATH + MCP are cached at session start), then re-run with -Probe to confirm.'
}
Write-Host ''
Write-Host '===SETUP-ENVIRONMENT-SUMMARY-BEGIN==='
$script:results | ConvertTo-Json -AsArray -Compress -Depth 4
Write-Host '===SETUP-ENVIRONMENT-SUMMARY-END==='
