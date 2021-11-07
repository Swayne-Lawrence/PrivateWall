from flask_app import app
from flask import render_template, request, session,flash, redirect
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app.models.message import Message
bcrypt= Bcrypt(app)

@app.route('/')
def register():
    if  'user_id' in session:
        return redirect('/user_page')
    return render_template("register.html")
@app.route('/reg_form', methods=["POST"])
def reg_form():
    if not User.validate(request.form):
        return redirect('/')
    pw_hash=bcrypt.generate_password_hash(request.form["password"])
    data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password":pw_hash

    }
    session["user_id"]=User.save(data)
    return redirect('/user_page')
@app.route('/login_form',methods=["POST"])
def login_form():
    user_db=User.check_email(request.form)
    if (not user_db) or (not bcrypt.check_password_hash(user_db.password,request.form["password"])):
        flash("Invalid email/password")
        return redirect('/')
    session["user_id"]=user_db.id
    return redirect('/user_page')
@app.route('/user_page')
def user_page():
    if not 'user_id' in session:
        return redirect('/')
    data={
        "id":session['user_id']
    }
    users_data=User.get_all()
    user_db=User.get_one_with_message(data)
    return render_template("user_page.html",all_users=users_data,user=user_db)
@app.route('/msg_form', methods=["POST"])
def msg_form():
    if not Message.validate(request.form):
        return redirect('/user_page')

    Message.save(request.form)
    return redirect('/user_page')
@app.route('/delete_msg/<int:id>')
def delete_msg(id):
    data={
        "id":id
    }
    Message.delete(data)
    return redirect("/user_page")
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

