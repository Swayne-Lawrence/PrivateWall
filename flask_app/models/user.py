from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models import message
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,user_data):
        self.id=user_data["id"]
        self.first_name=user_data["first_name"]
        self.last_name=user_data["last_name"]
        self.email=user_data["email"]
        self.password=user_data["password"]
        self.created_at=user_data["created_at"]
        self.updated_at=user_data["updated_at"]
        self.messages=[]
    
    @classmethod
    def save(cls,data):
        query="INSERT INTO users(first_name, last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL("user_msg_schema").query_db(query,data)
    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM users WHERE id=%()s;"
        result=connectToMySQL("user_msg_schema").query_db(query,data)
        return  cls(result[0])
    @classmethod
    def check_email(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        results=connectToMySQL("user_msg_schema").query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])
    @classmethod
    def get_all(cls):
        query="SELECT * FROM users;"
        results=connectToMySQL("user_msg_schema").query_db(query)
        users=[]
        for r in results:
            users.append(cls(r))
        return users
    @classmethod
    def get_one_with_message(cls,data):
        query="SELECT * FROM users LEFT JOIN messages ON users.id=messages.users_id WHERE users.id=%(id)s order by messages.created_at desc;"
        result=connectToMySQL("user_msg_schema").query_db(query,data)
        user=cls(result[0])
        for r in result:
            message_db={
                "id":r["messages.id"],
                "message":r["message"],
                "sender":r["sender"],
                "created_at":r["messages.created_at"],
                "updated_at":r["messages.updated_at"]
            }
            user.messages.append(message.Message(message_db))
        return user
    @staticmethod
    def validate(user):
        is_valid=True
        query="SELECT * FROM users WHERE email=%(email)s;"
        results=connectToMySQL("user_msg_schema").query_db(query,user)
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email")
            is_valid=False
        if (len(user["first_name"])<2) or (len(user["last_name"])<2):
            flash("First and Last name should be more then 2 letters")
            is_valid=False
        if user["password"] != user["confirm"]:
            flash("Passwords must match")
            is_valid=False
        if len(results)>=1:
            flash("email already exist")
            is_valid=False
        return is_valid