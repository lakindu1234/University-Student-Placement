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

        # Check if files exist
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(columns_path):
            raise FileNotFoundError(f"Columns file not found: {columns_path}")

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
            # Validate that all required columns are present
            missing_columns = [col for col in self.columns if col not in data]
            if missing_columns:
                return jsonify({"error": f"Missing required fields: {', '.join(missing_columns)}"}), 400

            # Define validation ranges
            validation_rules = {
                "iq": {"min": 70, "max": 160},
                "prev_sem_result": {"min": 2.0, "max": 4.0},
                "cgpa": {"min": 2.0, "max": 4.0},
                "academic_performance": {"min": 1, "max": 10},
                "extra_curricular_score": {"min": 0, "max": 10},
                "communication_skills": {"min": 1, "max": 10},
                "projects_completed": {"min": 0, "max": 5},
                "internship_experience_yes": {"min": 0, "max": 1}
            }

            # Validate input values
            for field, rules in validation_rules.items():
                if field in data:
                    value = float(data[field])
                    if value < rules["min"] or value > rules["max"]:
                        return jsonify({"error": f"{field} must be between {rules['min']} and {rules['max']}"}), 400

            # Arrange input in training column order
            input_data = [data.get(col, 0) for col in self.columns]
            input_array = np.array([input_data])

            prediction = self.model.predict(input_array)[0]
            result = "Selected for Internship" if prediction == 1 else "Not Selected"

            return jsonify({"prediction": int(prediction), "result": result})
        except ValueError as e:
            return jsonify({"error": f"Invalid input data: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": f"Prediction error: {str(e)}"}), 500

    def run(self):
        self.app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    try:
        app_instance = PlacementApp()
        app_instance.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure that 'college_student_placement.pkl' and 'columns.json' are in the server directory.")
        exit(1)
    except Exception as e:
        print(f"Failed to start application: {e}")
        exit(1)
