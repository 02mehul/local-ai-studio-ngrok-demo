# scripts/watch_migrations.ps1
# Watches lovable/todo-sanctuary/db/migrations for NEW .sql files.
# Copies them to supabase/migrations and restarts Supabase.

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$lovableMigrations = Join-Path $repoRoot "lovable\todo-sanctuary\db\migrations"
$supabaseMigrations = Join-Path $repoRoot "supabase\migrations"

# Ensure directories exist
if (!(Test-Path $lovableMigrations)) {
    Write-Host "⚠️  Lovable migrations folder not found at: $lovableMigrations"
    Write-Host "   Waiting for it to be created..."
}
if (!(Test-Path $supabaseMigrations)) {
    Write-Host "❌ Supabase migrations folder not found at: $supabaseMigrations"
    exit 1
}

Write-Host "👀 Watching for new migrations in: $lovableMigrations"
Write-Host "   Target: $supabaseMigrations"

# Track known files in Lovable folder
$known = @{}
if (Test-Path $lovableMigrations) {
    Get-ChildItem $lovableMigrations -Filter *.sql | ForEach-Object { $known[$_.Name] = $true }
}

while ($true) {
    Start-Sleep -Seconds 2

    if (Test-Path $lovableMigrations) {
        $current = Get-ChildItem $lovableMigrations -Filter *.sql
        foreach ($f in $current) {
            if (-not $known.ContainsKey($f.Name)) {
                $known[$f.Name] = $true

                Write-Host ""
                Write-Host "✅ New Lovable migration detected: $($f.Name)"
                
                # Copy file
                $dest = Join-Path $supabaseMigrations $f.Name
                Copy-Item -Path $f.FullName -Destination $dest -Force
                Write-Host "✅ Copied to supabase/migrations"
                
                # Trigger UI Scaffolding
                Write-Host "🎨 Scaffolding UI for new migration..."
                node "$repoRoot/scripts/scaffold_ui.js" "$($f.FullName)"
                
                # Apply migration SQL directly via Docker (no restart needed)
                Write-Host "🔄 Applying migration SQL directly..."
                $sql = Get-Content $f.FullName -Raw
                try {
                    docker exec -i supabase_db_local-ai-studio-ngrok-demo psql -U postgres -c $sql
                    Write-Host "✅ Migration applied successfully!"
                } catch {
                    Write-Host "⚠️  Direct apply failed: $_"
                    Write-Host "   Try restarting Supabase manually."
                }

                Write-Host "✅ Supabase restarted. Migration applied."
                Write-Host "   Check Supabase Studio: http://127.0.0.1:54323"
                Write-Host ""
            }
        }
    }
}
