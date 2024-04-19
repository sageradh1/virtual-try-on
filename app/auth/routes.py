from flask import render_template, redirect, url_for, flash, request, jsonify,current_app,abort, session, request
from . import auth
# from app import db
from app.auth.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from werkzeug.security import check_password_hash
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime
from werkzeug.utils import secure_filename
import os


def get_db():
    from app.extensions import db
    return db


# Reference if wtf_form is used
# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     photo = FileField('Profile Photo', validators=[FileAllowed(photos, 'Images only!')])
#     submit = SubmitField('Sign Up')


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
@auth.route("/register", methods=['GET', 'POST'])
def register():

    db = get_db()
    if request.method == 'GET':
        return render_template('auth/register.html')
    if request.method == 'POST':

        required_fields = ['username', 'password', 'image']
        missing_fields = [field for field in required_fields if field not in request.form and field not in request.files]

        if missing_fields:
            return jsonify({
                "status": 422,
                "error": "Bad request",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 422

        username = request.form['username']
        password = request.form['password']
        file = request.files['image']
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return jsonify({
                "error": "Conflict",
                "message": "A user with the provided username already exists."
            }), 409
            flash('A user with that username already exists.', 'warning')
            return render_template('auth/register.html')

        if not file:
            return jsonify({
                "status": 422,
                "error": "Bad request",
                "message": f"Please confirm that image file is submitted."
            }), 422
            
        if not allowed_file(file.filename):
            return jsonify({
                "status": 422,
                "error": "Bad request",
                "message": f"Please confirm that image file is in the right format."
            }), 422

        datetime_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_base, filename_ext = os.path.splitext(secure_filename(file.filename))
        new_filename = f"{filename_base}_{datetime_stamp}{filename_ext}"

        file_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], new_filename)
        try:
            file.save(file_path)
            user = User(username=username, image_path=file_path)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                "status": 200,
                "message": "User create successfully",
                "data": user.to_dict()
            }), 200
            
            flash('Your account has been created!', 'success')
            return redirect(url_for('main.home'))
        
        except Exception as e:
            print("4")
            print(e)
            db.session.rollback()
            return jsonify({
                "status": 400,
                "message": "Could not create a user"
            }), 400
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Error: {e}")
#     return render_template('register.html')


@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']

        # data = request.get_json()


        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({
                "status": 404,
                "error": "Not Found",
                "message": "User not found."
            }), 404

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return jsonify({
                "status": 200,
                "message": "Login successful",
                "data": user.to_dict()    
            }), 200
        else:
            return jsonify({
                "status": 401,
                "error": "Unauthorized",
                "message": "Invalid username or password."
            }), 401

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@auth.route('/get-users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [user.to_dict() for user in users]
    return jsonify(users_data), 200


@auth.route('/protected-route',methods=['GET'])
def protected_route():
    if 'user_id' not in session:
        abort(401)
    else:
        if request.method == 'GET':
            return render_template('postloggedin/items.html')
        
@auth.route('/product-info',methods=['GET'])
def product_info():
    if 'user_id' not in session:
        abort(401)
    else:
        if request.method == 'GET':
            return render_template('postloggedin/productinfo.html')

@auth.route("/logout",methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"status": 200, "message": "Logged out successfully"}), 200
