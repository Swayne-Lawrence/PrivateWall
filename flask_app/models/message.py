from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Message:
    def __init__(self,message_data):
        self.id=message_data["id"]
        self.message=message_data["message"]
        self.sender=message_data["sender"]
        self.created_at=message_data["created_at"]
        self.updated_at=message_data["updated_at"]
        self.user=None
    
    @classmethod
    def save(cls,data):
        query="INSERT INTO messages(message,users_id,sender) VALUES(%(message)s,%(users_id)s,%(sender)s);"
        return connectToMySQL("user_msg_schema").query_db(query,data)
    @classmethod
    def delete(cls,data):
        query="DELETE FROM messages WHERE id=%(id)s;"
        return connectToMySQL("user_msg_schema").query_db(query,data)
    @staticmethod
    def validate(message):
        is_valid=True
        if len(message["message"])<5:
            flash("message too short")
            is_valid=False
        if len(message["users_id"])<1:
            flash("Select a user")
            is_valid=False
        return is_valid