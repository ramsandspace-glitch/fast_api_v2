# FastAPI Server
## Prerequisites

Before you start, make sure you have:
- **Python 3.8 or higher** installed on your computer
  - Check by running: `python --version` in your terminal/command prompt
- **pip** (Python package installer)
  - Usually comes with Python
  - Check by running:
  ```bash
  pip --version
  ```
- **Clone from git**
  ```bash
  git clone https://github.com/ramsandspace-glitch/fast_api_v2.git
  ```
- **Virtual Environment**
  - Create a virtual environment to avoid messup with modules and package version for multiple projects
  - Run `python -m venv venv`
  - Start venv by `venv\Scripts\activate`
  - Install the required modules and packages with
  ```bash
  pip install -r requirements.txt
  ```
- **Start server**
  ```bash
  uvicorn main:app --reload
  ```
  - This starts the fast api server at default url - http://127.0.0.1:8000
  - To test the api with swagger UI follow this url - http://127.0.0.1:8000/docs

## API Endpoints

### User Endpoints

- **GET /** - Root endpoint (returns 200)

- **POST /register** - Register a new user
  - Body: `username` (string), `password` (string), `mobile` (int, 10 digits)
  - Returns: User details with id

- **POST /login** - Login user
  - Body: `username` (string), `password` (string)
  - Returns: User details and success message

- **GET /users** - Get all users
  - Returns: List of all users with count

- **GET /users/{id}** - Get single user by ID
  - Returns: User details

- **PUT /users/{id}** - Update user details
  - Body: `username` (optional string), `password` (optional string), `mobile` (optional int, 10 digits)
  - Returns: Updated user details

- **DELETE /users/{id}** - Delete user by ID
  - Returns: Success message with deleted user ID
