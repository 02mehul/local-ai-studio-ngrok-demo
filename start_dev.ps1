
Write-Host "Starting Web Server..."
Start-Process python -ArgumentList "-m http.server 8000 --directory web" -WindowStyle Minimized

Write-Host "Starting ngrok for AI Studio..."
Start-Process ngrok -ArgumentList "http 54321" -WindowStyle Minimized

Write-Host "Starting Migration Watcher..."
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File scripts/watch_migrations.ps1" -WindowStyle Minimized

Write-Host "Starting Local Supabase Stack (Docker)..."
npx supabase start

Write-Host "Configuring App with Local Keys..."
node scripts/auto_config.js

Write-Host "---------------------------------------------------"
Write-Host "✅ Stack Started!"
Write-Host "---------------------------------------------------"
Write-Host "Web UI:    http://localhost:8000"
Write-Host "Supabase:  http://127.0.0.1:54323 (Studio)"
Write-Host "API:       http://127.0.0.1:54321"
Write-Host "Ngrok:     http://localhost:4040 (Check public URL here)"
Write-Host "---------------------------------------------------"
Write-Host "To stop:   npx supabase stop"
