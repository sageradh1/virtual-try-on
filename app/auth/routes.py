import os
from flask import render_template, redirect, url_for, flash, request, jsonify,current_app,abort, session, request
from werkzeug.security import check_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
import asyncio
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from . import auth
from app.extensions import db, get_synthesiser, synthesiser
from app.auth.models import GeneratedImage, User
from app.logger import app_logger
from app.auth.models import GeneratedImage
from app.extensions import db

background_tasks_queue = asyncio.Queue() 

def get_db():
    from app.extensions import db
    return db

@auth.route('/check-thread-status', methods=['GET'])
def check_thread_status():
    global thread
    if thread and thread.is_alive():
        thread_status = 'running'
    else:
        thread_status = 'not running'
    return jsonify({'thread_status': thread_status})


# Asynchronous function to use the object's pipeline
async def async_use_pipeline(data_dict):
    app_logger.info("Inside async_use_pipeline")
    try:
        clothes = [
            f"{current_app.config['CLOTHES_PHOTOS_DEST']}/shirt.jpg"
            # f"{current_app.config['CLOTHES_PHOTOS_DEST']}/suit.jpeg"
        ]

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # db = get_db()
        tasks = []
        for cloth in clothes:
            data=dict()
            data['person_image_path']=data_dict['person_image_path']
            data['cloth_image_path']=cloth
            
            # result_image = loop.run_in_executor(None, synthesiser.produce_synthesized_image, data)
            result_image = await synthesiser.produce_synthesized_image(data)

            datetime_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_generated_filename = f"{data_dict['uploaded_filename_ext']}_{datetime_stamp}{data_dict['uploaded_filename_ext']}"
            generated_file_path = os.path.join(current_app.config['GENERATED_PHOTOS_DEST'], new_generated_filename)
            result_image.save(generated_file_path)
            generated_image = GeneratedImage(
                username=data_dict['username'],
                source_image=data_dict['person_image_path'],
                generated_image_path=generated_file_path
            )
            db.session.add(generated_image)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Issue while trying to generate new image")
        app_logger.error("Error: Issue while trying to generate new image",e)
        return jsonify({
            "status": 400,
            "message": "Could not create a user"
        }), 400

async def async_use_pipeline(data_dict):
    app_logger.info("Inside async_use_pipeline")
    try:
        clothes = [
            f"{current_app.config['CLOTHES_PHOTOS_DEST']}/shirt.jpg"
            # f"{current_app.config['CLOTHES_PHOTOS_DEST']}/suit.jpeg"
        ]

        tasks = []
        for cloth in clothes:
            data = dict()
            data['person_image_path'] = data_dict['person_image_path']
            data['cloth_image_path'] = cloth

            # Create a task for each image generation and store it
            task = asyncio.create_task(synthesiser.produce_synthesized_image(data))
            tasks.append(task)

        for generated_image in tasks:
            datetime_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_generated_filename = f"{data_dict['uploaded_filename_ext']}_{datetime_stamp}{data_dict['uploaded_filename_ext']}"
            generated_file_path = os.path.join(current_app.config['GENERATED_PHOTOS_DEST'], new_generated_filename)
            generated_image.save(generated_file_path)

            # Prepare data for background processing (optional)
            background_data = {
                'username': data_dict['username'],
                'source_image_path': data_dict['person_image_path'],
                'generated_image_path': generated_file_path
            }

            global background_tasks
            background_tasks.append(background_data)

    except Exception as e:
        print("Error generating images:", e)
        app_logger.error("Error", e)

background_tasks = []

async def handle_generated_image_background():
    while True:
        async with background_tasks_queue.get() as data:
            try:
                print(f"Processing generated image for user: {data['username']}")
                generated_image = GeneratedImage(
                    username=data['username'],
                    source_image_path=data['source_image_path'],
                    generated_image_path=data['generated_image_path']
                )
                db.session.add(generated_image)
                db.session.commit()

            except Exception as e:
                print(f"Error processing image in background: {e}")


@auth.route("/register-postman", methods=['GET', 'POST'])
def register():
    global thread 
    print("Registration started")
    # db = get_db()
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
        uploaded_filename_base, uploaded_filename_ext = os.path.splitext(secure_filename(file.filename))
        new_uploaded_filename = f"{uploaded_filename_base}_{datetime_stamp}{uploaded_filename_ext}"
        uploaded_file_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], new_uploaded_filename)
        print("uploaded_file_path",uploaded_file_path)
        file.save(uploaded_file_path)
        
        data_dict = dict()
        data_dict['uploaded_filename_base']=uploaded_filename_base
        data_dict['uploaded_filename_ext']=uploaded_filename_ext
        data_dict['person_image_path']=uploaded_file_path
        data_dict['username']=username
        
        try:
            # Processing one image for demo
            clothes = [
                f"{current_app.config['CLOTHES_PHOTOS_DEST']}/shirt.jpg"
                # f"{current_app.config['CLOTHES_PHOTOS_DEST']}/suit.jpeg"
                # '/Users/sagar/working_dir/github_personal/virtual-try-on/app/static/clothes/shirt.jpg'
            ]

            for cloth in clothes:
                data = dict()
                data['person_image_path'] = data_dict['person_image_path']
                data['cloth_image_path'] = cloth

                # Create a task for each image generation and store it
                # generated_image= synthesiser.produce_synthesized_image(data)
                generated_image = get_synthesiser().produce_synthesized_image(data)

                # Wait for all image generation tasks to complete
                # generated_images = await asyncio.gather(*tasks)

                datetime_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_generated_filename = f"{data_dict['uploaded_filename_base']}_{datetime_stamp}{data_dict['uploaded_filename_ext']}"
                generated_file_path = os.path.join(current_app.config['GENERATED_PHOTOS_DEST'], new_generated_filename)
                # generated_file_path = os.path.join('/Users/sagar/working_dir/github_personal/virtual-try-on/app/static/generated', new_generated_filename)
                generated_image.save(generated_file_path)

                    # Prepare data for background processing (optional)
                background_data = {
                    'username': data_dict['username'],
                    'source_image_path': data_dict['person_image_path'],
                    'generated_image_path': generated_file_path
                }

                from app.auth.models import GeneratedImage

                generated_image = GeneratedImage(
                    username=data_dict['username'],
                    source_image_path=data_dict['person_image_path'],
                    generated_image_path=generated_file_path
                )
                db.session.add(generated_image)
                db.session.commit()



                # background_synthesis_function.delay(data_dict=data_dict)

                user = User(username=username, image_path=uploaded_file_path)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()

                # asyncio.create_task(async_use_pipeline(data_dict))

                return jsonify({
                    "status": 200,
                    "message": "User created and image synthesis started successfully.",
                    "data": user.to_dict()
                }), 200
        except Exception as e:
            print("4")
            print(e)
            db.session.rollback()
            return jsonify({
                "status": 400,
                "message": "Could not create a user"
            }), 400


@auth.route("/login", methods=['POST'])
def login():
    db = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


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

@auth.route('/get-generated-images', methods=['GET'])
def get_generated_images():
    images = GeneratedImage.query.all()
    images_data = [image.to_dict() for image in images]
    return jsonify(images_data), 200

@auth.route('/protected-route',methods=['GET'])
def protected_route():
    if 'user_id' not in session:
        abort(401)
    return 'This is a protected route.'

@auth.route("/logout",methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"status": 200, "message": "Logged out successfully"}), 200
