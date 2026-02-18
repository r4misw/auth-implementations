# For Heroku/Platform-as-a-Service deployment

# Flask HTTP Basic Auth (port 5000)
web: cd projects/flask_http_basic_auth && gunicorn flask_http_basic:app --bind 0.0.0.0:$PORT

# Flask JWT Auth (port 5001)
# web: cd projects/flask_jwt_auth && gunicorn flask_jwt:app --bind 0.0.0.0:$PORT

# FastAPI OAuth 2.0 (recommended for production)
# web: cd fastapi_learning/advanced && uvicorn fastapi_oauth:app --host 0.0.0.0 --port $PORT
