import json
import argparse
import requests
import sys

def patch_openapi(input_url, output_file, server_url):
    print(f"Fetching OpenAPI spec from {input_url}...")
    try:
        response = requests.get(input_url)
        response.raise_for_status()
        spec = response.json()
    except Exception as e:
        print(f"Error fetching spec: {e}")
        sys.exit(1)

    # Patch Servers
    print(f"Patching servers to {server_url}...")
    spec["servers"] = [{"url": server_url, "description": "Ngrok Tunnel"}]

    # Filter paths to only include /rest/v1/
    # This ensures AI Studio only sees the Supabase-compatible layer
    supabase_paths = {}
    for path, path_item in spec.get("paths", {}).items():
        if path.startswith("/rest/v1/"):
            supabase_paths[path] = path_item
    
    spec["paths"] = supabase_paths
    
    # We ideally should prune components/schemas that are unused, but it's optional.
    # Leaving them is safer.

    print(f"Saving patched spec to {output_file}...")
    with open(output_file, "w") as f:
        json.dump(spec, f, indent=2)

    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch OpenAPI spec for Supabase/Ngrok")
    parser.add_argument("--server-url", required=True, help="Ngrok Public URL (e.g. https://xxxx.ngrok-free.app)")
    parser.add_argument("--input-url", default="http://localhost:8000/openapi.json", help="Local OpenAPI Endpoint")
    parser.add_argument("--output-file", default="supabase_openapi_ngrok.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    patch_openapi(args.input_url, args.output_file, args.server_url)
