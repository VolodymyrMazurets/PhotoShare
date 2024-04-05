# PhotoShare Awesome App

## Local Development

* Start the local development with Docker Compose:

```bash
docker compose --file 'docker-compose.development.yml' up -d
```

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost/8000/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs

Adminer, database web administration: http://localhost:8080

Frontend app: http://localhost:3000

* After changes on dependencies files you need to stop docker and rebuild containers:

```bash
docker compose --file 'docker-compose.development.yml' up --build -d
```
