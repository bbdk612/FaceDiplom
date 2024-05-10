import numpy as np
from flask import Flask, render_template, send_from_directory, jsonify
from CameraCapturing import CameraCapturing

app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"

cap = CameraCapturing(0, [["know/Mishana.jpg", "Mishana"]])

@app.route('/start_capture')
def start_cap():
    cap.start()
    return jsonify({"message": "Zaebis"})

@app.route('/stop-capture')
def stop_cap():
    students = cap.stop_capturing()
    return jsonify({"students": students})

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
