# A Super Nice Backend Application

## Overview

This FastAPI-based backend application is designed for processing geospatial data, specifically handling building limit polygons and height plateaus. It allows users to split building limits based on specified height criteria, offering an efficient way to manage geospatial information.

## Prerequisites

- **Python**: Version 3.12.0
- **Operating System**: This application has been tested on Windows 11 only.

## Getting Started

### Setup Instructions (Only tested on Windows 11)

1. **Set Local Python Version**   
   `pyenv local 3.12.0`
2. **Set up virtual environment**   
   `pyenv exec python -m venv .venv`
3. **Activate the virtual environment**   
   `.venv\Scripts\activate` (to deactivate: `deactivate`)
4. **Install all python reqirements**   
   `pip install -r requirements.txt`
5. **Run program**   
   `python -m app.main`
5. **Run program**   
   `python -m app.main`

## OpenApi:
Once the application is running, you can access the interactive API documentation at (with default port and host): [Swagger UI](http://127.0.0.1:8000/docs)

## Testing:

Tests are found under `/tests` and have the same file structure as `/app`. \
The tests under `/tests/routers` tests the entire api with an in-memory database.\
The tests under `/tests/services` are more traditional unit tests.

1. **To run all tests**   
   `pytest`

## Technologies Used

- **FastAPI**: A modern web framework for building APIs quickly and efficiently.
- **Uvicorn**: A fast ASGI server to run the FastAPI application.
- **Pydantic**: For data validation and settings management using Python type hints.
- **GeoPandas**: Simplifies geospatial data manipulation and analysis.
- **SQLAlchemy**: An ORM for database interaction.
- **Testing Libraries**: Includes `pytest` for testing and `httpx` for making HTTP requests in tests.
- **Matplotlib**: For creating static visualizations. Used to understand the datastructure

## Datamodel

The datamodel is quiet simpel and we store relevant data and their relationship.

## Deploy
