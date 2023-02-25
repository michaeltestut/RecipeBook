from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db="recipes_schema"

class Recipe:
    def __init__(self,data):
        self.id=data['id']
        self.recipe_name=data['recipe_name']
        self.description=data['description']
        self.instructions=data['instructions']
        self.time=data['time']
        self.date_made=data['date_made']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.users_id=data['users_id']

    @classmethod
    def save(cls,data):
        query="INSERT INTO recipes (recipe_name, description, instructions, time, date_made, users_id) VALUES ( %(recipe_name)s, %(description)s, %(instructions)s, %(time)s, %(date_made)s, %(users_id)s )"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query='SELECT * FROM recipes;'
        results= connectToMySQL(db).query_db(query)
        recipes=[]
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one(cls,data):
        query='SELECT * FROM recipes WHERE id = %(id)s;'
        result=connectToMySQL(db).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def update(cls,data):
        query="UPDATE recipes SET recipe_name=%(recipe_name)s, description=%(description)s, instructions=%(instructions)s, time=%(time)s, date_made=%(date_made)s WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)
        
    @classmethod
    def remove(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)
    
    @staticmethod
    def validate(form):
        is_valid = True
        if len(form['recipe_name'])==0:
            flash('Recipe Name is Required')
            is_valid= False
        if len(form['recipe_name'])<3:
            flash('Recipe name must be at least 3 characters')
            is_valid=False
        if len(form['description'])==0:
            flash('Description is required')
            is_valid= False
        if len(form['description'])<3:
            flash('Description must be at least 3 characters')
            is_valid=False
        if len(form['instructions'])==0:
            flash('Instructions are required')
            is_valid= False
        if len(form['instructions'])<3:
            flash('Instructions must be at least 3 characters')
            is_valid=False
        if form['date_made']== "":
            flash("Date Made is required")
            is_valid=False
        return is_valid

