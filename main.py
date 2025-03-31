from fuego import (Fuego, FuegoRequest, FuegoResponse, detect_server_type,
                   fuego_logging_middleware)

app = Fuego()
app.register_middleware(fuego_logging_middleware)


@app.route("/home", "GET")
def home(request: FuegoRequest, response: FuegoResponse):
    # Check if running in WSGI or ASGI
    server_type = detect_server_type(request)
    response.set_header("X-Server-Type", server_type)

    response.set_body(f"Hello from the HOME page ({server_type})")


@app.route("/about/{me}", "GET")
def about(request: FuegoRequest, response: FuegoResponse, me: str):
    response.json(
        data={"message": f"Hello from the ABOUT page, {me}"},
        status=200,
    )


wsgi_app = app.get_wsgi_app()
asgi_app = app.get_asgi_app()
