import json
import os

from src.api.main import app

# Utility script to regenerate the OpenAPI spec for this service.
# You can re-run this script after modifying routes or models to refresh interfaces/openapi.json.
# No environment variables are required.

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file
output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
