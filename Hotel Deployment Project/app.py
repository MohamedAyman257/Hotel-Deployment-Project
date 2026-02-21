from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("hotel_model.pkl")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():

    try:
        input_data = {
            'number_of_people': int(request.form['number_of_people']),
            'number_of_nights': int(request.form['number_of_nights']),
            'room_type': request.form['room_type'],
            'type_of_meal': request.form['type_of_meal'],
            'car_parking_space': request.form['car_parking_space'],
            'market_segment_type': request.form['market_segment_type'],
            'repeated': int(request.form['repeated']),
            'lead_time': float(request.form['lead_time']),
            'p-c': int(request.form['p-c']),
            'p-not-c': int(request.form['p-not-c']),
            'special_requests': int(request.form['special_requests']),
            'average_price': float(request.form['average_price']),
            'day': int(request.form['day']),
            'month': int(request.form['month']),
            'year': int(request.form['year'])
        }

        input_df = pd.DataFrame([input_data])

        prediction = model.predict(input_df)[0]

        if prediction == 1:
            result = "Booking Will Be Cancelled ❌"
            color = "danger"
        else:
            result = "Booking Will Not Be Cancelled ✅"
            color = "success"

        return render_template("index.html", prediction=result, color=color)

    except:
        return render_template("index.html", prediction="Invalid Input ❗", color="warning")

if __name__ == "__main__":
    app.run(debug=True)