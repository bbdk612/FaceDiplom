from core import app
from flask_login import login_required, current_user
from flask import render_template, request, redirect, jsonify, flash, get_flashed_messages
from forms import CoursesForm, LessonForm
from models import Student, Course, Course_Student, Auditory, Lesson, Lesson_Student
from datetime import datetime

def user_views_init():
    
    @app.route('/course/<user_id>/create', methods=["POST", "GET"])
    @login_required
    def create_course(user_id):
        form = CoursesForm(request.form)
        form.students.choices = [(stud.id, stud.fio) for stud in Student.query.order_by(Student.fio).all()]
        
        if request.method == "POST":
            print(form.students.data)
            course = Course(name=form.name.data, user_id=user_id)
            course_data = Course.create(course)
            if course_data["id"] == -1:
                flash(course_data["message"])
            else:
                flash("Курс успешно создан")
                for student_id in form.students.data:
                    cs = Course_Student(course.id, student_id)
                    Course_Student.create(cs)
                return redirect("/")
                # pass
        return render_template("user/make_course.html", form=form)
    
    @app.route("/course/update/<course_id>", methods=["POST", "GET"])
    @login_required 
    def update_course(course_id):
        form = CoursesForm(request.form)
        form.students.choices = [(stud.id, stud.fio) for stud in Student.query.order_by(Student.fio).all()]
        if request.method == "POST" and form.validate():
            css = Course_Student.query.filter_by(course_id=course_id).all()
            for cs in css:
                Course_Student.delete(cs)

            lessons = Lesson.query.filter_by(course_id=course_id).all()
            for lesson in lessons:
                lss = Lesson_Student.query.filter_by(lesson_id=lesson.id).all()
                for ls in lss:
                    Lesson_Student.delete(ls)

            course_data = Course.update(course_id=course_id, new_name=form.name.data)
            if course_data["id"] == -1:
                flash(course_data["message"])
            else:
                flash("Курс успешно создан")
                for student in form.students.data:
                    cs = Course_Student(course_id, student)
                    Course_Student.create(cs)
                    for lesson in lessons:
                        ls = Lesson_Student(lesson_id=lesson.id, student_id=student)
                        Lesson_Student.create(ls)
                    
                return redirect("/")

        form.students.data = [cs.student_id for cs in Course_Student.query.filter_by(course_id=course_id).all()]
        print(form.students.data)
        course = Course.query.filter_by(id=course_id).first()
        return render_template("user/update_course.html", form=form, course=course) 

    @app.route('/lesson/<course_id>/create', methods=["POST", "GET"])
    @login_required
    def create_lesson(course_id):
        form = LessonForm(request.form)
        form.auditory.choices = [(aud.id, aud.number) for aud in Auditory.query.order_by(Auditory.number).all()]
        
        if request.method == "POST" and form.validate():
            lesson = Lesson(theme=form.name.data, auditory_id=form.auditory.data, course_id=course_id)
            Lesson.create(lesson)
            flash("Занятие успешно создано")
            students_course = Course_Student.query.filter_by(course_id=course_id).all()
            for student in students_course:
                ls = Lesson_Student(lesson.id, student.student_id)
                Lesson_Student.create(ls)
            
            return redirect("/")

        return render_template("user/make_lesson.html", form=form)
    
    @app.route("/lesson/<group_id>/update/<lesson_id>", methods=["GET","POST"])
    @login_required 
    def update_lesson(group_id, lesson_id):
        form = LessonForm(request.form)
        form.auditory.choices = [(aud.id, aud.number) for aud in Auditory.query.order_by(Auditory.number).all()]
        
        if request.method == "POST" and form.validate():
            Lesson.update(lesson_id, {"theme": form.name.data, "new_auditory": form.auditory.data})
            return redirect("/")
        
        lesson = Lesson.query.filter_by(id=lesson_id).first()
        form.auditory.data = [lesson.auditory_id]
        return render_template("user/update_lesson.html", form=form, lesson=lesson) 

    @app.route("/lesson/delete/<lesson_id>", methods=["POST"])
    @login_required 
    def delete_lesson(lesson_id):
        Lesson.delete(id=lesson_id)
        return jsonify({"message":"Занятие успешно удалено"})

    @app.route("/lesson/start/<lesson_id>", methods=["GET"])
    @login_required
    def start_lesson(lesson_id):
        date = datetime.now()
        lesson = Lesson.query.filter_by(id=lesson_id).first()
        lesson.set_date(date)
        return render_template("index.html", lesson_id=lesson_id)

    @app.route("/student/check/<lesson_id>", methods=["POST"])
    @login_required
    def student_check(lesson_id):
        print(request.form["students"])
        return jsonify({"123": "123"}), 200
