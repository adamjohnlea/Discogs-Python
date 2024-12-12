Record Collection App - Project Documentation

PROJECT OVERVIEW
A Flask-based vinyl record collection app using HTMX for interactivity and SQLite for data storage. Built with learning and teaching in mind.

TECHNOLOGY STACK
Backend: Flask (Python web framework)
- Chosen for simplicity and explicit patterns
- Perfect for learning web development concepts

Frontend: HTMX + Tailwind CSS
- Minimal JavaScript approach
- Dynamic features through HTMX
- Clean, responsive styling with Tailwind

Database: SQLite + SQLAlchemy
- Self-contained, perfect for learning
- Robust ORM for database operations

PROJECT STRUCTURE
app/
├── models/              # Database models
│   ├── user.py         # User authentication
│   ├── record.py       # Vinyl record data
│   └── collection.py   # User collections
├── routes/             # HTTP endpoints
│   ├── auth.py        # Authentication routes
│   └── collection.py  # Collection management
├── services/          # Business logic
│   ├── discogs.py    # Discogs API integration
│   └── collection.py # Collection operations
├── templates/
│   ├── base/         # Base templates
│   ├── partials/     # HTMX partial templates
│   └── pages/        # Full page templates
└── static/
    ├── css/          # Stylesheets
    └── js/           # Minimal JS for HTMX

CODING PATTERNS

Route Pattern:
@app.route('/path', methods=['GET'])
def handler():
    # 1. Get data from request
    # 2. Validate input
    # 3. Call service if complex
    # 4. Return template response

Model Pattern:
class ModelName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

Service Pattern:
class ServiceName:
    @staticmethod
    def method_name(params):
        """
        Docstring explaining purpose
        """
        # Complex business logic here

Template Pattern:
{% extends "base/layout.html" %}
{% block content %}
    <div hx-target="this" hx-swap="outerHTML">
        <!-- Content here -->
    </div>
{% endblock %}

LEARNING PROGRESSION

Stage 1: Basics
- Focus:
  - Basic routes and views
  - Simple database operations
  - Template fundamentals
- Key Concepts:
  - HTTP methods
  - URL patterns
  - Basic CRUD operations

Stage 2: Intermediate
- Focus:
  - Service layer implementation
  - Complex database queries
  - HTMX interactions
- Key Concepts:
  - Code organization
  - Database relationships
  - Dynamic updates

Stage 3: Advanced
- Focus:
  - Discogs API integration
  - Performance optimization
  - Advanced patterns
- Key Concepts:
  - Caching strategies
  - Background tasks
  - Complex features

DEVELOPMENT GUIDELINES

When Adding New Features:
1. Start with the model if data storage is needed
2. Create/update service methods for business logic
3. Add routes to handle HTTP requests
4. Create/update templates for display

When Fixing Bugs:
1. Identify the layer where the bug exists
2. Check for similar patterns in working code
3. Write tests to prevent regression
4. Document the fix and why it works

When Improving Code:
1. Explain why the improvement helps
2. Show the current vs. improved approach
3. Document any new patterns introduced

USING WITH AI TOOLS

Effective Prompting:
When asking for help, include:
1. Your current learning stage
2. The specific feature/problem
3. Relevant code context
4. What you've tried

Example:
"As a beginner working on the record collection app, I'm trying to add a feature 
that lets users rate records. I've created the model but don't know how to 
connect it to the routes. Here's my current model code: [code]"