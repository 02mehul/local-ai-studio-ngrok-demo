# scripts/watch_migrations.ps1
# Watches supabase/migrations for NEW .sql files and restarts Supabase when one appears.

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$migrationsPath = Join-Path $repoRoot "supabase\migrations"

if (!(Test-Path $migrationsPath)) {
    Write-Host "❌ Migrations folder not found at: $migrationsPath"
    exit 1
}

Write-Host "👀 Watching for new migrations in: $migrationsPath"
Write-Host "   When a NEW .sql file appears, Supabase will restart to apply migrations."

# Track known migration filenames
$known = @{}
Get-ChildItem $migrationsPath -Filter *.sql | ForEach-Object { $known[$_.Name] = $true }

while ($true) {
    Start-Sleep -Seconds 2

    $current = Get-ChildItem $migrationsPath -Filter *.sql
    foreach ($f in $current) {
        if (-not $known.ContainsKey($f.Name)) {
            $known[$f.Name] = $true

            Write-Host ""
            Write-Host "✅ New migration detected: $($f.Name)"
            Write-Host "🔄 Restarting Supabase to apply migrations..."

            # Restart Supabase (local dev)
            # If you use Supabase CLI:
            npx supabase stop | Out-Null
            npx supabase start | Out-Null

            Write-Host "✅ Supabase restarted. Migration should now be applied."
            Write-Host "   Check Supabase Studio: http://127.0.0.1:54323"
            Write-Host ""
        }
    }
}
