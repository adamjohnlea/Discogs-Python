# Record Collection App

A Flask web application for managing your vinyl record collection with Discogs integration.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd record-collection
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by copying the example .env file:
   ```bash
   cp .env.example .env
   # Edit .env with your specific settings:
   # FLASK_APP=run.py
   # FLASK_ENV=development
   # SECRET_KEY=your-secret-key
   # DATABASE_URL=sqlite:///app.db
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the development server:
   ```bash
   flask run
   ```

The application will be available at `http://127.0.0.1:5000`

## Features

- User authentication (register, login, profile management)
- Discogs integration for accessing your record collection
- Profile management with:
  - Basic information updates (username, email)
  - Password changes
  - Discogs account connection/disconnection

## Technology Stack

- Backend: Flask
- Database: SQLite with SQLAlchemy
- Frontend: HTMX for dynamic updates
- Styling: Tailwind CSS

## Project Structure
app/
├── models/ # Database models
│ └── user.py # User model for authentication
├── routes/ # Route handlers
│ └── auth.py # Authentication routes
├── services/ # Business logic
│ └── auth_service.py # Authentication service
├── static/ # Static files (CSS, JS)
├── templates/ # Jinja2 templates
│ ├── base/ # Base templates
│ ├── pages/ # Full page templates
│ └── partials/ # HTMX partial templates
└── init.py # App initialization
config.py # Application configuration
requirements.txt # Python dependencies
run.py # Application entry point


## Development

- Follow PEP 8 style guide for Python code
- Use meaningful commit messages
- Keep functions focused and documented
- Write tests for new features

## Security Features

- Password hashing with Werkzeug
- CSRF protection
- Rate limiting for login attempts
- Secure session handling
- Input validation and sanitization