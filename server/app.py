from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import json
import os

class PlacementApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        # Setup paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "college_student_placement.pkl")
        columns_path = os.path.join(base_dir, "columns.json")

        # Load model and columns
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        with open(columns_path, "r") as f:
            self.columns = json.load(f)["data_columns"]

        # Define routes
        self.app.add_url_rule("/predict", view_func=self.predict, methods=["POST"])

    def predict(self):
        data = request.json
        try:
            # Arrange input in training column order
            input_data = [data.get(col, 0) for col in self.columns]
            input_array = np.array([input_data])

            prediction = self.model.predict(input_array)[0]
            result = "Selected for Internship" if prediction == 1 else "Not Selected"

            return jsonify({"prediction": int(prediction), "result": result})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    app_instance = PlacementApp()
    app_instance.run()
