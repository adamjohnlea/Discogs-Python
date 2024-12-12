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
