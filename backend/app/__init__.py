"""
Inicialización de la aplicación Flask.
Este módulo configura la aplicación Flask, CORS y registra los blueprints.
"""
from flask import Flask
from flask_cors import CORS


def create_app():
    """
    Factory function para crear y configurar la aplicación Flask.
    
    Returns:
        Flask: Instancia configurada de la aplicación Flask
    """
    app = Flask(__name__)
    
    # Configuración básica
    app.config['JSON_AS_ASCII'] = False  # Para soportar caracteres UTF-8
    app.config['JSON_SORT_KEYS'] = False
    
    # Configurar CORS para permitir peticiones desde el frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Registrar blueprints
    from app.routes.cabins import cabins_bp
    from app.routes.reservations import reservations_bp
    from app.routes.availability import availability_bp
    
    app.register_blueprint(cabins_bp, url_prefix='/api/cabins')
    app.register_blueprint(reservations_bp, url_prefix='/api/reservations')
    app.register_blueprint(availability_bp, url_prefix='/api/availability')
    
    # Ruta de health check
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'API is running'}, 200
    
    return app
