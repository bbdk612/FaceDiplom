# models.py
# Тут происходит описание всех таблиц в базе данных
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import UserMixin, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from core import app
#TODO создание админа

db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    
    course = db.relationship("User", back_populates="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(100), nullable=False)

class Auditory(db.Model):
    __tablename__ = "auditory"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), unique=True, nullable=False)
    camera_address = db.Column(db.String(300), unique=True, nullable=False)
    
    course = db.relationship("Course", back_populates="auditory")

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", back_populates="course", cascade="all, delete") 

class Lesson(db.Model):
    __tablename__ = "lesson"
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(150), nullable=False)
    datetime = db.Column(db.DateTime, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    auditory_id = db.Column(db.Integer, db.ForeignKey("auditory.id"))

    course = db.relationship("Course", back_populates="lesson", cascade="all, delete")
    auditory = db.relationship("Auditory", back_populates="lesson", cascade="all, delete")

class Lesson_Student(db.Model):
    __tablename__ = "lesson_student"
    id = db.Column(db.Integer, primary_key=True)
    checked = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))

    student = db.relationship("Student", back_populates="lesson_student", cascade="all, delete") 
    lesson = db.relationship("Lesson", back_populates="lesson_student", cascade="all, delete") 
    
