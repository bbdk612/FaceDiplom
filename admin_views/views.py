from core import app
from flask_login import login_required
from flask import render_template, request, redirect, jsonify, flash, get_flashed_messages
from models import User, Student, Auditory
from forms import UpdateUserForm, MakeUserForm, MakeStudentForm, AuditoryForm

def init_admin_routes():
    @app.route("/admin")
    @login_required
    def admin():
        users  = User.query.filter_by(is_admin=False).all()
        admins = User.query.filter_by(is_admin=True).all()
        students = Student.query.all()
        auditories = Auditory.query.all()
        messages = get_flashed_messages()
        return render_template("admin/index.html", 
                               users=users, 
                               admins=admins, 
                               user_class="user", 
                               messages=messages, 
                               student_class="student", 
                               students=students,
                               auditories=auditories,
                               auditory_class="auditory"
                               )
    
    @app.route("/user/delete/<user_id>", methods=["POST"])
    @login_required
    def user_delete(user_id):
        User.delete(user_id)
        return jsonify({"message": "Пользавотель успешо удален"})
    
    @app.route("/student/delete/<user_id>", methods=["POST"])
    @login_required
    def student_delete(user_id):
        Student.delete(user_id)
        return jsonify({"message": "Пользавотель успешо удален"})

    @app.route('/user/update/<user_id>', methods=["GET", "POST"])
    @login_required
    def user_update(user_id):
        old_user = User.query.filter_by(id=user_id).first()
        form = UpdateUserForm(request.form)
        if request.method == "POST" and form.validate():
            user = {
                "fio":form.fio.data,
            }
            User.update(user_id, user)
            return redirect("/admin")
        return render_template("user/update.html", form=form, old_user=old_user)
    
    @app.route("/user/create", methods=["GET", "POST"])
    @login_required
    def user_create():
        form = MakeUserForm(request.form)
        if request.method == "POST" and form.validate():
            user = User(login=form.login.data, fio=form.fio.data, is_admin=False)
            data = User.create(user, form.password.data)
            if data["id"] == -1:
                flash(data["message"])
                return redirect("/user/create")
            else: 
                flash(data["message"])
                return redirect("/admin")

        messages = get_flashed_messages()
        return render_template("admin/make_user.html", form=form, messages=messages)

    @app.route("/admin/create", methods=["GET", "POST"])
    # @login_required
    def admin_create():
        form = MakeUserForm(request.form)
        if request.method == "POST" and form.validate():
            user = User(login=form.login.data, fio=form.fio.data, is_admin=True)
            data = User.create(user, form.password.data)
            if data["id"] == -1:
                flash(data["message"])
                return redirect("/admin/create")
            else: 
                flash(data["message"])
                return redirect("/admin")

        messages = get_flashed_messages()
        return render_template("admin/make_user.html", form=form, messages=messages)

    @app.route("/student/create", methods=["GET", "POST"])
    @login_required
    def student_create():
        form = MakeStudentForm(request.form)
        if request.method == "POST" and form.validate():

            stud = Student(fio=str(form.fio.data), image_url=form.image_url.data)
            Student.create(student=stud)
            flash("Студент успешно создан")
            return redirect("/admin")
    
        return render_template("admin/make_student.html", form=form)

    @app.route('/student/update/<student_id>', methods=["GET", "POST"])
    @login_required
    def update_student(student_id):
        form = MakeStudentForm(request.form)
        if request.method == "POST" and form.validate():
            stud = Student(fio=form.fio.data, image_url=form.image_url.data)
            Student.update(id=student_id, student=stud)
            return redirect("/admin")

        student = Student.query.filter_by(id=student_id).first()
        return render_template("admin/update_student.html", form=form, student=student)

    @app.route("/auditory/create", methods=["GET", "POST"])
    @login_required
    def create_auditory():
        form = AuditoryForm(request.form)

        if request.method == "POST" and form.validate():
            auditory = Auditory(number=form.number.data, camera_address=form.camera_address.data)
            data = Auditory.create(auditory)
            if data["id"] == -1:
                flash(data["message"])
            else:
                flash(data["message"])
                return redirect("/admin")
        return render_template("admin/make_auditory.html", form=form)
    
    @app.route("/auditory/delete/<auditory_id>", methods=["POST"])
    @login_required
    def delete_auditory(auditory_id):
        Auditory.delete(auditory_id=auditory_id)
        return jsonify({"message": "Аудитория успешно удалена"})
