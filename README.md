# fastapi-blog

A simple blog with fast-api.

## Prerequisites
- Python3.7 Environment
- pip3

## Technologies
- Fast-API
- SQLite Database
- Elasticsearch
- Redis
- JWT Authentication

## Installation
You must install python dependencies before running project. To install dependencies use pip3:
```bash
pip install -r requirements.txt
```
**Recommendation:** It is highly recommended that run the project in a python virtual environment.

## Run Project
After install dependencies, use the steps below to run project run project:
1. Update the default JWT secret key: 
You should generate a secret key that jwt use to secure the data. You can use 'openssl' command to generate secret key. Make sure that you updated the secret key in the 'conf/settings.py' file.
<br/>**Warning:** Do not use default secret key for running in production.
2. Database settings: Make sure that the SQLite, Elasticsearch and Redis are ready to use in your system.
3. Run the main program: 
You have 2 choices to run the program:
    - Run program directly using main.py: 
        ```bash
        uvicorn main:app --reload
        ```
    - Run program using manage.py:
        ```bash
        python manage.py runserver -r -p 8000
      ```
        This will run the main app with the --reload option and on the port 8000.
