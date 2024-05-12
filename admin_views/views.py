from core import app
from flask_login import login_required
from flask import render_template, request, redirect
from models import User
from forms import UpdateUserForm

def init_admin_routes():
    @app.route("/admin")
    @login_required
    def admin():
        users  = User.query.filter_by(is_admin=False).all()
        admins = User.query.filter_by(is_admin=True).all()
        return render_template("admin/index.html", users=users, admins=admins, data_class="user")

    @app.route('/user/update/<user_id>', methods=["GET", "POST"])
    def user_update(user_id):
        old_user = User.query.filter_by(id=user_id).first()
        form = UpdateUserForm(request.form)
        if request.method == "POST" and form.validate():
            user = {
                "fio":form.fio.data,
                "login":form.login.data,
                "is_admin":form.is_admin.data,
                "password": form.password.data
            }
            User.update(user_id, user)
            return redirect("/admin")
        return render_template("user/update.html", form=form, old_user=old_user)
