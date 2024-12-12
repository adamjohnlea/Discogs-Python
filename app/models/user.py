from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model for authentication and Discogs integration"""
    
    __tablename__ = 'users'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication fields
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Discogs integration fields
    discogs_username = db.Column(db.String(80), unique=True, nullable=True)
    discogs_consumer_key = db.Column(db.String(128), nullable=True)
    discogs_consumer_secret = db.Column(db.String(128), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)

    @property
    def is_discogs_connected(self):
        """Check if user has connected their Discogs account"""
        return bool(self.discogs_username and 
                   self.discogs_consumer_key and 
                   self.discogs_consumer_secret) 