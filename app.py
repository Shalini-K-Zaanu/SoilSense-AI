from flask import Flask, request, render_template_string, render_template, redirect, url_for, session
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import joblib
import pandas as pd
from datetime import datetime
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__)

# Secret key for login sessions
app.secret_key = "soilsense_secret_key_2026"


# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

def get_db():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],
        cursor_factory=RealDictCursor
    )


# -----------------------------------
# CREATE DATABASE
# -----------------------------------

def create_database():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS soil_analysis (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            ph REAL,
            soil_moisture REAL,
            organic_matter REAL,
            soil_type TEXT,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            recommended_crop TEXT
        )
    """)

    conn.commit()

    cur.close()
    conn.close()


create_database()


# -----------------------------------
# LOAD MODEL AND DATA
# -----------------------------------

model = joblib.load("soil_model.pkl")
crop_model = joblib.load("crop_model.pkl")

df = pd.read_csv("Crop_recommendationV2.csv")

TARGET_COLUMNS = ["N", "P", "K"]


# -----------------------------------
# CREATE PREPROCESSOR
# -----------------------------------

X = df.drop(columns=TARGET_COLUMNS)

categorical_columns = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_columns
        )
    ],
    remainder="passthrough"
)

preprocessor.fit(X)


# -----------------------------------
# NUTRIENT STATUS
# -----------------------------------

def get_nutrient_status(value):

    if value < 30:
        return "Low", "⚠️"

    elif value <= 60:
        return "Medium", "🌱"

    else:
        return "High", "✅"


# -----------------------------------
# FARMING SUGGESTION
# -----------------------------------

def get_suggestion(nutrient, status):

    if nutrient == "Nitrogen":

        if status == "Low":
            return "Apply nitrogen-rich fertilizer"

        elif status == "Medium":
            return "Monitor nitrogen levels"

        else:
            return "Reduce nitrogen application"

    elif nutrient == "Phosphorus":

        if status == "Low":
            return "Apply phosphorus-rich fertilizer"

        elif status == "Medium":
            return "Monitor phosphorus levels"

        else:
            return "Reduce phosphorus application"

    elif nutrient == "Potassium":

        if status == "Low":
            return "Apply potassium-rich fertilizer"

        elif status == "Medium":
            return "Monitor potassium levels"

        else:
            return "Reduce potassium application"

    return "Continue monitoring your soil."


# -----------------------------------
# REGISTER
# -----------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        try:

            cur.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, password)
            )

            conn.commit()

            cur.close()
            conn.close()

            return redirect(url_for("login"))

        except psycopg2.IntegrityError:

            conn.rollback()

            cur.close()
            conn.close()

            error = "An account with this email already exists."

    return render_template(
        "register.html",
        error=error
    )


# -----------------------------------
# LOGIN
# -----------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s AND password = %s
            """,
            (email, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        else:

            error = "Invalid email or password."

    return render_template(
        "login.html",
        error=error
    )


# -----------------------------------
# DASHBOARD
# -----------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM soil_analysis
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    analyses = cur.fetchall()

    cur.close()
    conn.close()

    return render_template_string("""

<!DOCTYPE html>

<html>

<head>

    <title>Dashboard | SoilSense AI</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {

            min-height: 100vh;

            background: linear-gradient(
                135deg,
                #e8f5e9,
                #f5fff6
            );

            color: #183b25;
        }

        .container {

            width: 92%;
            max-width: 1000px;

            margin: 40px auto;
        }

        .header {

            position: relative;

            min-height: 130px;

            margin-bottom: 30px;
        }

        .brand {

            display: flex;

            flex-direction: column;

            gap: 6px;

            text-align: center;

            align-items: center;

            width: 100%;

            padding-top: 45px;
        }

        .brand h1 {

            position: absolute;

            left: 0;

            top: 0;

            color: #125c32;

            font-size: 32px;

            line-height: 1.2;
        }

        .brand h2 {

            color: #205c37;

            font-size: 28px;

            font-weight: 600;

            margin-top: 5px;
        }

        .brand h3 {

            color: #35a85c;

            font-size: 25px;

            font-weight: 500;
        }

        .brand p {

            color: #637667;

            font-size: 15px;

            margin-top: 2px;
        }

        .logout {

            position: absolute;

            right: 0;

            top: 0;

            text-decoration: none;

            color: white;

            background: #c62828;

            padding: 10px 18px;

            border-radius: 10px;

            font-weight: bold;

            white-space: nowrap;
        }

        .welcome {

            background: white;

            padding: 30px;

            border-radius: 22px;

            box-shadow:
                0 10px 35px
                rgba(30, 90, 50, 0.10);

            margin-bottom: 25px;

            animation: dashboardReveal 0.7s ease forwards;
        }

        .welcome h2 {

            color: #205c37;

            margin-bottom: 10px;
        }

        .welcome p {

            color: #637667;
        }

        .new-analysis {

            display: block;

            text-align: center;

            text-decoration: none;

            background: linear-gradient(
                90deg,
                #15783d,
                #35a85c
            );

            color: white;

            padding: 18px;

            border-radius: 14px;

            font-size: 18px;

            font-weight: bold;

            margin-bottom: 25px;

            animation: dashboardReveal 0.7s ease forwards;

            animation-delay: 0.2s;

            transition: all 0.4s ease;
        }

        .new-analysis:hover {

            transform: translateY(-4px) scale(1.02);

            box-shadow:
                0 10px 25px
                rgba(21, 120, 61, 0.25);
        }

        .history {

            background: white;

            padding: 30px;

            border-radius: 22px;

            box-shadow:
                0 10px 35px
                rgba(30, 90, 50, 0.10);

            animation: dashboardReveal 0.7s ease forwards;

            animation-delay: 0.4s;
        }

        .history h2 {

            color: #205c37;

            margin-bottom: 15px;
        }

        .analysis-card {

            border: 1px solid #d8eadc;

            background: #f8fff9;

            padding: 18px;

            border-radius: 14px;

            margin-bottom: 15px;
        }

        .analysis-card:last-child {

            margin-bottom: 0;
        }

        .analysis-date {

            color: #637667;

            font-size: 14px;

            margin-bottom: 10px;
        }

        .analysis-values {

            display: flex;

            gap: 10px;

            flex-wrap: wrap;

            margin: 10px 0;
        }

        .value {

            background: white;

            border: 1px solid #d8eadc;

            padding: 8px 12px;

            border-radius: 8px;

            font-size: 14px;
        }

        .crop {

            color: #15783d;

            font-weight: bold;

            margin-top: 8px;
        }

        .empty {

            color: #637667;

            text-align: center;

            padding: 30px;
        }

        @keyframes dashboardReveal {

            from {

                opacity: 0;

                transform: translateY(25px);
            }

            to {

                opacity: 1;

                transform: translateY(0);
            }
        }

        body {

            animation: pageFadeIn 0.6s ease-in-out;
        }

        @keyframes pageFadeIn {

            from {

                opacity: 0;

                transform: translateY(15px);
            }

            to {

                opacity: 1;

                transform: translateY(0);
            }
        }

        button,
        .btn,
        a {

            transition: all 0.25s ease;
        }

        button:hover,
        .btn:hover,
        a:hover {

            transform: translateY(-2px);
        }

        @media (max-width: 600px) {

            .header {

                flex-direction: column;

                gap: 20px;
            }

            .logout {

                align-self: flex-end;
            }
        }

    </style>

</head>


<body>

    <div class="container">

        <div class="header">

            <div class="brand">

                <h1>SoilSense AI 🌱</h1>

                <h2>Know Your Soil 🍃</h2>

                <h3>Nurture Your Harvest 🌱</h3>

                <p>
                    Where soil intelligence meets sustainable farming.
                </p>

            </div>

            <a href="/logout" class="logout">
                Logout
            </a>

        </div>


        <div class="welcome">

            <h2>
                Welcome, {{ session["user_name"] }} 👋
            </h2>

            <p>
                Your personal soil analysis dashboard.
            </p>

        </div>


        <a href="/soil-input" class="new-analysis">

            🌱 Start New Soil Analysis →

        </a>


        <div class="history">

            <h2>📊 Previous Analyses</h2>

            {% if analyses %}

                {% for analysis in analyses %}

                    <div class="analysis-card">

                        <div class="analysis-date">

                            📅 {{ analysis["date"] }}

                        </div>

                        <div class="analysis-values">

                            <div class="value">

                                🌿 N:
                                {{ analysis["nitrogen"] }}
                                mg/kg

                            </div>

                            <div class="value">

                                🌱 P:
                                {{ analysis["phosphorus"] }}
                                mg/kg

                            </div>

                            <div class="value">

                                🍃 K:
                                {{ analysis["potassium"] }}
                                mg/kg

                            </div>

                        </div>

                        <div class="crop">

                            🌾 Recommended Crop:
                            {{ analysis["recommended_crop"] }}

                        </div>

                    </div>

                {% endfor %}

            {% else %}

                <div class="empty">

                    No soil analyses yet.

                    <br><br>

                    Start your first soil analysis above.

                </div>

            {% endif %}

        </div>

    </div>

</body>

</html>

""", analyses=analyses)


# -----------------------------------
# SOIL INPUT / PREDICTION
# -----------------------------------

@app.route("/soil-input", methods=["GET", "POST"])
def soil_input():

    if "user_id" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        try:

            # -----------------------------------
            # GET USER INPUT
            # -----------------------------------

            user_values = {

                "temperature": float(
                    request.form["temperature"]
                ),

                "humidity": float(
                    request.form["humidity"]
                ),

                "ph": float(
                    request.form["ph"]
                ),

                "soil_moisture": float(
                    request.form["soil_moisture"]
                ),

                "organic_matter": float(
                    request.form["organic_matter"]
                ),

                "soil_type": request.form["soil_type"],

                # IMPORTANT:
                # N, P and K are now taken
                # directly from the user.

                "nitrogen": float(
                    request.form["nitrogen"]
                ),

                "phosphorus": float(
                    request.form["phosphorus"]
                ),

                "potassium": float(
                    request.form["potassium"]
                )

            }


            # -----------------------------------
            # TAKE ONE EXISTING ROW AS BASE
            # -----------------------------------

            sample = df.iloc[[0]].copy()


            # -----------------------------------
            # SOIL TYPE MAPPING
            # -----------------------------------

            soil_mapping = {

                "Alluvial": 0,
                "Black": 1,
                "Clay": 2,
                "Loamy": 3,
                "Red": 4,
                "Sandy": 5

            }


            # -----------------------------------
            # REPLACE SOIL MODEL INPUT VALUES
            # -----------------------------------

            soil_model_values = {

                "temperature": user_values["temperature"],

                "humidity": user_values["humidity"],

                "ph": user_values["ph"],

                "soil_moisture": user_values["soil_moisture"],

                "organic_matter": user_values["organic_matter"],

                "soil_type": user_values["soil_type"]

            }


            for column, value in soil_model_values.items():

                if column in sample.columns:

                    if pd.api.types.is_numeric_dtype(
                        df[column]
                    ):

                        sample[column] = float(value)

                    else:

                        sample[column] = str(value)


            # -----------------------------------
            # REMOVE N P K
            # -----------------------------------

            input_data = sample.drop(
                columns=TARGET_COLUMNS,
                errors="ignore"
            )


            # -----------------------------------
            # APPLY PREPROCESSOR
            # -----------------------------------

            transformed_data = preprocessor.transform(
                input_data
            )


            # -----------------------------------
            # PREDICT SOIL N P K
            # -----------------------------------

            prediction = model.predict(
                transformed_data
            )[0]


            predicted_nitrogen = round(
                float(prediction[0]),
                2
            )

            predicted_phosphorus = round(
                float(prediction[1]),
                2
            )

            predicted_potassium = round(
                float(prediction[2]),
                2
            )


            # -----------------------------------
            # USER ENTERED N P K
            # -----------------------------------

            nitrogen = user_values["nitrogen"]

            phosphorus = user_values["phosphorus"]

            potassium = user_values["potassium"]


            # -----------------------------------
            # CROP RECOMMENDATION
            # -----------------------------------

            recommended_crop = crop_model.predict(
                [[
                    nitrogen,
                    phosphorus,
                    potassium
                ]]
            )[0]

            recommended_crop = str(
                recommended_crop
            )


            # -----------------------------------
            # TERMINAL OUTPUT
            # -----------------------------------

            print("--------------------------------")

            print("USER INPUT:")

            print(user_values)

            print(
                "SOIL MODEL PREDICTED NPK:",
                predicted_nitrogen,
                predicted_phosphorus,
                predicted_potassium
            )

            print(
                "USER ENTERED NPK:",
                nitrogen,
                phosphorus,
                potassium
            )

            print(
                "Recommended Crop:",
                recommended_crop
            )

            print("--------------------------------")


            # -----------------------------------
            # SAVE ANALYSIS
            # -----------------------------------

            conn = get_db()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO soil_analysis (
                    user_id,
                    date,
                    temperature,
                    humidity,
                    ph,
                    soil_moisture,
                    organic_matter,
                    soil_type,
                    nitrogen,
                    phosphorus,
                    potassium,
                    recommended_crop
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    session["user_id"],

                    datetime.now().strftime(
                        "%d %b %Y, %I:%M %p"
                    ),

                    user_values["temperature"],

                    user_values["humidity"],

                    user_values["ph"],

                    user_values["soil_moisture"],

                    user_values["organic_matter"],

                    user_values["soil_type"],

                    nitrogen,

                    phosphorus,

                    potassium,

                    recommended_crop
                )
            )

            conn.commit()

            cur.close()
            conn.close()


            # -----------------------------------
            # SHOW RESULT PAGE
            # -----------------------------------

            return render_template(
                "result.html",

                nitrogen=nitrogen,

                phosphorus=phosphorus,

                potassium=potassium,

                recommended_crop=recommended_crop
            )


        except Exception as e:

            print("Prediction Error:", e)

            return render_template(
                "soil_input.html",

                error="Prediction Error: " + str(e)
            )


    return render_template("soil_input.html")


# -----------------------------------
# LOGOUT
# -----------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -----------------------------------
# HOME
# -----------------------------------

@app.route("/")
def home():

    return redirect(url_for("login"))


# -----------------------------------
# RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":

    app.run(debug=True)