# models.py
# Тут происходит описание всех таблиц в базе данных
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import UserMixin, login_user, UserMixin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from core import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    course = db.relationship("Course", back_populates="user", cascade="all, delete")
    
    def __init__(self, login: str, fio:str, is_admin:bool, password:str):
        self.login = login
        self.fio = fio
        self.is_admin = is_admin
        self.password = password

    def set_password(self, password: str):
        self.password = password
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
        old_user.set_password(new_user["password"])
        old_user.login = new_user["login"]
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
    def update(id, student):
        stud = Student.query.filter_by(id=id).first()
        stud.fio = student.fio
        stud.image_url = student.image_url
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
        auditory = Auditory.query.filter_by(id=auditory_id).first()
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
    name = db.Column(db.String(200), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    lesson = db.relationship("Lesson", back_populates="course")
    user = db.relationship("User", back_populates="course") 
    course_student = db.relationship("Course_Student", back_populates="course", cascade="all, delete")
    
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    @staticmethod
    def create(course):
        check = Course.query.filter_by(name=course.name).first()
        if not check:
            db.session.add(course)
            db.session.commit()
            return {"id": course.id, "message": "Курс успешно создан"}
        else: 
            return {"id": -1, "message": "Курс с таким именем уже существует, придумайте другой"}
    
    @staticmethod
    def delete(course_id):
        course = Course.query.filter_by(id=course_id).first()
        db.session.delete(course)
        db.session.commit()
    
    @staticmethod
    def update(course_id, new_name):
        course = Course.query.filter_by(id=course_id).first()
        check = Course.query.filter_by(id=new_name).first()
        if not check or course.id == check.id:
            course.name = new_name
            db.session.commit()
            return {"id": course.id, "message": "Курс успешно создан"}
        else:
            return {"id": -1, "message": "Курс с таким именем уже существует, придумайте другой"}


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
    def delete(cs):
        db.session.delete(cs)
        db.session.commit()

class Lesson(db.Model):
    __tablename__ = "lesson"
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(150), nullable=False)
    datetime = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    auditory_id = db.Column(db.Integer, db.ForeignKey("auditory.id"))

    course = db.relationship("Course", back_populates="lesson")
    auditory = db.relationship("Auditory", back_populates="lesson")
    lesson_student = db.relationship("Lesson_Student", back_populates="lesson", cascade="all, delete") 

    def __init__(self, theme:str, course_id:int, auditory_id:int):
        self.theme = theme
        self.course_id = course_id
        self.auditory_id = auditory_id
        self.completed = False

    def set_date(self, date):
        self.datetime = date
        self.completed = True
        db.session.commit()

    @staticmethod 
    def create(lesson):
        db.session.add(lesson)
        db.session.commit()

    @staticmethod
    def delete(id):
        lesson = Lesson.query.filter_by(id=id).first()
        db.session.delete(lesson)
        db.session.commit()

    @staticmethod
    def update(id, new_data):
        lesson = Lesson.query.filter_by(id=id).first()
        lesson.theme = new_data["theme"]
        lesson.auditory_id = new_data["new_auditory"]
        db.session.commit()

class Lesson_Student(db.Model):
    __tablename__ = "lesson_student"
    id = db.Column(db.Integer, primary_key=True)
    checked = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))

    student = db.relationship("Student", back_populates="lesson_student") 
    lesson = db.relationship("Lesson", back_populates="lesson_student") 
    
    def __init__(self, student_id, lesson_id):
        self.student_id = student_id
        self.lesson_id = lesson_id
        self.checked = False
    
    def set_checked(self):
        self.checked = True
        db.session.commit()

    def set_unchecked(self):
        self.checked = False
        db.session.commit()
    @staticmethod 
    def create(ls):
        db.session.add(ls)
        db.session.commit()
    
    @staticmethod
    def delete(ls):
        db.session.delete(ls)
        db.session.commit()

with app.app_context():
    db.create_all()
