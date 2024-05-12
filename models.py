# models.py
# Тут происходит описание всех таблиц в базе данных
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import UserMixin, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from core import app
#TODO создание админа

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    
    course = db.relationship("Course", back_populates="user", cascade="all, delete")
    
    def __init__(self, login: str, fio:str, is_admin:bool):
        self.login = login
        self.fio = fio
        self.is_admin = is_admin

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create(user, password):
        user_check = User.query.filter_by(login=user.login).first()
        if user_check is None:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return {
                "id": user.id, 
                "isAdmin": user.is_admin, 
                "message": "Пользователь успешно создан"
            }

        else:
            return {
                "id": -1, 
                "isAdmin": False, 
                "message": "Пользователь с таким логином уже существует, придумайте другой"
            }

    @staticmethod
    def update(old_user_id: int, new_user: dict):
        old_user = User.query.filter_by(id=old_user_id).first()
        old_user.fio = new_user["fio"]
        old_user.login = new_user["login"]
        old_user.is_admin = new_user["is_admin"]
        old_user.set_password(new_user["password"])
        db.session.commit()

    @staticmethod
    def delete(id: int):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(250), nullable=False)
    
    lesson_student = db.relationship("Lesson_Student", back_populates="student", cascade="all, delete") 
    course_student = db.relationship("Course_Student", back_populates="student", cascade="all, delete")
    
    def __init__(self, fio, image_url):
        self.fio = fio
        self.image_url = image_url

    @staticmethod
    def create(student):
        db.session.add(student)
        db.session.commit()
    
    @staticmethod
    def delete(id):
        student = Student.query.filter_by(id=id).first()
        db.session.delete(student)
        db.session.commit()

    @staticmethod 
    def update(id, new_fio):
        student = Student.query.filter_by(id=id).first()
        student.fio = new_fio
        db.session.commit()

class Auditory(db.Model):
    __tablename__ = "auditory"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    camera_address = db.Column(db.String(300), unique=True, nullable=False)
    
    lesson = db.relationship("Lesson", back_populates="auditory", cascade="all, delete")
    
    def __init__(self, number: str, camera_address: str):
        self.number = number
        self.camera_address = camera_address

    @staticmethod
    def create(auditory):
        check = Auditory.query.filter_by(number=auditory.number).first()
        if not check:
            db.session.add(auditory)
            db.session.commit()
            return {"id": auditory.id, "message": "Все успешно создано"}
        else:
            return {"id": -1, "message": "Такая аудитория уже существует"}
    
    @staticmethod
    def delete(auditory_id):
        auditory = Auditory.query(id=auditory_id).first()
        db.session.delete(auditory)
        db.session.commit()
    
    @staticmethod
    def update(auditory_id, new_camera):
        auditory = Auditory.query.filter_by(id=auditory_id).first()
        auditory.camera_address = new_camera
        db.session.commit()

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    lesson = db.relationship("Lesson", back_populates="course")
    user = db.relationship("User", back_populates="course") 
    course_student = db.relationship("Course_Student", back_populates="course", cascade="all, delete")
    
    @staticmethod
    def create(course):
        db.session.add(course)
        db.session.commit()
    
    @staticmethod
    def delete(course_id):
        course = Auditory.query(id=course_id).first()
        db.session.delete(course)
        db.session.commit()
    
    @staticmethod
    def update(course_id, new_name):
        course = Auditory.query.filter_by(id=course_id).first()
        course.camera_name = new_name
        db.session.commit()

class Course_Student(db.Model):
    __tablename__ = "course_student"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    
    student = db.relationship("Student", back_populates="course_student")
    course = db.relationship("Course", back_populates="course_student")

    def __init__(self, student_id:int, course_id: int):
        self.student_id = student_id
        self.course_id = course_id

    @staticmethod
    def create(course_student):
        db.session.add(course_student)
        db.session.commit()

    @staticmethod
    def delete(course_id, student_id):
        course_students = Course_Student.query.filter_by(course_id=course_id, student_id=student_id).all()
        for course_student in course_students:
            db.session.delete(course_student)
            db.session.commit()

class Lesson(db.Model):
    __tablename__ = "lesson"
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(150), nullable=False)
    datetime = db.Column(db.DateTime, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    auditory_id = db.Column(db.Integer, db.ForeignKey("auditory.id"))

    course = db.relationship("Course", back_populates="lesson", cascade="all, delete")
    auditory = db.relationship("Auditory", back_populates="lesson", cascade="all, delete")
    lesson_student = db.relationship("Lesson_Student", back_populates="lesson", cascade="all, delete") 

    def __init__(self, theme:str, course_id:int, auditory_id:int):
        self.theme = theme
        self.course_id = course_id
        self.auditory_id = auditory_id

    def set_date(self, date):
        self.datetime = date

    @staticmethod 
    def create(lesson):
        db.session.add(lesson)
        db.session.commit()

    @staticmethod
    def delete(id):
        lesson = Lesson.query.filter_by(id=id).first()
        db.query.delete(lesson)

    @staticmethod
    def update(id, new_data):
        lesson = Lesson.query.filter_by(id=id).first()
        lesson.theme = new_data["theme"]
        lesson.datetime = new_data["datetime"]

class Lesson_Student(db.Model):
    __tablename__ = "lesson_student"
    id = db.Column(db.Integer, primary_key=True)
    checked = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))

    student = db.relationship("Student", back_populates="lesson_student", cascade="all, delete") 
    lesson = db.relationship("Lesson", back_populates="lesson_student", cascade="all, delete") 
    
    def __init__(self, student_id, lesson_id):
        self.student_id = student_id
        self.lesson_id = lesson_id
    
    @staticmethod
    def set_checked(student_id, lesson_id):
        ls = Lesson_Student.query.filter_by(student_id=student_id, lesson_id=lesson_id).first()
        ls.checked = True
        db.session.commit()
    
    @staticmethod 
    def create(ls):
        db.session.add(ls)
        db.session.commit()

with app.app_context():
    db.create_all()
