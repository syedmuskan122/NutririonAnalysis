from flask import Flask, render_template, request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates")

# -------------------------
# Load your trained model
# -------------------------
MODEL_PATH = "nutrition.h5"
model = load_model(MODEL_PATH)
print("✅ Loaded model from disk")

# -------------------------
# Nutrition data function
# -------------------------
def get_nutrition(fruit_name):
    nutrition_data = {
        "APPLE": {"Calories": 52, "Carbs": "14g", "Protein": "0.3g"},
        "BANANA": {"Calories": 89, "Carbs": "23g", "Protein": "1.1g"},
        "ORANGE": {"Calories": 47, "Carbs": "12g", "Protein": "0.9g"},
        "PINEAPPLE": {"Calories": 50, "Carbs": "13g", "Protein": "0.5g"},
        "WATERMELON": {"Calories": 30, "Carbs": "8g", "Protein": "0.6g"}
    }
    return nutrition_data.get(fruit_name, {"error": "Fruit not found"})

# -------------------------
# Home Page
# -------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -------------------------
# Image Upload / Classify Page
# -------------------------
@app.route('/image1', methods=['GET', 'POST'])
def image1():
    return render_template("image1.html")

# -------------------------
# About page
# -------------------------
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# -------------------------
# Contact page
# -------------------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

# -------------------------
# Predict route
# -------------------------
@app.route('/predict', methods=['POST'])
def predict():
    f = request.files.get('file')
    if not f:
        return "No file uploaded", 400

    try:
        # Save uploaded file
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, "uploads")
        os.makedirs(upload_path, exist_ok=True)
        filename = secure_filename(f.filename)
        filepath = os.path.join(upload_path, filename)
        f.save(filepath)
        print("Saved file at:", filepath)

        # Preprocess image
        img = image.load_img(filepath, target_size=(64, 64))  # adjust size if needed
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0  # normalize if model was trained on normalized images

        # Model prediction
        pred_probs = model.predict(x)[0]
        pred_class = np.argmax(pred_probs)
        fruits = ['APPLE', 'BANANA', 'ORANGE', 'PINEAPPLE', 'WATERMELON']
        fruit_name = fruits[pred_class]
        confidence = round(pred_probs[pred_class]*100, 2)
        print(f"Detected: {fruit_name} ({confidence}%)")

        # Get nutrition info
        nutrition_info = get_nutrition(fruit_name)

        # Render result
        return render_template("0.html", showcase=nutrition_info, showcase1=fruit_name, confidence=confidence)

    except Exception as e:
        print("Prediction error:", e)
        return "Error during prediction", 500

# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
