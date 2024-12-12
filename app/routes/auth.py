from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from app.services.auth_service import AuthService

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rate limiting configuration
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME = timedelta(minutes=15)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'GET':
        return render_template('pages/auth/register.html')
        
    # Handle POST request
    user, errors = AuthService.register_user(
        username=request.form.get('username', ''),
        email=request.form.get('email', ''),
        password=request.form.get('password', '')
    )
    
    if errors:
        # If HTMX request, return validation errors inline
        if request.headers.get('HX-Request'):
            return render_template('partials/auth/register_form.html', 
                                errors=errors)
        # For regular form submit
        return render_template('pages/auth/register.html', errors=errors)

    # Registration successful
    login_user(user)
    flash('Registration successful! Welcome to Record Collection.', 'success')
    
    # For HTMX requests, send a redirect instruction
    if request.headers.get('HX-Request'):
        response = make_response()
        response.headers['HX-Redirect'] = url_for('auth.profile')
        return response
        
    # For regular form submit, redirect to profile
    return redirect(url_for('auth.profile'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login with rate limiting"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user, error = AuthService.authenticate_user(
            username_or_email=request.form.get('username_or_email', ''),
            password=request.form.get('password', '')
        )

        if error:
            if request.headers.get('HX-Request'):
                return render_template('partials/auth/login_form.html',
                                    error=error)
            flash(error, 'error')
            return render_template('pages/auth/login.html')

        login_user(user)
        flash('Successfully logged in!', 'success')
        
        # Always redirect to index for now
        return redirect(url_for('main.index'))

    return render_template('pages/auth/login.html')

def is_locked_out() -> bool:
    """Check if the current IP is locked out"""
    attempts = session.get('login_attempts', 0)
    last_attempt = session.get('last_attempt')
    
    if attempts >= MAX_LOGIN_ATTEMPTS:
        if last_attempt:
            last_attempt = datetime.fromisoformat(last_attempt)
            if datetime.utcnow() - last_attempt < LOCKOUT_TIME:
                return True
            # Lockout expired, reset attempts
            clear_login_attempts()
    return False

def increment_login_attempts():
    """Increment failed login attempts"""
    attempts = session.get('login_attempts', 0) + 1
    session['login_attempts'] = attempts
    session['last_attempt'] = datetime.utcnow().isoformat()

def clear_login_attempts():
    """Clear login attempts"""
    session.pop('login_attempts', None)
    session.pop('last_attempt', None)

def is_safe_url(target):
    """Validate URL is safe for redirects"""
    from urllib.parse import urlparse, urljoin
    from flask import request
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """Display user profile"""
    return render_template('pages/auth/profile.html', user=current_user)

@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Handle profile editing"""
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'basic_info':
            success, errors = AuthService.update_user_profile(
                user=current_user,
                username=request.form.get('username', ''),
                email=request.form.get('email', '')
            )
            if errors:
                flash(errors[0], 'error')
                return render_template('pages/auth/edit_profile.html', basic_info_errors=errors)
            flash('Profile information updated successfully!', 'success')
            
        elif form_type == 'password':
            success, errors = AuthService.update_password(
                user=current_user,
                current_password=request.form.get('current_password', ''),
                new_password=request.form.get('new_password', '')
            )
            if errors:
                flash(errors[0], 'error')
                return render_template('pages/auth/edit_profile.html', password_errors=errors)
            flash('Password updated successfully!', 'success')
            
        elif form_type == 'discogs':
            success, errors = AuthService.update_discogs_credentials(
                user=current_user,
                discogs_username=request.form.get('discogs_username', ''),
                consumer_key=request.form.get('consumer_key', ''),
                consumer_secret=request.form.get('consumer_secret', '')
            )
            if errors:
                flash(errors[0], 'error')
                return render_template('pages/auth/edit_profile.html', discogs_errors=errors)
            flash('Discogs settings updated successfully!', 'success')

        return redirect(url_for('auth.profile'))

    return render_template('pages/auth/edit_profile.html')

@auth_bp.route('/profile/discogs/disconnect', methods=['POST'])
@login_required
def disconnect_discogs():
    """Remove Discogs integration"""
    success, errors = AuthService.remove_discogs_connection(current_user)
    
    if request.headers.get('HX-Request'):
        if not success:
            flash(errors[0], 'error')
            return render_template('partials/auth/discogs_form.html', 
                                errors=errors)
        # Instead of just updating the form, redirect to refresh the whole profile
        response = make_response()
        response.headers['HX-Redirect'] = url_for('auth.profile')
        return response
    
    if not success:
        flash(errors[0], 'error')
    else:
        flash('Discogs account disconnected successfully.', 'success')
    
    return redirect(url_for('auth.profile'))

# HTMX-specific routes for live validation
@auth_bp.route('/validate/username', methods=['POST'])
def validate_username():
    """Validate username availability"""
    username = request.form.get('username', '')
    errors = AuthService.validate_registration(username, 'dummy@email.com', 'dummypass')
    username_errors = [e for e in errors if 'Username' in e]
    return render_template('partials/auth/username_validation.html',
                         errors=username_errors)

@auth_bp.route('/validate/email', methods=['POST'])
def validate_email():
    """Validate email availability"""
    email = request.form.get('email', '')
    errors = AuthService.validate_registration('dummyuser', email, 'dummypass')
    email_errors = [e for e in errors if 'Email' in e]
    return render_template('partials/auth/email_validation.html',
                         errors=email_errors) 