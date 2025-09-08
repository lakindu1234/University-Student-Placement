from flask import Flask, request, jsonify
import pickle
import numpy as np
import json

app = Flask(__name__)

# Load model
with open("college_student_placement.pkl", "rb") as f:
    model = pickle.load(f)

# Load feature columns
with open("columns.json", "r") as f:
    columns = json.load(f)["data_columns"]

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        # Arrange inputs in same order as training columns
        input_data = [data.get(col, 0) for col in columns]
        input_array = np.array([input_data])

        prediction = model.predict(input_array)[0]  # 0 or 1
        result = "Selected for Internship" if prediction == 1 else "Not Selected"

        return jsonify({"prediction": int(prediction), "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
