# Start Backend
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "app.main:app --reload --port 8000"

# Start Ngrok
Start-Process -NoNewWindow -FilePath "ngrok" -ArgumentList "http 8000"

# Wait a moment for Ngrok to start
Start-Sleep -Seconds 3

# Display Ngrok URL
$tunnels = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels"
Write-Host "Ngrok URL: $($tunnels.tunnels[0].public_url)"
Write-Host "Backend: http://localhost:8000"
