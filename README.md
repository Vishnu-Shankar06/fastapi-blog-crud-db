# 🚀 FastAPI Full-Stack Blog Application

A complete, dual-interface blog application built to explore and master **FastAPI**. This project serves both a traditional server-side rendered web interface (using HTML templates) and a modern RESTful API, all backed by a SQLite database via SQLAlchemy.

## ✨ Features

* **Dual Interface:** Fully functional Web UI (HTML forms/templates) and a structured JSON API.
* **Full CRUD Functionality:** Create, Read, Update, and Delete blog posts through the browser or via API endpoints.
* **Data Validation:** * Backend validation using **Pydantic** models for the API.
  * Custom form validation for the web templates (checking string length and empty fields).
* **Database Integration:** Utilizes **SQLAlchemy** ORM with a local SQLite database (`.blog.db`).
* **Custom Error Handling:** Beautiful template-rendered error pages for 404 (Not Found) and custom validation exception handlers for API requests (422 Unprocessable Entity).

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **Language:** Python
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Data Validation:** Pydantic
* **Templating:** Jinja2
* **Server:** Uvicorn

## 📂 Project Structure

    ├── main.py          # Core application, routing, and error handling
    ├── database.py      # SQLite engine and SQLAlchemy session configuration
    ├── models.py        # SQLAlchemy database models (Table schemas)
    ├── schemas.py       # Pydantic models for API request/response validation
    ├── templates/       # Jinja2 HTML templates for the Web UI
    │   ├── home.html    # Displays all blog posts
    │   ├── post.html    # Displays a single post
    │   ├── create.html  # Form to create a new post
    │   ├── edit.html    # Form to edit an existing post
    │   └── error.html   # Custom error display page
    └── .blog.db         # Auto-generated SQLite database

## 🚀 Installation & Setup

Follow these steps to run the application on your local machine.

**1. Clone the repository**
    git clone https://github.com/Vishnu-Shankar06/fastapi-blog-crud-db.git
    cd fastapi-blog-crud-db

**2. Create and activate a virtual environment**
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

**3. Install dependencies**
Make sure you have the required packages installed:
    pip install fastapi 

**4. Run the development server**
    fastapi dev main.py

The application will be available at: `http://127.0.0.1:8000`

---

## 💻 Sample Output & Usage

### 🌐 Web Interface

Navigate to `http://127.0.0.1:8000/` in your browser. 
* **Home Page (`/`)**: You will see a list of all your posts.
* **Create Post (`/create`)**: Submitting an empty form or a title with less than 3 characters will trigger the custom validation, re-rendering the page with error messages.
* **View/Edit Post (`/post/{id}`)**: Click on a post to read it, edit its contents, or delete it entirely.

### 🔌 REST API Endpoints

FastAPI automatically generates interactive API documentation. You can view and test all endpoints by visiting:
* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

#### API Reference Table

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/posts` | Retrieve a list of all posts |
| `GET` | `/api/posts/{post_id}` | Retrieve a specific post by ID |
| `POST` | `/api/posts` | Create a new post |
| `PUT` | `/api/posts/{post_id}` | Fully update a post |
| `PATCH`| `/api/posts/{post_id}` | Partially update a post |
| `DELETE`| `/api/posts/{post_id}` | Delete a post |

#### Example API Requests

**Create a new post (POST `/api/posts`)**
    // Request Body
    {
      "title": "Learning FastAPI",
      "content": "Building APIs with Python has never been faster!"
    }

    // Response (200 OK)
    {
      "title": "Learning FastAPI",
      "content": "Building APIs with Python has never been faster!",
      "id": 1
    }

**Validation Error Example (POST `/api/posts`)**
If you send a title that is too short:
    // Request Body
    {
      "title": "Hi",
      "content": "This content is long enough."
    }

    // Response (422 Unprocessable Entity)
    {
      "detail": [
        {
          "loc": ["body", "title"],
          "msg": "ensure this value has at least 3 characters",
          "type": "value_error.any_str.min_length",
          "ctx": {"limit_value": 3}
        }
      ]
    }

## 🧠 What I Learned

Building this project provided hands-on experience with:
1.  **FastAPI Routing:** Handling both API routes and HTML template rendering in the same application.
2.  **Dependency Injection:** Using `Depends(get_db)` to safely open and close database sessions per request.
3.  **Data Validation:** Leveraging Pydantic for strict API schemas and writing custom logic for HTML forms.
4.  **SQLAlchemy ORM:** Mapping Python classes to database tables and executing CRUD operations without writing raw SQL.
5.  **Exception Handling:** Overriding standard error handlers to serve custom HTML pages for user-facing errors while preserving JSON errors for API clients.
