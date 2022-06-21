from flask import render_template, redirect, render_template_string, session, request
from flask_app import app
from flask_app.model.user import User
from flask_app.model.recipe import Recipe

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validation(request.form): 
        return redirect('/')
    User.sign_up(request.form)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.login(request.form):
        return redirect('/')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if not session:
        return redirect('/')
    recipes = Recipe.user_recipes()
    print(recipes[0].user.id)
    return render_template('dashboard.html', recipes = recipes)

@app.route('/logout')
def logout():
    User.logout()
    return redirect('/')
    
    

