import numpy as np
from flask import Flask, render_template, send_from_directory, jsonify
from CameraCapturing import CameraCapturing

app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"

cap = None
@app.route('/start_capture', methods=["POST"])
def start_cap():
    global cap
    if cap is None:
        cap = CameraCapturing(0, [["know/Mishana.jpg", "Mishana"], ["know/photo_2024-05-09_23-05-17.jpg", "Artem"]])
    cap.start()
    return jsonify({"message": "Zaebis"})

@app.route('/stop_capture', methods=["POST"])
def stop_cap():
    global cap
    
    students = cap.stop_capturing()
    cap = None
    print()
    return jsonify({"students": students})

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
