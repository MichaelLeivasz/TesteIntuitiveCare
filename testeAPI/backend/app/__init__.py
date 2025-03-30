from flask import Flask
from flask_cors import CORS
import logging
from .routes import buscar_operadoras

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

app.add_url_rule('/busca', view_func=buscar_operadoras, methods=['GET'])