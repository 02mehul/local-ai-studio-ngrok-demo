import json
import sys
import subprocess
import time
import urllib.request

output_spec = "openapi_patched.json"
local_spec = "openapi_local.json"
api_url = "http://127.0.0.1:4040/api/tunnels"

print("Querying ngrok API...")
url = None

for i in range(10):
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            tunnels = data.get('tunnels', [])
            if tunnels:
                url = tunnels[0].get('public_url')
                if url:
                    break
    except Exception as e:
        print(f"Retrying... {e}")
    time.sleep(1)

if url:
    print(f"Found URL: {url}")
    # Call patch script
    subprocess.run([sys.executable, "scripts/patch_openapi_servers.py", local_spec, output_spec, "--server-url", url])
else:
    print("Could not find public URL from ngrok API.")
