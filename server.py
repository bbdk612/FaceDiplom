from flask import Flask, render_template, send_from_directory, jsonify, redirect, request, flash, get_flashed_messages
from flask_login import current_user, login_required, logout_user
from CameraCapturing import CameraCapturing
from core import app, login_manager
from forms.LoginForm import LoginForm
from forms.MakeUserForm import MakeUserForm
from models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

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

@app.route('/login/', methods=["get", "post"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
    
    return render_template("login.html", form=form)

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Вы успешно вышли"})

@app.route('/registrate/', methods=["GET", "POST"])
def registrate():
    form = MakeUserForm(request.form)
    print(form.errors)
    if request.method == "POST" and form.validate():
        user = User(login=form.login.data, fio=form.fio.data, is_admin=form.is_admin.data)
        data = User.create(user, form.password.data)
        if data["id"] == -1:
            flash(data["message"])
            return redirect("/registrate/")
        else: 
            flash(data["message"])
            return redirect("/login/")

    messages = get_flashed_messages()
    return render_template("admin/make_user.html", form=form, messages=messages)

@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect("/admin")
        
        return render_template("user/index.html")

    return redirect("/login/")
