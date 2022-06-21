import re
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.model import recipe

bcrypt = Bcrypt(app)
rege = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'recipes'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = ['created_at']
        self.updated_at = ['updated_at']
        self.recipes = []
    
    @staticmethod
    def validation(data):
        info_valid = True
        if len(data['first_name']) < 2:
            info_valid = False
            flash('First name must be at least 2 characters.', 'regi')
        if len(data['last_name']) < 2:
            info_valid = False
            flash('Last name must be at least 2 characters.', 'regi')
        if not rege.match(data['email']):
            info_valid = False
            flash('Email is not valid.', 'regi')
        if User.check_email(data['email']) == False:
            info_valid = False
            flash('That email is already registered to another account', 'regi')
        if len(data['password']) < 8:
            info_valid = False
            flash('Password must be at least 8 characters long.', 'regi')
        if data['password'] != data['confirm']:
            info_valid = False
            flash('Passwords do not match.', 'regi')
        return info_valid

    @staticmethod
    def parse_in(data):
        parsed = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return parsed
    
    @classmethod
    def check_email(cls, email):
        data = {
            'email' : email
        }
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        """
        result = connectToMySQL(db).query_db(query, data)
        if result:
            return False
        return True

    @classmethod
    def sign_up(cls, data):
        parsed = User.parse_in(data)
        query = """
                INSERT INTO users(first_name, last_name, email, password, created_at, updated_at)
                VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
                """
        id = connectToMySQL(db).query_db(query, parsed)
        session['id'] = id
        session['first_name'] = parsed['first_name']

    @classmethod
    def login(cls, data):
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s
                """
        result = connectToMySQL(db).query_db(query, data)
        if not result or bcrypt.check_password_hash(result[0]['password'], data['password']) == False:
            flash('Email or password is incorrect', 'login')
            return False
        session['id'] = result[0]['id']
        session['first_name'] = result[0]['first_name']
        return True

    @classmethod
    def logout(cls):
        session.clear()
