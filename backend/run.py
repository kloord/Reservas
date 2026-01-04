"""
Punto de entrada principal para ejecutar la aplicación Flask.
Lee el puerto desde la variable de entorno `PORT` si está definida.
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=True, host='0.0.0.0', port=port)
