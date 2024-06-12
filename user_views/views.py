from io import StringIO

from core import app
from flask_login import login_required
from flask import (
    render_template,
    request,
    redirect,
    jsonify,
    flash,
    Response,
)
from forms import CoursesForm, LessonForm
from models import (
    Student,
    Course,
    Course_Student,
    Auditory,
    Lesson,
    Lesson_Student,
    Group,
)
from datetime import datetime
import pandas as pd


def user_views_init():
    @app.route("/course/<user_id>/create", methods=["POST", "GET"])
    @login_required
    def create_course(user_id):
        """
        Creates a new course in the database.

        Parameters:
        user_id (str): The unique identifier of the user creating the course.

        Returns:
        render_template: A rendered HTML template for creating a course if the request method is GET.
        redirect: A redirection to the home page after successful course creation if the request method is POST.
        """
        form = CoursesForm(request.form)
        form.students.choices = [
            (stud.id, stud.fio) for stud in Student.query.order_by(Student.fio).all()
        ]

        if request.method == "POST":
            course = Course(name=request.form["name"], user_id=user_id)
            course_data = Course.create(course)
            if course_data["id"] == -1:
                flash(course_data["message"])
            else:
                flash("Курс успешно создан")
                students = request.form.get("students").split()
                print(students)
                for student_id in students:
                    print(student_id)
                    cs = Course_Student(course_id=course.id, student_id=student_id)
                    Course_Student.create(cs)
                return jsonify({"message": "Курс успешно создан"})

        groups = Group.query.order_by(Group.number).all()
        return render_template("user/make_course.html", form=form, groups=groups)

    @app.route("/course/update/<course_id>", methods=["POST", "GET"])
    @login_required
    def update_course(course_id):
        """
        Updates a course in the database.

        Parameters:
        course_id (str): The unique identifier of the course to be updated.

        Returns:
        render_template: A rendered HTML template for updating a course.
        redirect: A redirection to the home page after successful update.
        """
        form = CoursesForm(request.form)
        form.students.choices = [
            (stud.id, stud.fio) for stud in Student.query.order_by(Student.fio).all()
        ]
        if request.method == "POST":
            # Update the course
            course_data = Course.update(course_id=course_id, new_name=form.name.data)
            if course_data["id"] == -1:
                flash(course_data["message"])
            else:
                flash("Курс успешно создан")
                
                return redirect("/")
        
        students = [
            cs.student
            for cs in Course_Student.query.filter_by(course_id=course_id).all()
        ]
        # Get the course to be updated
        course = Course.query.filter_by(id=course_id).first()
        return render_template("user/update_course.html", form=form, course=course, students=students)

    @app.route("/course/delete/<course_id>", methods=["POST"])
    @login_required
    def course_delete(course_id):
        """
        Deletes a course from the database.

        Parameters:
        course_id (str): The unique identifier of the course to be deleted.

        Returns:
        jsonify: A JSON response indicating the success of the deletion.
        """
        Course.delete(course_id=course_id)
        return jsonify({"message": "Все успешно удалилось"}), 200

    @app.route("/course/report/<course_id>")
    @login_required
    def report_course(course_id):
        table_data = [["ФИО студента", "Отметка по дате занятия"]]
        course_students = Course_Student.query.filter_by(course_id=course_id).all()
        students = []
        for student in course_students:
            student = Student.query.filter_by(id=student.student_id).first()
            if student:
                students.append(student)
            else:
                return redirect("/")
        students.sort(key=lambda x: x.fio)
        lessons = (
            Lesson.query.filter_by(course_id=course_id)
            .filter(Lesson.datetime)
            .order_by()
            .all()
        )
        lesson_dates = [""] + [
            lesson.datetime.strftime("%d.%m.%Y") for lesson in lessons
        ]
        table_data.append(lesson_dates)
        for student in students:
            student_row = [student.fio]
            for lesson in lessons:
                lesson_students = Lesson_Student.query.filter_by(
                    lesson_id=lesson.id, student_id=student.id
                ).first()
                if lesson_students.checked:
                    student_row.append(True)
                else:
                    student_row.append(False)
            table_data.append(student_row)
        course = Course.query.filter_by(id=course_id).first()
        buffer = StringIO()
        table = pd.DataFrame(table_data)
        table.to_csv(buffer, encoding="utf8", index=False, sep=",")
        buffer.seek(0)
        response = Response(buffer, mimetype="text/csv")
        response.headers.set(
            "Content-Disposition",
            "attachment",
            filename="Order_{0}.csv".format(course.id),
        )
        return response

    @app.route("/lesson/<course_id>/create", methods=["POST", "GET"])
    @login_required
    def create_lesson(course_id):
        form = LessonForm(request.form)
        form.auditory.choices = [
            (aud.id, aud.number)
            for aud in Auditory.query.order_by(Auditory.number).all()
        ]

        if request.method == "POST" and form.validate():
            lesson = Lesson(
                theme=form.name.data,
                auditory_id=form.auditory.data,
                course_id=course_id,
            )
            Lesson.create(lesson)
            flash("Занятие успешно создано")
            students_course = Course_Student.query.filter_by(course_id=course_id).all()
            for student in students_course:
                ls = Lesson_Student(lesson_id=lesson.id, student_id=student.student_id)
                Lesson_Student.create(ls)

            return redirect("/")

        return render_template("user/make_lesson.html", form=form)

    @app.route("/lesson/<group_id>/update/<lesson_id>", methods=["GET", "POST"])
    @login_required
    def update_lesson(group_id, lesson_id):
        form = LessonForm(request.form)
        form.auditory.choices = [
            (aud.id, aud.number)
            for aud in Auditory.query.order_by(Auditory.number).all()
        ]

        if request.method == "POST" and form.validate():
            Lesson.update(
                lesson_id, {"theme": form.name.data, "new_auditory": form.auditory.data}
            )
            return redirect("/")

        lesson = Lesson.query.filter_by(id=lesson_id).first()
        form.auditory.data = [lesson.auditory_id]
        return render_template("user/update_lesson.html", form=form, lesson=lesson)

    @app.route("/lesson/delete/<lesson_id>", methods=["POST"])
    @login_required
    def delete_lesson(lesson_id):
        Lesson.delete(id=lesson_id)
        return jsonify({"message": "Занятие успешно удалено"})

    @app.route("/lesson/start/<lesson_id>", methods=["GET"])
    @login_required
    def start_lesson(lesson_id):
        date = datetime.now()
        lesson = Lesson.query.filter_by(id=lesson_id).first()
        lesson.set_date(date)
        return render_template("index.html", lesson_id=lesson_id)

    @app.route("/lesson/check_edit/<lesson_id>", methods=["GET", "POST"])
    @login_required
    def check_edit(lesson_id):
        lesson_students = Lesson_Student.query.filter_by(lesson_id=lesson_id).all()
        return render_template("user/check_edit.html", lesson_students=lesson_students)

    @app.route("/lesson/student/<sl_id>/check", methods=["POST"])
    @login_required
    def check_student(sl_id):
        lesson = Lesson_Student.query.filter_by(id=sl_id).first()
        lesson.set_checked()
        return jsonify({"message": "ok"})

    @app.route("/lesson/student/<sl_id>/uncheck", methods=["POST"])
    @login_required
    def uncheck_student(sl_id):
        lesson = Lesson_Student.query.filter_by(id=sl_id).first()
        lesson.set_unchecked()

        return jsonify({"message": "ok"})

    @app.route("/student/check/<lesson_id>", methods=["POST"])
    @login_required
    def student_check(lesson_id):
        students_ids = request.form["students"].split(";")
        lss = Lesson_Student.query.filter_by(lesson_id=lesson_id).all()
        for ls in lss:
            student = Student.query.filter_by(id=ls.student_id).first()
            if str(student.id) in students_ids:
                ls.set_checked()

        lesson = Lesson.query.filter_by(id=lesson_id).first()
        lesson.set_date(datetime.now())
        return jsonify({"123": "123"}), 200
