import json
import argparse
import sys
import yaml

def patch_spec(input_path, output_path, server_url):
    print(f"Reading spec from {input_path}...")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        if input_path.endswith('.yaml') or input_path.endswith('.yml'):
            spec = yaml.safe_load(f)
        else:
            spec = json.load(f)

    # OpenAPI 3.x
    if 'openapi' in spec:
        print(f"Detected OpenAPI {spec['openapi']}")
        spec['servers'] = [{'url': server_url, 'description': 'Ngrok public URL'}]
    
    # Swagger 2.0
    elif 'swagger' in spec:
        print(f"Detected Swagger {spec['swagger']}")
        # Remove schemes, host, basePath if present
        # OpenAPI 2.0 (Swagger) creates URL from scheme + host + basePath
        # We can try to convert to minimal structure to force the host
        # But simpler is to parse the URL
        from urllib.parse import urlparse
        parsed = urlparse(server_url)
        spec['host'] = parsed.netloc
        spec['schemes'] = [parsed.scheme]
        # If there is a path in the ngrok url, set basePath (unlikely for root tunnel)
        if parsed.path and parsed.path != '/':
             spec['basePath'] = parsed.path
        else:
             # Keep existing basePath if valid, or default to /
             if 'basePath' not in spec:
                 spec['basePath'] = '/'
    
    else:
        print("Warning: Unknown spec format. Attempting to add servers block anyway.")
        spec['servers'] = [{'url': server_url}]
        
    print(f"Writing patched spec to {output_path} with URL: {server_url}")

    with open(output_path, 'w', encoding='utf-8') as f:
        if output_path.endswith('.yaml') or output_path.endswith('.yml'):
            yaml.dump(spec, f, sort_keys=False)
        else:
            json.dump(spec, f, indent=2)
    
    print("Done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Patch OpenAPI spec server URL')
    parser.add_argument('input', help='Input spec file (json/yaml)')
    parser.add_argument('output', help='Output spec file (json/yaml)')
    parser.add_argument('--server-url', required=True, help='The public ngrok URL')
    
    args = parser.parse_args()
    patch_spec(args.input, args.output, args.server_url)
