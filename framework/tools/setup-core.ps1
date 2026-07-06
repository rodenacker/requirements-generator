#requires -Version 7.0
<#
.SYNOPSIS
  One-command consultant bootstrap for the CORE machine dependencies (items 1-6):
  Python, Node.js, markitdown (converters + MCP), mmdc, and the @playwright/mcp npx cache.

.DESCRIPTION
  A thin, canonical-source-respecting wrapper. It contains NO install commands of its own --
  it delegates entirely to `framework/tools/setup-environment.ps1 -Component core` (the single
  home for every dependency install command), then renders a clean consolidated status table
  and the Windows restart / MCP guidance the raw installer cannot infer.

  Scope is deliberately narrow -- exactly the six core dependencies. It does NOT install the
  vector renderers (draw.io / Inkscape / LibreOffice), the /prototype smoke browser, or the
  per-project `template/node_modules` tree. Run the canonical script directly for those:
  `& framework/tools/setup-environment.ps1 -Component all|drawio|inkscape|libreoffice`.

  The two npm dependencies in this set are installed MACHINE-GLOBALLY and are therefore
  available to every future project/clone: mmdc via the global npm prefix (`npm -g`),
  and @playwright/mcp via the global npx (`@playwright/mcp`) cache.

.PARAMETER Probe
  Detect-only. Report status, install nothing. Forwarded verbatim to the canonical installer.

.NOTES
  Windows caches PATH and the MCP tool list at session start, so anything freshly installed
  reports `installed-pending-restart`: it is on disk, but the running Claude Code session
  cannot use it until you restart Claude Code and re-run.
#>
[CmdletBinding()]
param([switch]$Probe)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$installer = Join-Path $PSScriptRoot 'setup-environment.ps1'
if (-not (Test-Path $installer)) {
  Write-Host "ERROR: canonical installer not found at $installer" -ForegroundColor Red
  exit 1
}

Write-Host ''
Write-Host ('=' * 72)
Write-Host (" requirements-generator - core dependency check (items 1-6){0}" -f $(if ($Probe) { '  [probe]' } else { '' }))
Write-Host ('=' * 72)
if (-not $Probe) {
  Write-Host ' Running core setup via setup-environment.ps1 -Component core.'
  Write-Host ' First run may take several minutes (winget / pip / npm downloads)...'
}
Write-Host ''

# Delegate. Merge every stream (*>&1) so the machine-readable summary block is captured, but
# show the installer's live progress lines to the console -- while hiding the raw JSON blob
# between the sentinels (we re-render it ourselves below).
$forward = @{}
if ($Probe) { $forward['Probe'] = $true }

$captured  = [System.Collections.Generic.List[string]]::new()
$inSummary = $false
& $installer -Component core @forward *>&1 | ForEach-Object {
  $line = [string]$_
  $captured.Add($line)
  if     ($line -match 'SETUP-ENVIRONMENT-SUMMARY-BEGIN') { $inSummary = $true }
  elseif ($line -match 'SETUP-ENVIRONMENT-SUMMARY-END')   { $inSummary = $false }
  elseif (-not $inSummary)                                { Write-Host $line }
}
$raw = ($captured -join "`n")

# Extract + parse the summary JSON emitted between the installer's sentinels.
$rows = $null
if ($raw -match '(?s)===SETUP-ENVIRONMENT-SUMMARY-BEGIN===\s*(.+?)\s*===SETUP-ENVIRONMENT-SUMMARY-END===') {
  try { $rows = @($Matches[1].Trim() | ConvertFrom-Json) } catch { $rows = $null }
}
if (-not $rows) {
  Write-Host ''
  Write-Host 'ERROR: could not parse the setup summary. Raw installer output above.' -ForegroundColor Red
  exit 1
}

# Consolidated status table.
$glyph = @{
  'ready'                     = 'OK  [ready]'
  'installed-pending-restart' = '!!  [pending-restart]'
  'failed'                    = 'XX  [FAILED]'
  'absent'                    = '--  [absent]'
  'n/a'                       = 'i   [n/a]'
}
Write-Host ''
Write-Host ('-' * 72)
Write-Host ' Core dependency status'
Write-Host ('-' * 72)
foreach ($r in $rows) {
  $tag = if ($glyph.ContainsKey($r.status)) { $glyph[$r.status] } else { "?   [$($r.status)]" }
  Write-Host ("  {0,-22} {1,-11} {2}" -f $tag, $r.component, $r.detail)
  if ($r.gates) { Write-Host ("  {0,-22} {1,-11}   gates: {2}" -f '', '', $r.gates) }
}
Write-Host ('-' * 72)

# Failed rows -- surface verbatim, never hide behind a green summary.
$failed = @($rows | Where-Object { $_.status -eq 'failed' })
if ($failed.Count -gt 0) {
  Write-Host ''
  Write-Host ' FAILED components (consult the named setup-instructions doc):' -ForegroundColor Red
  foreach ($f in $failed) { Write-Host ("   - {0}: {1}" -f $f.component, $f.detail) -ForegroundColor Red }
}

# Restart guidance -- Windows caches PATH + the MCP tool list at session start.
$pending = @($rows | Where-Object { $_.restartNeeded })
if ($pending.Count -gt 0) {
  Write-Host ''
  Write-Host ' NOTE: restart Claude Code, then re-run `& framework/tools/setup-core.ps1 -Probe`' -ForegroundColor Yellow
  Write-Host '       to confirm. Freshly installed tools (PATH) are not visible to the running'  -ForegroundColor Yellow
  Write-Host '       session until you restart.' -ForegroundColor Yellow
}

# MCP note -- only Claude sees the live tool list; this script cannot.
Write-Host ''
Write-Host ' MCP servers (markitdown, playwright): this script cannot see Claude Code''s live'
Write-Host ' tool list. After a fresh markitdown/playwright install, restart Claude Code so'
Write-Host ' mcp__markitdown__convert_to_markdown and mcp__playwright__browser_navigate become'
Write-Host ' callable. Run /setup inside Claude Code to verify the live MCP tools.'
Write-Host ''

if ($failed.Count -gt 0) { exit 1 } else { exit 0 }
