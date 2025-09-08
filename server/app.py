from flask import Flask, request, jsonify
import pickle
import numpy as np
import json
import os

app = Flask(__name__)

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model with absolute path
model_path = os.path.join(BASE_DIR, "..", "college_student_placement.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Load feature columns
columns_path = os.path.join(BASE_DIR, "..", "columns.json")
with open(columns_path, "r") as f:
    columns = json.load(f)["data_columns"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        input_data = [data.get(col, 0) for col in columns]
        input_array = np.array([input_data])

        prediction = model.predict(input_array)[0]
        result = "Selected for Internship" if prediction == 1 else "Not Selected"

        return jsonify({"prediction": int(prediction), "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
