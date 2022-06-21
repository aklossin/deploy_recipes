from flask import render_template, redirect, render_template_string, session, request
from flask_app import app
from flask_app.model.recipe import Recipe

@app.route('/recipes/new')
def new_recipe():
    if not session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if not session:
        return redirect('/')
    if not Recipe.validation(request.form):
        return redirect('/recipes/new')
    new = Recipe.add_recipe(request.form)
    return redirect(f'/recipes/{new}')

@app.route('/recipes/<selected>')
def show_recipe(selected):
    if not session:
        return redirect('/')
    recipe = Recipe.show_recipe(selected)
    return render_template('recipe.html', recipe = recipe)

@app.route('/recipes/edit/<selected>')
def edit_recipe(selected):
    if not session:
        return redirect('/')
    recipe = Recipe.show_recipe(selected)
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/change', methods=['POST'])
def change_recipe():
    if not session:
        return redirect('/')
    id = request.form['id']
    if not Recipe.validation(request.form):
        return redirect(f'/recipes/edit/{id}')
    Recipe.edit_recipe(request.form)
    return redirect(f'/recipes/{id}')

@app.route('/recipes/delete/<selected>')
def delete_recipe(selected):
    if not session:
        return redirect('/')
    Recipe.delete_recipe(selected)
    return redirect('/dashboard')