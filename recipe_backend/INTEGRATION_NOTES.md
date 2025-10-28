# Integration Notes

- CORS:
  - By default allows http://localhost:3000.
  - Override via BACKEND_CORS_ORIGINS env var (comma-separated), e.g.:
    BACKEND_CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

- Regenerate OpenAPI:
  - From container root `recipe_backend/` run:
    python -m src.api.generate_openapi
  - The schema writes to `recipe_backend/interfaces/openapi.json`.

- Frontend:
  - Set REACT_APP_API_BASE in `recipe_frontend/.env`:
    REACT_APP_API_BASE=http://localhost:3001
