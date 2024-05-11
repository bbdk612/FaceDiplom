# core/__init__.py
# Тута короче инициализация всего проекта
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder="../templates", static_folder="../templates/static/") # Работает не трогай
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite" # Сюда пихай url до базы данных
app.config["SECRET_KEY"] = "abc" # Ключ нормальный надо


login_manager = LoginManager()
login_manager.init_app(app)

import models
import server
