import requests
import sys
from patch_supabase_openapi import patch_openapi

def main():
    try:
        print("Fetching Ngrok URL...")
        response = requests.get("http://localhost:4040/api/tunnels")
        response.raise_for_status()
        data = response.json()
        public_url = data["tunnels"][0]["public_url"]
        print(f"Found Ngrok URL: {public_url}")
        
        patch_openapi(
            input_url="http://localhost:8000/openapi.json",
            output_file="supabase_openapi_ngrok.json",
            server_url=public_url
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
