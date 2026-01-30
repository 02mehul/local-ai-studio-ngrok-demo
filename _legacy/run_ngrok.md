# Exposing Localhost via Ngrok

To let Google AI Studio access your local API, you need a public URL.

## 1. Install Ngrok
If you haven't installed it:
- **Windows**: `winget install ngrok` or download from [ngrok.com](https://ngrok.com/download)
- **Mac**: `brew install ngrok/ngrok/ngrok`

## 2. Start the Tunnel
Run this in a new terminal window:
```bash
ngrok http 8000
```

## 3. Get the URL
Look for line that says `Forwarding`.
Example: `https://abcd-123-456.ngrok-free.app` -> `http://localhost:8000`

**Copy the HTTPS URL.** You will need it for the next step.

> **Note**: Free ngrok URLs change every time you restart ngrok. If you have a paid account, you can use reserved domains: `ngrok http 8000 --domain=my-domain.ngrok-free.app`
