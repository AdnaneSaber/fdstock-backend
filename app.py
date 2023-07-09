
from flask_cors import CORS
import os
from flask import Flask
import os
from dotenv import load_dotenv
from chat.main import chat_bp, init_socketio_app
from auth.main import auth_bp
from images_app.main import images_bp
from profile.main import profile_bp
load_dotenv()

# Fetch the secret key
secret_key = os.getenv('SECRET_KEY')





def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = secret_key
    app.config['UPLOAD_FOLDER'] = 'uploads'

    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}    
    init_socketio_app(app)
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(profile_bp)
    
    return app
if __name__ == '__main__':
    root = create_app()
    root.run(
        host="localhost",
        port="8000",
        debug=True
    )
