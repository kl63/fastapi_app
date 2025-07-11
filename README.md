# FastAPI User Management System

A modern RESTful API built with FastAPI, PostgreSQL, and async SQLAlchemy for user management and authentication.

## Features

- ✅ **FastAPI** for high-performance API endpoints with automatic documentation
- ✅ **Async SQLAlchemy** for non-blocking database operations
- ✅ **PostgreSQL** with asyncpg driver for efficient data storage
- ✅ **JWT Authentication** for secure API access
- ✅ **Alembic** for database migrations
- ✅ **Pydantic** for data validation and settings management
- ✅ **Service Layer Pattern** for clean separation of business logic
- ✅ **Comprehensive Error Handling**
- ✅ **CLI Management Tool** for easy administration

## Project Structure

```
fastapi_app/
├── alembic/                    # Database migration configuration and versions
├── app/
│   ├── api/                    # API endpoints
│   │   ├── endpoints/          # API route handlers
│   │   └── api.py              # API router configuration
│   ├── core/                   # Core functionality
│   │   ├── middleware/         # Middleware components
│   │   ├── config.py           # Application configuration
│   │   ├── deps.py             # Dependency injection
│   │   └── security.py         # Security utilities (JWT, password hashing)
│   ├── crud/                   # Database CRUD operations
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic schemas for validation
│   ├── services/               # Business logic layer
│   └── database.py             # Database connection and session management
├── migrations/                 # Alembic migrations
├── .env                        # Environment variables
├── main.py                     # Application entry point
├── manage.py                   # CLI management tool
└── requirements.txt            # Project dependencies
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd fastapi_app
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env` file:

```
DB_USER=kevinlin192003
DB_PASS=your_password
DB_HOST=localhost
DB_NAME=fastapi_app
DATABASE_URL=postgresql+asyncpg://kevinlin192003:your_password@localhost/fastapi_app
```

## Database Setup

1. Create a PostgreSQL database:

```bash
createdb fastapi_app
```

2. Run database migrations:

```bash
python manage.py upgrade
```

3. Initialize the database with default data (optional):

```bash
python manage.py init_database
```

## Running the Application

Start the application server with:

```bash
python manage.py run
```

Or directly with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

## API Documentation

Once the application is running, you can access:

- Interactive API documentation: http://127.0.0.1:8000/docs
- Alternative documentation: http://127.0.0.1:8000/redoc
- OpenAPI schema: http://127.0.0.1:8000/api/openapi.json

## API Endpoints

### Authentication

- `POST /api/auth/login` - Login and get access token

### Users

- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user
- `GET /api/users/{user_id}` - Get a specific user by ID

## Database Management

This project uses Alembic for database migrations. The `manage.py` script provides convenient commands:

```bash
# Create a new migration
python manage.py migrate "Add new field to user model"

# Upgrade database to the latest version
python manage.py upgrade

# Downgrade database one revision
python manage.py downgrade

# Show migration history
python manage.py history

# Show current migration revision
python manage.py current
```

## Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Obtain a token by calling the login endpoint
2. Include the token in the Authorization header: `Bearer <your-token>`

## Development

### Creating New Endpoints

1. Create a new file in `app/api/endpoints/`
2. Define your router and endpoints
3. Import and include your router in `app/api/api.py`

### Adding Database Models

1. Define your SQLAlchemy model in `app/models/`
2. Import your model in `app/models/__init__.py`
3. Create Pydantic schemas in `app/schemas/`
4. Create CRUD operations in `app/crud/`
5. Create a migration: `python manage.py migrate "Add new model"`
6. Apply the migration: `python manage.py upgrade`

## Testing

Run tests with:

```bash
pytest
```

## License

This project is licensed under the MIT License.
