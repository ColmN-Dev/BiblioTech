from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user

from app.models import User
from app import db, bcrypt

from . import auth

# Define a function to validate the password based on length and character requirements
def validate_password(password):
    return (
        len(password) >= 8
        and any(char.isdigit() for char in password) # Check for numeric character
        and any(char.isupper() for char in password) # Check for uppercase character
        and any(char.islower() for char in password) # Check for lowercase character
        and any(not char.isalnum() for char in password)  # Check for special character
    )

# AUTH - SIGNUP
@auth.route("/auth/signup", methods=["GET", "POST"])
def signup():
    
    if request.method == "POST":
        
        # Get the username and password from the form, stripping any leading/trailing whitespace
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()
        
        # Basic validation so empty values do not get sent to database
        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("auth/signup.html", username=username)

        if not validate_password(password):
            flash("Password must be at least 8 characters long and contain uppercase, lowercase, numeric and special characters.", "error")
            return render_template("auth/signup.html", username=username)
    
        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different username.", "error")
        else:
            new_user = User(username=username, password_hash=bcrypt.generate_password_hash(password).decode("utf-8"))
            
            # Add the new user to the database and commit the changes
            db.session.add(new_user)
            db.session.commit()
            
            flash("Account created successfully! Please log in.", "success")
            
            # Redirect the user to the login page after successful signup
            return redirect(url_for("auth.login"))
    
    return render_template("auth/signup.html")


# AUTH - LOGIN
@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()
    
        # Basic validation so empty values do not get sent to database
        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("auth/login.html", username=username)
        
        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
        
        # Check if the user exists and if the provided password matches the stored password hash
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Log the user in and create a session for them
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("routes.your_library"))  # Redirect to the user's library after successful login
        else:
            flash("Invalid username or password", "error")
            return render_template("auth/login.html", username=username)

    return render_template("auth/login.html")


# AUTH - LOGOUT
@auth.route("/auth/logout", methods=["GET", "POST"])
@login_required
def logout():
    # Log the user out and clear their session
    logout_user()
    
    flash("Logged out successfully!", "success")
    return redirect(url_for("routes.index"))  # Redirect to the home page after logout