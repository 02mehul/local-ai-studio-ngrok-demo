import os
import sys
import requests
import json

# Setup
# You can set these env vars or hardcode for testing
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Please set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY env vars.")
    print("Example PowerShell: $env:VITE_SUPABASE_URL='...'; python scripts/verify_supabase.py")
    sys.exit(1)

BASE_URL = f"{SUPABASE_URL.rstrip('/')}/rest/v1/todos"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def run_verification():
    print(f"Verifying against: {BASE_URL}")

    # 1. CREATE
    print("\n[1] Creating Todo...")
    res = requests.post(BASE_URL, json={"title": "Verification Script Item", "done": False}, headers=HEADERS)
    if res.status_code == 201:
        created = res.json()[0]
        print(f"Success: {created}")
        todo_id = created['id']
    else:
        print(f"Failed: {res.text}")
        return

    # 2. READ
    print("\n[2] Reading Todos...")
    res = requests.get(f"{BASE_URL}?select=*", headers=HEADERS)
    if res.status_code == 200:
        todos = res.json()
        print(f"Success. Count: {len(todos)}")
        found = any(t['id'] == todo_id for t in todos)
        print(f"Newly created item found? {found}")
    else:
        print(f"Failed: {res.text}")

    # 3. UPDATE
    print("\n[3] Updating Todo (Done=True)...")
    res = requests.patch(f"{BASE_URL}?id=eq.{todo_id}", json={"done": True}, headers=HEADERS)
    if res.status_code == 200:
        updated = res.json()[0]
        print(f"Success: {updated}")
    else:
        print(f"Failed: {res.text}")

    # 4. DELETE
    print("\n[4] Deleting Todo...")
    res = requests.delete(f"{BASE_URL}?id=eq.{todo_id}", headers=HEADERS)
    if res.status_code == 204 or res.status_code == 200:
        print("Success (Deleted)")
    else:
        print(f"Failed: {res.text}")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"Error: {e}")
