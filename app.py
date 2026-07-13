from datetime import datetime
import logging
import os

from flask import Flask, render_template
from dotenv import load_dotenv

from routes.patients import patients_bp
from routes.consultations import consultations_bp
from routes.ai_help import ai_help_bp

# Load environment variables
load_dotenv()

DEBUG_MODE = os.getenv('IS_DEBUG', 'False') in ['True', '1', 't']
PORT = int(os.getenv('PORT', '5000'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

secret = os.environ.get('SECRET_KEY')

if not secret:
    raise RuntimeError("SECRET_KEY not set")

app = Flask(__name__)
app.secret_key = secret
app.jinja_env.globals['now'] = datetime.now


# Routes
@app.route('/')
def index():    
    return render_template('index.html')

# Register blueprints from other modules
app.register_blueprint(patients_bp)
app.register_blueprint(consultations_bp)
app.register_blueprint(ai_help_bp)


if __name__ == '__main__':    
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=PORT)