# FastAPI Server

## Prerequisites

Before you start, make sure you have:

- **Python 3.8 or higher** installed on your computer
  - Check by running: `python --version` in your terminal/command prompt
- **pip** (Python package installer)
  - Usually comes with Python
  - Check by running: 
  ```bash
  `pip --version`
  ```
- **Clone from git**
  ```bash
  "git clone https://github.com/ramsandspace-glitch/fast_api_v2.git"
  ```
- **Virtual Environment**
  - create a virtual environment to avoid messup with modules and package version for multiple projects
  - run "python -m venv <name of your virtual env preferably an easy name like ve or venv>"
  - start ve by "<name of your ve>\Scripts\activate", this starts a virtual environment in your machine
  - install the required modules and packages with 
  ```bash
  "pip install -r requirements.txt" 
  ```
- **start server**
  ```bash
  "uvicorn main:app --reload"
  ```
  - this starts the fast api server at default url - http://127.0.0.1:8000
  - to test the api with swagger UI follow this url - http://127.0.0.1:8000/docs
  
## API Endpoints

### Simple Status Endpoints

These endpoints just return status codes for testing:

- **GET /** - Root endpoint (returns 200)
- **POST /200-only-post-method** - Test POST (returns 201)
- **GET /200-only-get-method/{id}** - Test GET with ID (returns 200)
- **PUT /200-only-put-method/{id}** - Test PUT with ID (returns 200)
- **DELETE /200-only-delete-method/{id}** - Test DELETE with ID (returns 204)
