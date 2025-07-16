from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from supabase import create_client, Client
import os
from functools import wraps

auth = Blueprint('auth', __name__)

# Supabase setup
url: str = "https://rcaleqoorgrhnjknlavj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJjYWxlcW9vcmdyaG5qa25sYXZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAzNzQ0MDUsImV4cCI6MjA2NTk1MDQwNX0.ZVtoEMGEybG25wFJ0524x8q-Mhfi-aXXVyypQdk58QE"
supabase: Client = create_client(url, key)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        privacy_agree = request.form.get('privacy_agree')

        if not all([username, email, password]):
            flash('All fields are required', 'error')
            return redirect(url_for('auth.signup'))
        
        if not privacy_agree:
            flash('You must agree to the Privacy Policy', 'error')
            return redirect(url_for('auth.signup'))

        try:
            # Check if username already exists in the old system for backward compatibility
            res = supabase.table('users').select("id").eq('username', username).execute()
            if res.data:
                flash('Username already exists', 'error')
                return redirect(url_for('auth.signup'))

            # Check if email already exists to give a clearer error message
            email_res = supabase.table('users').select("id").eq('email', email).execute()
            if email_res.data:
                flash('Email already exists. Please try logging in or use a different email.', 'error')
                return redirect(url_for('auth.signup'))

            # Sign up the user with Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username
                    },
                    "email_redirect_to": url_for('auth.login', _external=True)
                }
            })

            # After successful Supabase Auth sign-up, create a record in the public 'users' table
            if auth_response.user:
                try:
                    # Note: We are inserting a placeholder for the password as it's managed by Supabase Auth
                    # The 'password' column in the 'users' table has a NOT NULL constraint.
                    supabase.table('users').insert({
                        "username": username,
                        "email": email,
                        "password": "managed-by-supabase-auth"
                    }).execute()
                except Exception as db_error:
                    # This is a critical error. The user exists in Supabase Auth but not in our public users table.
                    # This can lead to login issues. For now, we flash an error.
                    # A more robust solution would be to either delete the Supabase Auth user or retry the insert.
                    flash(f"An error occurred while creating your user profile: {db_error}. Please contact support.", 'error')
                    return redirect(url_for('auth.signup'))

            # The user is signed up but needs to confirm their email
            # Supabase sends the confirmation email automatically
            flash('Registration successful! Please check your email to confirm your account before logging in.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            error_message = str(e).lower()
            if "user already registered" in error_message:
                flash('Email already registered. Please check your inbox for a confirmation link or try logging in.', 'error')
            else:
                flash(f'An error occurred: {e}', 'error')
            return redirect(url_for('auth.signup'))
            
    return render_template('auth/signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Handle confirmation tokens or access_tokens from email verification
    token = request.args.get('access_token')
    refresh_token = request.args.get('refresh_token')
    
    # If tokens are present in URL (redirected from email confirmation)
    if token and refresh_token:
        try:
            # Exchange tokens for a session
            auth_response = supabase.auth.set_session(token, refresh_token)
            user = auth_response.user
            
            if user:
                # Fetch the user profile from the public 'users' table to get the bigint ID
                profile_res = supabase.table('users').select("id").eq('email', user.email).single().execute()
                
                if not profile_res.data:
                    flash('User profile not found. Please contact support.', 'error')
                    return redirect(url_for('auth.login'))

                # Set session data
                session['user_id'] = profile_res.data['id'] # This is the bigint ID
                session['auth_user_id'] = user.id # This is the UUID
                session['username'] = user.user_metadata.get('username', 'N/A')
                flash('Email confirmed! Welcome back!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Error processing confirmation. Please try logging in.', 'error')
        except Exception as e:
            from flask import current_app
            current_app.logger.error(f"Error handling confirmation token: {str(e)}")
            flash('Error processing confirmation. Please try logging in.', 'error')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('auth.login'))
            
        try:
            # Attempt login
            auth_data = supabase.auth.sign_in_with_password({"email": email, "password": password})
            
            # Fetch the user profile from the public 'users' table to get the bigint ID
            profile_res = supabase.table('users').select("id").eq('email', email).single().execute()
            
            if not profile_res.data:
                # This case can happen if the user was created in Supabase Auth but not in the public.users table
                flash('User profile not found. Please contact support.', 'error')
                return redirect(url_for('auth.login'))

            session['user_id'] = profile_res.data['id'] # This is the bigint ID
            session['auth_user_id'] = auth_data.user.id # This is the UUID
            session['username'] = auth_data.user.user_metadata.get('username', 'N/A')
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            error_message = str(e).lower()
            if "email not confirmed" in error_message or "not confirmed" in error_message:
                flash('Your email requires confirmation. Please check your inbox for a confirmation link. If you already clicked the link, try clearing your browser cache and logging in again.', 'error')
            elif "invalid login credentials" in error_message:
                flash('Invalid email or password. Please try again.', 'error')
            else:
                flash('Login failed. Please try again.', 'error')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth.route('/privacy-policy')
def privacy_policy():
    return render_template('auth/privacy_policy.html')
    
@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index')) 

@auth.route('/resend-confirmation', methods=['POST'])
def resend_confirmation():
    if request.is_json:
        email = request.json.get('email')
    else:
        email = request.form.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    try:
        # Send confirmation email through Supabase
        response = supabase.auth.resend_sign_up(email=email)
        
        # If we get here without an exception, the email was sent successfully
        return jsonify({'success': True, 'message': 'Confirmation email resent'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500 