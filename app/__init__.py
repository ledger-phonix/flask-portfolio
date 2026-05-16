from flask import Flask
from flask_mail import Mail
import cloudinary
from .database import db_handler
import os
from dotenv import load_dotenv
mail = Mail()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    
    #code for mail configuration 
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MY_PERSONAL_EMAIL'] = os.getenv("MAIL_PERSONAL")
    
    mail.init_app(app)
    
    #cloudinary configration
    cloudinary.config(
        cloud_name = os.getenv("CLOUDINARY_NAME"),
        api_key = os.getenv("CLOUDINARY_KEY"),
        api_secret = os.getenv("CLOUDINARY_SECRET"),
        secure = True
    )
    
    db_handler.connect(
        uri= os.getenv("MONGO_URI"),
        db_name= os.getenv("DB_NAME")
        )
    
    
    from .routes import main
    from .admin_routes import admin
    
    app.register_blueprint(main)
    app.register_blueprint(admin , url_prefix='/admin')
    return app