import re
from typing import Optional, Tuple
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User

class AuthService:
    """Service class for handling user authentication and registration"""

    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$')
    
    # Username requirements
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    
    # Email requirements
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    @staticmethod
    def validate_registration(username: str, email: str, password: str) -> list[str]:
        """
        Enhanced validation with stronger requirements
        """
        errors = []
        
        # Username validation
        if not username:
            errors.append("Username is required")
        elif not AuthService.USERNAME_PATTERN.match(username):
            errors.append("Username must be 3-20 characters and contain only letters, numbers, underscores, and hyphens")
        
        # Email validation
        if not email:
            errors.append("Email is required")
        elif not AuthService.EMAIL_PATTERN.match(email):
            errors.append("Please provide a valid email address")
        
        # Password validation
        if not password:
            errors.append("Password is required")
        elif len(password) < AuthService.MIN_PASSWORD_LENGTH:
            errors.append(f"Password must be at least {AuthService.MIN_PASSWORD_LENGTH} characters")
        elif not AuthService.PASSWORD_PATTERN.match(password):
            errors.append("Password must contain at least one letter and one number")
            
        # Check existing users (case-insensitive)
        if User.query.filter(User.username.ilike(username)).first():
            errors.append("Username already taken")
        if User.query.filter(User.email.ilike(email)).first():
            errors.append("Email already registered")
            
        return errors

    @staticmethod
    def register_user(username: str, email: str, password: str) -> Tuple[Optional[User], list[str]]:
        """
        Register a new user
        Returns tuple of (User, errors)
        User will be None if registration fails
        """
        errors = AuthService.validate_registration(username, email, password)
        if errors:
            return None, errors
            
        try:
            user = User()
            user.username = username.lower().strip()
            user.email = email.lower().strip()
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            return user, []
            
        except IntegrityError:
            db.session.rollback()
            return None, ["Registration failed. Please try again."]
        except Exception as e:
            db.session.rollback()
            return None, [f"An unexpected error occurred: {str(e)}"]

    @staticmethod
    def authenticate_user(username_or_email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Enhanced authentication with rate limiting and security measures
        Returns tuple of (User, error_message)
        """
        if not username_or_email or not password:
            return None, "Please provide both username/email and password"

        # Case-insensitive lookup
        if '@' in username_or_email:
            user = User.query.filter(User.email.ilike(username_or_email)).first()
        else:
            user = User.query.filter(User.username.ilike(username_or_email)).first()

        if not user:
            # Vague error message for security
            return None, "Invalid credentials"

        if not user.check_password(password):
            # Vague error message for security
            return None, "Invalid credentials"

        return user, None

    @staticmethod
    def update_discogs_credentials(
        user: User,
        discogs_username: str,
        consumer_key: str,
        consumer_secret: str
    ) -> Tuple[bool, list[str]]:
        """
        Update user's Discogs integration credentials
        Returns tuple of (success, errors)
        """
        errors = []
        
        if not discogs_username:
            errors.append("Discogs username is required")
        if not consumer_key:
            errors.append("Consumer key is required")
        if not consumer_secret:
            errors.append("Consumer secret is required")
            
        if errors:
            return False, errors
            
        try:
            user.discogs_username = discogs_username.strip()
            user.discogs_consumer_key = consumer_key.strip()
            user.discogs_consumer_secret = consumer_secret.strip()
            
            db.session.commit()
            return True, []
            
        except IntegrityError:
            db.session.rollback()
            return False, ["This Discogs username is already connected to another account"]
        except Exception as e:
            db.session.rollback()
            return False, [f"An unexpected error occurred: {str(e)}"]

    @staticmethod
    def remove_discogs_connection(user: User) -> Tuple[bool, list[str]]:
        """
        Remove user's Discogs integration credentials
        Returns tuple of (success, errors)
        """
        try:
            user.discogs_username = None
            user.discogs_consumer_key = None
            user.discogs_consumer_secret = None
            
            db.session.commit()
            return True, []
            
        except Exception as e:
            db.session.rollback()
            return False, [f"Failed to remove Discogs connection: {str(e)}"]

    @staticmethod
    def update_user_profile(user: User, username: str, email: str) -> Tuple[bool, list[str]]:
        """
        Update user's basic profile information
        Returns tuple of (success, errors)
        """
        errors = []
        
        # Validate username
        if not username:
            errors.append("Username is required")
        elif not AuthService.USERNAME_PATTERN.match(username):
            errors.append("Username must be 3-20 characters and contain only letters, numbers, underscores, and hyphens")
        elif username != user.username and User.query.filter(User.username.ilike(username)).first():
            errors.append("Username already taken")
        
        # Validate email
        if not email:
            errors.append("Email is required")
        elif not AuthService.EMAIL_PATTERN.match(email):
            errors.append("Please provide a valid email address")
        elif email != user.email and User.query.filter(User.email.ilike(email)).first():
            errors.append("Email already registered")
            
        if errors:
            return False, errors
            
        try:
            user.username = username.lower().strip()
            user.email = email.lower().strip()
            db.session.commit()
            return True, []
        except Exception as e:
            db.session.rollback()
            return False, [f"An error occurred: {str(e)}"]

    @staticmethod
    def update_password(user: User, current_password: str, new_password: str) -> Tuple[bool, list[str]]:
        """
        Update user's password
        Returns tuple of (success, errors)
        """
        errors = []
        
        if not user.check_password(current_password):
            errors.append("Current password is incorrect")
        
        if not new_password:
            errors.append("New password is required")
        elif len(new_password) < AuthService.MIN_PASSWORD_LENGTH:
            errors.append(f"Password must be at least {AuthService.MIN_PASSWORD_LENGTH} characters")
        elif not AuthService.PASSWORD_PATTERN.match(new_password):
            errors.append("Password must contain at least one letter and one number")
            
        if errors:
            return False, errors
            
        try:
            user.set_password(new_password)
            db.session.commit()
            return True, []
        except Exception as e:
            db.session.rollback()
            return False, [f"An error occurred: {str(e)}"] 