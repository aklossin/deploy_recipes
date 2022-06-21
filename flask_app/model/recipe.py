from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
from flask_app.model import user
from datetime import date


db = 'recipes'

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made_on = data['date_made']
        self.quick = data['under_30']
        self.user = None

    @staticmethod
    def validation(data):
        is_valid = True
        if len(data['name']) < 3:
            is_valid = False
            flash('Name for recipe is too short')
        if len(data['description']) < 3:
            is_valid = False
            flash('Description needs to be longer')
        if len(data['instructions']) < 3:
            is_valid = False
            flash('Instructions needs to be longer')
        if data['date_made'] == '':
            is_valid = False
            flash('Date needed')
        return is_valid
    
    @classmethod
    def add_recipe(cls, data):
        if not Recipe.validation(data):
            return False
        query = """
        INSERT INTO recipes (name, description, instructions, date_made, under_30, created_at, updated_at, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(radio)s, NOW(), NOW(), %(user_id)s)
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def show_recipe(cls, data):
        print(data)
        data = {
            'id' : data
        }
        query = """
        SELECT id, name, description, instructions, under_30, date_made
        FROM recipes
        WHERE recipes.id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        return result[0]

    @classmethod
    def user_recipes(cls):
        data = {
            'id' : session['id']
        }
        query = """
        SELECT *
        FROM recipes
        JOIN users on recipes.user_id = users.id
        """
        results = connectToMySQL(db).query_db(query, data)
        recipes = []
        for index in results:
            recipe = cls(index)
            recipe_user = {
                'id' : index['users.id'],
                'first_name' : index['first_name'],
                'last_name' : index['last_name'],
                'email' : index['email'],
                'password' : index['password'],
                'created_at' : index['users.created_at'],
                'updated_at' : index['users.updated_at']
            }
            owner = user.User(recipe_user)
            recipe.user = owner
            recipes.append(recipe)
        return recipes

    @classmethod
    def delete_recipe(cls, selected):
        data = {
            'id' : selected,
            'user' : session['id']
        }
        query = """DELETE FROM recipes
        WHERE id = %(id)s
        AND user_id = %(user)s
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def edit_recipe(cls, data):
        input = {
            'id' : data
        }
        if not Recipe.validation(data):
            return False
        query = """UPDATE recipes 
        SET name = %(name)s, 
        description = %(description)s, 
        instructions = %(instructions)s,
        date_made = %(date_made)s,
        updated_at = NOW() 
        WHERE id = %(id)s;
        """
        return connectToMySQL(db).query_db(query, data)
        
