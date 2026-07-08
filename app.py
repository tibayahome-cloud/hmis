from datetime import datetime
import logging
import os

from flask import abort, Flask, render_template, request
from dotenv import load_dotenv


from utils import contribute, register, webhooks, withdraw

# Load environment variables
load_dotenv()

DEBUG_MODE = os.getenv('IS_DEBUG', 'False') in ['True', '1', 't']

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



# @app.route('/terms')
# def terms_route():
#     return render_template('terms.html')


# @app.route('/privacy')
# def privacy_route():
#     return render_template('privacy.html')


if __name__ == '__main__':    
    app.run(debug=DEBUG_MODE)