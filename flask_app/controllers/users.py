from flask_app import app
from flask import Flask, request, redirect, render_template, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

bcrypt = Bcrypt(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate(request.form)
    if not is_valid:
        return redirect('/')
    newUser={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email': request.form['email'],
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    id=User.save(newUser)
    if not id:
        flash('something got messed up somewhere')
        return redirect('/')
    session['user_id']=id
    flash('User Created: You are now logged in')
    return redirect ('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data={
        'email':request.form['email']
    }
    user=User.get_by_email(data)
    if not user:
        flash('Incorrect email/password')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect email/password')
        return redirect('/')
    session['user_id']=user.id
    flash('You are now logged in')
    return redirect ('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    data={
        'id':session['user_id']
    }
    theUser=User.get_one(data)
    all_recipes=Recipe.get_all()
    return render_template('dashboard.html', user=theUser, all_recipes=all_recipes)

@app.route('/logout',methods=["POST"])
def logout():
    session.clear()
    return redirect('/')

@app.route("/redirect", methods=['POST'])
def _redirect():
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    return redirect('/dashboard')
