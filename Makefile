# Variables
PYTHON = python3
GUNICORN = gunicorn
UVICORN = uvicorn
APP_MODULE = main
WSGI_PORT = 1111
ASGI_PORT = 2222

# Run the application in WSGI mode using Gunicorn
run_wsgi:
	@echo "Running application in WSGI mode using Gunicorn..."
	$(GUNICORN) $(APP_MODULE):wsgi_app --bind 0.0.0.0:$(WSGI_PORT)

# Run the application in ASGI mode using Uvicorn
run_asgi:
	@echo "Running application in ASGI mode using Uvicorn..."
	$(UVICORN) $(APP_MODULE):asgi_app --host 0.0.0.0 --port $(ASGI_PORT)

# Help message
help:
	@echo "Makefile commands:"
	@echo "  make run_wsgi     - Run the application using Gunicorn (WSGI mode)"
	@echo "  make run_asgi     - Run the application using Uvicorn (ASGI mode)"
