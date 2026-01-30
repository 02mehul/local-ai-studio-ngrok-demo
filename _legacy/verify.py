import requests
import sys
import time

def verify():
    try:
        # Get Ngrok URL
        print("Fetching Ngrok URL...")
        tunnels = requests.get("http://localhost:4040/api/tunnels").json()
        public_url = tunnels["tunnels"][0]["public_url"]
        print(f"Ngrok URL: {public_url}")
        
        # Test GET /rest/v1/todos
        target = f"{public_url}/rest/v1/todos"
        print(f"Testing GET {target}...")
        resp = requests.get(target)
        if resp.status_code == 200:
            print("SUCCESS: Endpoint reachable via Ngrok!")
            print(f"Response: {resp.json()}")
        else:
            print(f"FAILURE: Status {resp.status_code}")
            print(resp.text)
            sys.exit(1)
            
        # Test POST
        print("Testing POST...")
        payload = {"title": "Smoke Test Item", "done": False}
        resp = requests.post(target, json=payload)
        if resp.status_code == 201 or resp.status_code == 200:
             print("SUCCESS: Item created!")
             print(resp.json())
        else:
            print(f"FAILURE: Post failed {resp.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify()
