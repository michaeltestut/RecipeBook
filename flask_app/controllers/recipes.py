from flask import flash, session, redirect, render_template, request
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.controllers import users


@app.route('/add', methods=['POST'])
def add():
    return redirect('/add_recipe')

@app.route ('/add_recipe')
def add_recipe():
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    return render_template('add_recipe.html')

@app.route('/create', methods=['POST'])
def create():
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    is_valid = Recipe.validate(request.form)
    if is_valid == False:
        return redirect('/add_recipe')
    data={
        "recipe_name":request.form['recipe_name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "time": request.form['time'],
        "date_made": request.form['date_made'],
        "users_id": session['user_id']
        }
    Recipe.save(data)
    flash('Recipe Added')
    return redirect ('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    recipe_data={
        'id': id
    }
    return render_template('edit_recipe.html',recipe=Recipe.get_one(recipe_data))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    is_valid = Recipe.validate(request.form)
    if is_valid == False:
        return redirect(f'/edit/{id}')
    data={
        "id":id,
        "recipe_name":request.form['recipe_name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "time": request.form['time'],
        "date_made": request.form['date_made'],
        "users_id": session['user_id']
        }
    Recipe.update(data)
    flash('Recipe Updated')
    return redirect ('/dashboard')


@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    data={
        "id":id
    }
    Recipe.remove(data)
    flash('Recipe deleted')
    return redirect('/dashboard')

@app.route('/view_recipe/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/')
    data={
        "id":id
    }
    return render_template('view_recipe.html', recipe=Recipe.get_one(data))