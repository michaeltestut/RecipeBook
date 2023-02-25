from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile('\d.*[A-Z]|[A-Z].*\d')

db = 'recipes_schema'

class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.recipes=[]

    @classmethod
    def get_all(cls):
        query='SELECT * FROM users;'
        results= connectToMySQL(db).query_db(query)
        users=[]
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls,data):
        query='SELECT * FROM users WHERE id = %(id)s;'
        result=connectToMySQL(db).query_db(query,data)
        return cls(result[0])
    @classmethod
    def save(cls,data):
        query='INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls,data):
        pass

    @classmethod
    def remove(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query='SELECT * FROM users WHERE email = %(email)s;'
        result=connectToMySQL(db).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(form):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results=connectToMySQL(db).query_db(query,form)
        if len(results)>=1:
            is_valid=False
            flash('User already in database')
        if len(form['email'])<1:
            flash('*Email is requred field')
            is_valid=False
        if not EMAIL_REGEX.match(form['email']):
            flash('*incorrect email format')
            is_valid=False
        if len(form['first_name']) < 2:
            flash('*first name must be 2 or more letters')
            is_valid = False
        if len(form['last_name']) < 2:
            flash('*last name must be 2 or more letters')
            is_valid = False
        if len(form['password'])<8:
            flash('*Password must be minimum 8 characters')
            is_valid=False
        if not PASSWORD_REGEX.match(form['password']):
            flash('password must contain 1 uppercase letter, 1 lowercase letter, 1 number')
            is_valid=False
        if form['password'] != form['confirm_password']:
            flash('*passwords do not match')
            is_valid=False
        return is_valid
