Write-Host "Stopping Local Development Environment..."

# 1. Stop Supabase Safely (Preserves Data)
Write-Host "Stopping Supabase Containers..."
npx supabase stop

# 2. Stop Background Services
Write-Host "Stopping Web Server and Ngrok..."
Stop-Process -Name "python" -ErrorAction SilentlyContinue
Stop-Process -Name "ngrok" -ErrorAction SilentlyContinue
Stop-Process -Name "node" -ErrorAction SilentlyContinue
# Stop the specific PowerShell migration watcher
Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -like "*watch_migrations.ps1*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -ErrorAction SilentlyContinue }

Write-Host "---------------------------------------------------"
Write-Host "✅ Environment Stopped Safely."
Write-Host "   Your data is preserved in Docker volumes."
Write-Host "   Run .\start_dev.ps1 to restart."
Write-Host "---------------------------------------------------"
