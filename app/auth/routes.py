from flask import render_template, redirect, url_for, flash, request, jsonify,current_app
from . import auth
# from app import db
from app.auth.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
# from flask_wtf.file import FileField, FileAllowed
# from .extensions import photos

from werkzeug.utils import secure_filename
# from werkzeug.exceptions import RequestEntityTooLarge
import os



def get_db():
    from app.extensions import db
    return db


# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     photo = FileField('Profile Photo', validators=[FileAllowed(photos, 'Images only!')])
#     submit = SubmitField('Sign Up')



@auth.route("/register-postman", methods=['GET', 'POST'])
def register():


    db = get_db()
    if request.method == 'POST':

        required_fields = ['username', 'password', 'image']
        missing_fields = [field for field in required_fields if field not in request.form and field not in request.files]

        if missing_fields:
            # Return a 400 Bad Request with missing field details in JSON
            return jsonify({
                "status": 422,
                "error": "Bad request",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 422


        username = request.form['username']
        password = request.form['password']
        file = request.files['image']
        
        # Check if the username already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('A user with that username already exists.', 'warning')
            return render_template('register.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
            try:
                file.save(file_path)
                user = User(username=username, image_file=filename)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created!', 'success')
                return redirect(url_for('main.home'))  # Adjust to your actual 'home' view
            except Exception as e:
                db.session.rollback()  # Ensure session is clean on any exception
                flash('An error occurred during registration. Please try again.', 'danger')
                print(f"Error: {e}")  # Log the error for debugging

    return render_template('auth/register.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         filename = photos.save(form.photo.data)
#         file_url = photos.url(filename)
#         user = User(username=form.username.data, email=form.email.data, photo=filename)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('auth.login'))
#     return render_template('register.html', form=form)




# @auth.route('/register-postman', methods=['POST'])
# def register():
#     # return jsonify({
#     #     'success':True
#     # })

#     db = get_db()
#     # Assuming JSON data is sent with the request
#     data = request.get_json()

#     if not data:
#         return jsonify({'error': 'No data provided'}), 400

#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     if not all([username, email, password]):
#         return jsonify({'error': 'Missing data'}), 400

#     # Check if user already exists
#     existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
#     if existing_user:
#         return jsonify({'error': 'User already exists'}), 409

#     # Create new user instance
#     user = User(username=username, email=email)
#     user.set_password(password)

#     # Add new user to the database
#     db.session.add(user)
#     db.session.commit()

#     # Optionally return the created user's information
#     return jsonify({'message': 'User created successfully', 'user': {'username': user.username, 'email': user.email}}), 201
