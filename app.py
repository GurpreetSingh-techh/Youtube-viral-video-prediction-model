from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import os

app = Flask(__name__)

# -----------------------------
# LOAD THE TRAINED MODEL
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

print("Model loaded successfully!")


# -----------------------------
# CATEGORIES
# -----------------------------

CATEGORIES = [
    "Beauty",
    "Comedy",
    "Cooking",
    "DIY",
    "Education",
    "Finance",
    "Fitness",
    "Gaming",
    "Music",
    "News",
    "Science",
    "Sports",
    "Tech",
    "Travel",
    "Vlog"
]


# -----------------------------
# UPLOAD DAYS
# -----------------------------

UPLOAD_DAYS = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():

    return render_template(
        "index.html",
        categories=CATEGORIES,
        upload_days=UPLOAD_DAYS
    )


# -----------------------------
# PREDICTION
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get data from JavaScript
        data = request.get_json()


        # -----------------------------
        # GET NUMERICAL VALUES
        # -----------------------------

        duration_sec = float(data["duration_sec"])

        title_length = float(data["title_length"])

        upload_hour = float(data["upload_hour"])

        tags_count = float(data["tags_count"])

        description_length = float(data["description_length"])

        subscriber_count = float(data["subscriber_count"])

        views = float(data["views"])

        likes = float(data["likes"])

        comments = float(data["comments"])

        shares = float(data["shares"])


        # -----------------------------
        # YES / NO → 1 / 0
        # -----------------------------

        if data["thumbnail_face"] == "Yes":

            thumbnail_face = 1

        else:

            thumbnail_face = 0


        # Get selected values
        category = data["category"]

        upload_day = data["upload_day"]


        # -----------------------------
        # CREATE INPUT DATA
        # -----------------------------

        input_data = {

            "duration_sec": duration_sec,

            "title_length": title_length,

            "thumbnail_face": thumbnail_face,

            "upload_hour": upload_hour,

            "tags_count": tags_count,

            "description_length": description_length,

            "subscriber_count": subscriber_count,

            "views": views,

            "likes": likes,

            "comments": comments,

            "shares": shares
        }


        # -----------------------------
        # CATEGORY ENCODING
        # -----------------------------

        for cat in CATEGORIES:

            column_name = f"category_{cat}"

            if category == cat:

                input_data[column_name] = 1

            else:

                input_data[column_name] = 0


        # -----------------------------
        # UPLOAD DAY ENCODING
        # -----------------------------

        for day in UPLOAD_DAYS:

            column_name = f"upload_day_{day}"

            if upload_day == day:

                input_data[column_name] = 1

            else:

                input_data[column_name] = 0


        # -----------------------------
        # CONVERT TO DATAFRAME
        # -----------------------------

        input_df = pd.DataFrame([input_data])


        # -----------------------------
        # EXACT FEATURE ORDER
        # -----------------------------

        input_df = input_df.reindex(
            columns=model.feature_names_in_,
            fill_value=0
        )


        # -----------------------------
        # MAKE PREDICTION
        # -----------------------------

        prediction = model.predict(input_df)[0]


        # -----------------------------
        # CONVERT RESULT
        # -----------------------------

        if prediction == 1:

            result = "Viral 🔥"

            message = (
                "The model predicts that this video "
                "is likely to become viral!"
            )

        else:

            result = "Not Viral 📊"

            message = (
                "The model predicts that this video "
                "is less likely to become viral."
            )


        # -----------------------------
        # MODEL CONFIDENCE
        # -----------------------------

        confidence = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(input_df)[0]

            confidence = round(
                max(probabilities) * 100,
                2
            )


        # -----------------------------
        # SEND RESULT TO WEBSITE
        # -----------------------------

        return jsonify({

            "success": True,

            "prediction": result,

            "message": message,

            "confidence": confidence

        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        })


# -----------------------------
# RUN FLASK
# -----------------------------

if __name__ == "__main__":

    app.run(debug=True)