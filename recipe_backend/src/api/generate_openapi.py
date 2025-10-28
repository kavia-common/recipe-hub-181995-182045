import json
import os
import sys

# Ensure module resolution works if executed from the container root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.api.main import app  # noqa: E402

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file within the container root interfaces directory
output_dir = os.path.join(PROJECT_ROOT, "..", "interfaces")
output_dir = os.path.abspath(output_dir)
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2, sort_keys=False)
