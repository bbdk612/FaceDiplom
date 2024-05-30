from flask import render_template,  jsonify, redirect, request, url_for
from flask_login import current_user, login_required, logout_user
from CameraCapturing import CameraCapturing
from core import app, login_manager
from forms.LoginForm import LoginForm
from models import *

cap = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/start_capture/<int:lesson_id>', methods=["POST"])
@login_required
def start_cap(lesson_id):
    global cap
    if cap is None:
        # auditory_id = Lesson.query.filter_by(id=request.form['lesson_id']).first().auditory_id
        # camera_url = Auditory.query.filter_by(id=auditory_id).first().camera_address
        lesson_students = Lesson_Student.query.filter_by(lesson_id=lesson_id).all()
        students = []
        for lesson_student in lesson_students:
            students.append(Student.query.filter_by(id=lesson_student.student_id).first())
        cap_data = []
        for student in students:
            cap_data.append([student.image_url, student.id])
        cap = CameraCapturing(0, cap_data)
        cap.start()
        return jsonify({"message": "Zaebis"})

@app.route('/stop_capture/<int:lesson_id>', methods=["POST"])
@login_required
def stop_cap(lesson_id):
    global cap
    students_ids_faces = cap.stop_capturing()
    cap = None
    students_data = []
    for student_id_face in students_ids_faces:
        if student_id_face["id"] >= 0:
            student_data = {
                "id": student_id_face["id"],
                "name": Lesson_Student.query.filter_by(student_id=student_id_face["id"], lesson_id=lesson_id).first().student.fio,
                "faceUrl": url_for('static', filename=student_id_face["faceFile"])
            }
        else:
            student_data = {
                "id": student_id_face["id"],
                "name": f"Неизвестный №{abs(student_id_face['id'])}",
                "faceUrl": url_for('static', filename=student_id_face["faceFile"])
            }
        print(student_data)
        students_data.append(student_data)
    students_model = Lesson_Student.query.filter_by(lesson_id=lesson_id).all()
    students = []
    for student_model in students_model:
        student_data = {
            "id": student_model.student.id,
            "name": student_model.student.fio,
        }
        print(student_data)
        students.append(student_data)
    return jsonify({"responsed": students_data, "all": students})

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


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect("/admin")

        courses_data = Course.query.filter_by(user_id=current_user.id).all()
        courses = []
 
        for course in courses_data: 
            lessons = Lesson.query.filter_by(course_id=course.id)
            courses.append([course,lessons])
        
        return render_template("user/index.html", user_id=current_user.id, courses=courses)

    return redirect("/login/")
