👕 Shirt Printer API

Django REST + Celery project for generating T-shirt mockups with custom text.
------------------------------------
Features:

    Async task handling with Celery + Redis
    Pillow for text rendering on images
    Dockerized setup (Django, PostgreSQL, Redis)
-------------------------------------
🐳 Run with Docker

    git clone https://github.com/Arian-nmi/ShirtPrinter.git
    cd ShirtPrinter
    docker-compose up --build
------------------------------------
API Endpoints

    POST `/api/mockups/generate/` → create mockups
    GET `/api/mockups/tasks/<task_id>/` → check task status
    GET `/api/mockups/` → list all mockups
