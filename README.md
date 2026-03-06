# Backend Service for Image AI Tutorial

This directory contains the backend code and supporting configuration for the Image AI application. It implements the core APIs, business logic, data models, workflows, and infrastructure needed to scan images, generate reports, manage users, and support active learning.

The backend is built using FastAPI and leverages Celery for asynchronous task processing, Redis for caching and message brokering, and a host of internal services organized into a modular structure. It is designed to be run within a Dockerized development environment configured via `docker-compose.yml`.

Refer to the top-level `README.md` for overall project setup, but this file provides backend-specific insights and documentation.
