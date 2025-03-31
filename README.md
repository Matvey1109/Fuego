# 🔥 Fuego: A Simple Python Web Framework

**Fuego** is a lightweight, micro web framework designed for Python, supporting both **WSGI** and **ASGI** for synchronous and asynchronous applications. It's simple, flexible, and perfect for small-scale applications or APIs. The framework works seamlessly with **Gunicorn** or **Uvicorn** for serving your application and **Nginx** for handling reverse proxying in production.

## Features

- **Minimalistic**: Easy to use with a small footprint.
- **WSGI & ASGI support**: Handle both synchronous and asynchronous applications.
- **Integration with Gunicorn and Uvicorn**: Efficiently manage multiple worker processes.
- **Works well with Nginx**: Easily deploy with a reverse proxy.

## Project Structure

- **Fuego**: The core framework that handles routing and request/response.
- **Gunicorn/Uvicorn**: The application server that runs your app.
- **Nginx**: The reverse proxy for handling requests from clients.

---

## Set up enviroment

```bash
uv --version
uv init
uv venv
source .venv/bin/activate

uv add gunicorn uvicorn
uv pip list
```

```bash
uv run main.py
gunicorn main:wsgi_app
unicorn main:asgi_app
```

## How It Works

### Gunicorn/Uvicorn + Nginx Workflow:

1. **User** sends an HTTP request to **Nginx**.
2. **Nginx** forwards the request to **Gunicorn** (WSGI) or **Uvicorn** (ASGI) running the **Fuego** application.
3. **Gunicorn/Uvicorn** processes the request and passes it to the **Fuego** application.
4. **Fuego** returns the response to **Gunicorn/Uvicorn**, which forwards it back to **Nginx**.
5. **Nginx** sends the response back to the user.

---

## Diagram

The following table shows how **Fuego**, **Gunicorn/Uvicorn**, and **Nginx** interact:

| **Step** | **Component** | **Action**                                               |
| -------- | ------------- | -------------------------------------------------------- |
| 1        | Client        | Sends an HTTP request to **Nginx**                       |
| 2        | Nginx         | Forwards the request to **Gunicorn/Uvicorn**             |
| 3        | Gunicorn/Uvicorn      | Processes the request and passes it to the **Fuego** app |
| 4        | Fuego         | Returns the response to **Gunicorn/Uvicorn**                     |
| 5        | Gunicorn/Uvicorn      | Forwards the response to **Nginx**                       |
| 6        | Nginx         | Sends the response back to the **Client**                |

---

## Deployment with Nginx and Load Balancing

To improve scalability and performance, **Nginx** can be used as a reverse proxy and load balancer for multiple instances of **Fuego**. This setup ensures that requests are distributed efficiently among backend servers.

---

## Conclusion

With **Fuego**, **Gunicorn/Uvicorn**, and **Nginx**, you have a robust and scalable stack for building and deploying Python web applications. **Gunicorn/Uvicorn** ensures efficient request handling with multiple worker processes, while **Nginx** serves as a reverse proxy to handle incoming requests and distribute them efficiently to **Gunicorn/Uvicorn**. This setup is ideal for both development and production environments, providing performance and scalability with minimal complexity.

By using **Fuego**, you can focus on building your application logic without worrying about complex configurations. Whether you're building a small API or a larger web service, **Fuego** with **Gunicorn/Uvicorn** and **Nginx** will handle your application's needs efficiently.
