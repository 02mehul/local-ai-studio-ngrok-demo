import json
import os
import sys

# Load env vars manually or assume they are set in environment
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL")

if not SUPABASE_URL:
    print("VITE_SUPABASE_URL not set. Defaulting to Local Supabase (Docker): http://127.0.0.1:54321")
    SUPABASE_URL = "http://127.0.0.1:54321"

# Ensure URL does not have trailing slash for consistency
SUPABASE_URL = SUPABASE_URL.rstrip("/")

PRODUCED_OPENAPI_FILE = "supabase_openapi_real.json"
PRODUCED_OPENAPI_TXT = "supabase_openapi_real.txt"

def patch_openapi():
    # Read the local openapi.json (base spec) - assuming it exists from previous steps
    # If not, we might need to use a template or fetch it. 
    # For now, let's assume we are patching 'openapi_local.json' or similar if present, 
    # OR we are constructing a minimal one if we are replacing the Python backend entirely.
    
    # Actually, the user wants to point OpenAPI at Supabase PostgREST.
    # Supabase PostgREST OpenAPI is usually available at /rest/v1/?apikey=...
    # But here we probably want to patch the ONE we have locally to just point to Supabase.
    
    input_file = "openapi_local.json"
    if not os.path.exists(input_file):
        # Fallback to creating a basic one if local one isn't found
        print(f"Warning: {input_file} not found. Using minimal template.")
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Supabase Todo API",
                "version": "1.0.0"
            },
            "servers": [
                {"url": f"{SUPABASE_URL}/rest/v1"}
            ],
            "paths": {
                "/todos": {
                    "get": {
                        "summary": "Get Todos",
                        "parameters": [{"name": "select", "in": "query", "schema": {"type": "string"}, "example": "*"}],
                        "responses": {"200": {"description": "List of todos"}}
                    },
                    "post": {
                        "summary": "Create Todo",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "title": {"type": "string"},
                                                "done": {"type": "boolean"}
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"201": {"description": "Created"}}
                    }
                }
            }
        }
    else:
        with open(input_file, "r") as f:
            spec = json.load(f)

    # Patch Servers
    # We want to force the server URL to be the real Supabase REST endpoint
    spec["servers"] = [
        {
            "url": f"{SUPABASE_URL}/rest/v1",
            "description": "Supabase API"
        }
    ]

    # Write JSON
    with open(PRODUCED_OPENAPI_FILE, "w") as f:
        json.dump(spec, f, indent=2)
    
    # Write TXT
    with open(PRODUCED_OPENAPI_TXT, "w") as f:
        json.dump(spec, f, indent=2)

    print(f"Generated {PRODUCED_OPENAPI_FILE} and {PRODUCED_OPENAPI_TXT}")
    print(f"Target Server URL: {SUPABASE_URL}/rest/v1")

if __name__ == "__main__":
    patch_openapi()
