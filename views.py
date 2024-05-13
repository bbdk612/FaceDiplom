from flask import render_template,  jsonify, redirect, request
from flask_login import current_user, login_required, logout_user
from CameraCapturing import CameraCapturing
from core import app, login_manager
from forms.LoginForm import LoginForm
from models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

cap = None
@app.route('/start_capture', methods=["POST"])
def start_cap():
    global cap
    if cap is None:
        # auditory_id = Lesson.query.filter_by(id=request.form['lesson_id']).first().auditory_id
        # camera_url = Auditory.query.filter_by(id=auditory_id).first().camera_address
        lesson_students = Lesson_Student.query.filter_by(lesson_id=request.form['lesson_id']).all()
        students = []
        for lesson_student in lesson_students:
            students.append(Student.query.filter_by(id=lesson_student.student_id).first())
        cap_data = []
        for student in students:
            cap_data.append([student.image_url, student.id])
        cap = CameraCapturing(0, cap_data)
    cap.start()
    return jsonify({"message": "Zaebis"})

@app.route('/stop_capture', methods=["POST"])
def stop_cap():
    global cap
    students_id = cap.stop_capturing()
    cap = None
    students_fio = [Student.query.filter_by(id=stud_id).first().fio for stud_id in students_id if stud_id != "Неопознаный студент"]
    return jsonify({"studentsId": students_id, "students":students_fio})

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
