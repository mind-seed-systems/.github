[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')]
    [string] $Repository,

    [Parameter(Mandatory)]
    [ValidateSet('core', 'infrastructure', 'platform')]
    [string] $Profile,

    [switch] $PruneGitHubDefaults
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (Test-Path variable:PSNativeCommandUseErrorActionPreference) {
    $PSNativeCommandUseErrorActionPreference = $true
}

function Invoke-GitHubCli {
    param([Parameter(Mandatory)][string[]] $Arguments)

    $output = & gh @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "gh $($Arguments -join ' ') failed: $($output -join [Environment]::NewLine)"
    }
    return $output
}

$null = Invoke-GitHubCli -Arguments @('auth', 'status')

$configPath = Join-Path (Split-Path -Parent $PSScriptRoot) 'config/labels.json'
$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json -Depth 20
if ($config.schemaVersion -ne 'mind-seed.labels/v1') {
    throw "Unsupported label configuration version: $($config.schemaVersion)"
}

$desired = @($config.labels | Where-Object { $_.profiles -contains $Profile })
$currentJson = (Invoke-GitHubCli -Arguments @(
    'api',
    "repos/$Repository/labels?per_page=100"
)) -join [Environment]::NewLine
$current = @($currentJson | ConvertFrom-Json -Depth 20)

$currentByName = [Collections.Generic.Dictionary[string, object]]::new(
    [StringComparer]::OrdinalIgnoreCase
)
foreach ($label in $current) {
    $currentByName[$label.name] = $label
}

$created = 0
$updated = 0
$unchanged = 0
$removed = 0

foreach ($label in $desired) {
    $name = [string] $label.name
    $color = ([string] $label.color).ToUpperInvariant()
    $description = [string] $label.description

    if (-not $currentByName.ContainsKey($name)) {
        if ($PSCmdlet.ShouldProcess("$Repository label '$name'", 'create')) {
            $null = Invoke-GitHubCli -Arguments @(
                'api', '--method', 'POST', "repos/$Repository/labels",
                '--raw-field', "name=$name",
                '--raw-field', "color=$color",
                '--raw-field', "description=$description"
            )
            $created++
        }
        continue
    }

    $existing = $currentByName[$name]
    $needsUpdate =
        ([string] $existing.color).ToUpperInvariant() -ne $color -or
        [string] $existing.description -ne $description -or
        [string] $existing.name -cne $name

    if (-not $needsUpdate) {
        $unchanged++
        continue
    }

    if ($PSCmdlet.ShouldProcess("$Repository label '$name'", 'update')) {
        $encodedName = [Uri]::EscapeDataString([string] $existing.name)
        $null = Invoke-GitHubCli -Arguments @(
            'api', '--method', 'PATCH', "repos/$Repository/labels/$encodedName",
            '--raw-field', "new_name=$name",
            '--raw-field', "color=$color",
            '--raw-field', "description=$description"
        )
        $updated++
    }
}

if ($PruneGitHubDefaults) {
    $desiredNames = [Collections.Generic.HashSet[string]]::new(
        [StringComparer]::OrdinalIgnoreCase
    )
    foreach ($label in $desired) {
        $null = $desiredNames.Add([string] $label.name)
    }

    foreach ($defaultName in $config.githubDefaultsToRemove) {
        $name = [string] $defaultName
        if (-not $currentByName.ContainsKey($name) -or $desiredNames.Contains($name)) {
            continue
        }
        if ($PSCmdlet.ShouldProcess("$Repository label '$name'", 'delete known GitHub default')) {
            $encodedName = [Uri]::EscapeDataString($name)
            $null = Invoke-GitHubCli -Arguments @(
                'api', '--method', 'DELETE', "repos/$Repository/labels/$encodedName"
            )
            $removed++
        }
    }
}

[ordered]@{
    repository = $Repository
    profile = $Profile
    desired = $desired.Count
    created = $created
    updated = $updated
    unchanged = $unchanged
    removedKnownDefaults = $removed
    unknownLabelsPreserved = $true
} | ConvertTo-Json
