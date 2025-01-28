from flask import Flask
from aiagent.config import Config

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)
    
    with app.app_context():

        # Register Blueprints (lazy imports to avoid circular imports)
        from aiagent.app.routes.chat_routes import chat_bp
        app.register_blueprint(chat_bp, url_prefix='/chat')
        from aiagent.app.routes.health_routes import health_bp
        app.register_blueprint(health_bp, url_prefix='/health')

    return app
