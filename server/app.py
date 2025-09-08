from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # ✅ allow cross-origin requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "college_student_placement.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


